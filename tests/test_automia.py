"""Testes do conector da API Automia.

Herméticos: não dependem de rede. As chamadas a ``requests`` são substituídas
por fakes que simulam o IdP (token) e o API Hub. Verificamos:
- o fluxo Client Credentials (parâmetros enviados ao endpoint de token);
- a renovação automática quando o token expira;
- o retry transparente diante de um ``401``.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from briefing import automia as automia_mod  # noqa: E402
from briefing.automia import AutomiaClient  # noqa: E402
from briefing.config import Config  # noqa: E402


class _Resp:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json = json_data or {}

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise automia_mod.requests.HTTPError(f"status {self.status_code}")


def _client():
    return AutomiaClient(client_secret="segredo", timeout=1)


def test_from_config_requires_secret():
    cfg = Config(automia_client_secret=None)
    assert cfg.automia_configured is False
    with pytest.raises(RuntimeError):
        AutomiaClient.from_config(cfg)


def test_from_config_uses_config_values():
    cfg = Config(automia_client_secret="xyz", automia_client_id="outro-id")
    client = AutomiaClient.from_config(cfg)
    assert client.client_secret == "xyz"
    assert client.client_id == "outro-id"
    assert client.base_url == "https://apihub.automia.com.br"


def test_client_credentials_flow(monkeypatch):
    captured = {}

    def fake_post(url, data=None, headers=None, timeout=None):
        captured["url"] = url
        captured["data"] = data
        return _Resp(json_data={"access_token": "TOK", "expires_in": 300})

    monkeypatch.setattr(automia_mod.requests, "post", fake_post)

    token = _client().get_token()
    assert token == "TOK"
    assert captured["data"]["grant_type"] == "client_credentials"
    assert captured["data"]["client_id"] == "backend-api"
    assert captured["data"]["client_secret"] == "segredo"


def test_token_is_cached_until_expiry(monkeypatch):
    calls = {"n": 0}

    def fake_post(url, data=None, headers=None, timeout=None):
        calls["n"] += 1
        return _Resp(json_data={"access_token": f"TOK{calls['n']}", "expires_in": 300})

    monkeypatch.setattr(automia_mod.requests, "post", fake_post)

    client = _client()
    assert client.get_token() == "TOK1"
    assert client.get_token() == "TOK1"  # reutiliza, não busca de novo
    assert calls["n"] == 1


def test_request_retries_after_401(monkeypatch):
    tokens = {"n": 0}

    def fake_post(url, data=None, headers=None, timeout=None):
        tokens["n"] += 1
        return _Resp(json_data={"access_token": f"TOK{tokens['n']}", "expires_in": 300})

    seen_auth = []

    def fake_request(method, url, headers=None, timeout=None, **kwargs):
        seen_auth.append(headers["Authorization"])
        # 1ª chamada: 401 (token "expirado"); 2ª: sucesso.
        if len(seen_auth) == 1:
            return _Resp(status_code=401)
        return _Resp(json_data={"ok": True})

    monkeypatch.setattr(automia_mod.requests, "post", fake_post)
    monkeypatch.setattr(automia_mod.requests, "request", fake_request)

    result = _client().get("/algum/endpoint")
    assert result == {"ok": True}
    assert seen_auth == ["Bearer TOK1", "Bearer TOK2"]  # renovou o token no retry


def test_url_join_and_absolute(monkeypatch):
    client = _client()
    assert client._url("/x") == "https://apihub.automia.com.br/x"
    assert client._url("x") == "https://apihub.automia.com.br/x"
    assert client._url("https://outro/y") == "https://outro/y"
