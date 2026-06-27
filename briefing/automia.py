"""Conector da API Automia (API Hub).

Autenticação via OAuth 2.0 no fluxo *Client Credentials*: a gente troca
``client_id`` + ``client_secret`` por um ``access_token`` no IdP (Keycloak) e
usa esse token no header ``Authorization: Bearer`` de todas as chamadas ao
API Hub.

O token expira em ~5 minutos (``expires_in: 300``); o cliente renova
automaticamente quando o token está perto de expirar ou quando uma chamada
volta ``401``.

Uso básico::

    from briefing.config import Config
    from briefing.automia import AutomiaClient

    client = AutomiaClient.from_config(Config())
    dados = client.get("/algum/endpoint")          # GET autenticado
    novo = client.post("/outro/endpoint", json={...})

Documentação interativa (Swagger): ``https://apihub.automia.com.br/docs``.

> Nunca coloque a ``client_secret`` em código — ela vem de variável de
> ambiente (``AUTOMIA_CLIENT_SECRET``).
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import requests

# Endpoints padrão da Automia (sobrescrevíveis via variáveis de ambiente).
DEFAULT_BASE_URL = "https://apihub.automia.com.br"
DEFAULT_TOKEN_URL = "https://idp.automia.com.br/realms/master/protocol/openid-connect/token"
DEFAULT_CLIENT_ID = "backend-api"

# Margem de segurança (s) para renovar o token antes de ele realmente expirar.
_EXPIRY_SKEW_S = 15


@dataclass
class AutomiaClient:
    """Cliente HTTP autenticado para o API Hub da Automia.

    Cuida do fluxo Client Credentials: obtém o ``access_token``, anexa-o às
    requisições, e renova-o automaticamente quando expira (ou em resposta a um
    ``401``).
    """

    client_secret: str
    client_id: str = DEFAULT_CLIENT_ID
    base_url: str = DEFAULT_BASE_URL
    token_url: str = DEFAULT_TOKEN_URL
    timeout: int = 60

    # Estado interno do token (não passar na construção).
    _access_token: str | None = None
    _expires_at: float = 0.0

    @classmethod
    def from_config(cls, cfg) -> "AutomiaClient":
        """Cria o cliente a partir do :class:`~briefing.config.Config`."""
        if not cfg.automia_configured:
            raise RuntimeError(
                "Automia não configurada: defina AUTOMIA_CLIENT_SECRET "
                "(e, se necessário, AUTOMIA_CLIENT_ID / AUTOMIA_BASE_URL / "
                "AUTOMIA_TOKEN_URL)."
            )
        return cls(
            client_secret=cfg.automia_client_secret,
            client_id=cfg.automia_client_id,
            base_url=cfg.automia_base_url,
            token_url=cfg.automia_token_url,
        )

    # --- Autenticação --------------------------------------------------------

    def _fetch_token(self) -> None:
        """Obtém um novo ``access_token`` no IdP (fluxo Client Credentials)."""
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        last_exc: Exception | None = None
        for attempt in range(4):  # pequenas retentativas para falhas de rede
            try:
                resp = requests.post(
                    self.token_url,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=self.timeout,
                )
                resp.raise_for_status()
                payload = resp.json()
                self._access_token = payload["access_token"]
                expires_in = int(payload.get("expires_in", 300))
                self._expires_at = time.monotonic() + expires_in - _EXPIRY_SKEW_S
                return
            except requests.RequestException as exc:  # rede instável
                last_exc = exc
                time.sleep(2 ** attempt)
        raise RuntimeError(f"Falha ao obter token da Automia: {last_exc}")

    def _token_valid(self) -> bool:
        return bool(self._access_token) and time.monotonic() < self._expires_at

    def get_token(self, force: bool = False) -> str:
        """Devolve um ``access_token`` válido, renovando-o se necessário."""
        if force or not self._token_valid():
            self._fetch_token()
        assert self._access_token is not None  # garantido por _fetch_token
        return self._access_token

    # --- Requisições ---------------------------------------------------------

    def _url(self, path: str) -> str:
        if path.startswith(("http://", "https://")):
            return path
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        """Faz uma chamada autenticada ao API Hub.

        Anexa o ``Authorization: Bearer`` automaticamente e, se receber ``401``
        (token expirado/inválido), renova o token uma vez e repete a chamada.
        """
        url = self._url(path)
        headers = dict(kwargs.pop("headers", {}) or {})

        for attempt in range(2):  # 1ª tentativa + 1 retry após renovar o token
            headers["Authorization"] = f"Bearer {self.get_token(force=attempt == 1)}"
            resp = requests.request(
                method, url, headers=headers, timeout=self.timeout, **kwargs
            )
            if resp.status_code == 401 and attempt == 0:
                continue  # token expirou no meio do caminho: renova e tenta de novo
            resp.raise_for_status()
            return resp
        resp.raise_for_status()  # pragma: no cover - guarda de segurança
        return resp

    def get(self, path: str, **kwargs: Any) -> Any:
        """GET autenticado; devolve o JSON da resposta."""
        return self.request("GET", path, **kwargs).json()

    def post(self, path: str, **kwargs: Any) -> Any:
        """POST autenticado; devolve o JSON da resposta."""
        return self.request("POST", path, **kwargs).json()
