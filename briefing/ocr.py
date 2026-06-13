"""Leitura (OCR/visão) dos prints salvos na pasta configurada.

Cada imagem é enviada ao modelo de visão da Anthropic, que extrai e classifica
o conteúdo em: e-mail, compromisso de agenda, mensagem de WhatsApp ou outro —
destacando o que exige ação do Itiel.
"""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass, asdict
from pathlib import Path

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
MEDIA_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
}

CATEGORIES = ("email", "agenda", "whatsapp", "outro")

_SCHEMA = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "enum": list(CATEGORIES)},
                    "title": {"type": "string"},
                    "summary": {"type": "string"},
                    "requires_action": {"type": "boolean"},
                    "action": {"type": "string"},
                },
                "required": ["category", "title", "summary", "requires_action", "action"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["items"],
    "additionalProperties": False,
}

_PROMPT = (
    "Você está lendo um print de tela (captura) que pode conter um e-mail, um "
    "compromisso de agenda/calendário, uma conversa de WhatsApp, ou outro tipo "
    "de conteúdo. Leia TODO o texto visível (OCR) e extraia os itens relevantes.\n\n"
    "Para cada item identificado, classifique a 'category' como:\n"
    "- 'email': mensagens de e-mail (remetente, assunto, pedido)\n"
    "- 'agenda': compromissos, reuniões, eventos com data/hora\n"
    "- 'whatsapp': mensagens de WhatsApp ou apps de mensagem\n"
    "- 'outro': qualquer outra coisa relevante\n\n"
    "Campos:\n"
    "- 'title': remetente do e-mail / título do compromisso / contato do WhatsApp\n"
    "- 'summary': resumo curto e objetivo do conteúdo\n"
    "- 'requires_action': true se exige uma ação do Itiel (responder, decidir, comparecer, pagar...)\n"
    "- 'action': descreva a ação necessária (string vazia se requires_action for false)\n\n"
    "Se o print tiver vários itens (ex.: várias mensagens), gere um item por assunto relevante. "
    "Responda apenas no formato JSON solicitado."
)


@dataclass
class PrintItem:
    source_file: str
    category: str
    title: str
    summary: str
    requires_action: bool
    action: str

    def to_dict(self) -> dict:
        return asdict(self)


def list_print_images(cfg) -> list[Path]:
    """Lista os arquivos de imagem na pasta de prints, em ordem estável."""
    if not cfg.prints_dir.exists():
        return []
    return sorted(
        p for p in cfg.prints_dir.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    )


def _image_block(path: Path) -> dict:
    data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")
    media_type = MEDIA_TYPES.get(path.suffix.lower(), "image/png")
    return {
        "type": "image",
        "source": {"type": "base64", "media_type": media_type, "data": data},
    }


def extract_items(cfg) -> list[PrintItem]:
    """Roda OCR/visão em todos os prints e devolve os itens classificados."""
    images = list_print_images(cfg)
    if not images:
        return []
    if not cfg.anthropic_api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY não configurada — necessária para ler os prints (OCR/visão)."
        )

    import anthropic

    client = anthropic.Anthropic(api_key=cfg.anthropic_api_key)
    results: list[PrintItem] = []

    for path in images:
        response = client.messages.create(
            model=cfg.anthropic_model,
            max_tokens=4000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        _image_block(path),
                        {"type": "text", "text": _PROMPT},
                    ],
                }
            ],
            output_config={"format": {"type": "json_schema", "schema": _SCHEMA}},
        )
        text = next((b.text for b in response.content if b.type == "text"), "")
        if not text:
            continue
        payload = json.loads(text)
        for raw in payload.get("items", []):
            results.append(
                PrintItem(
                    source_file=path.name,
                    category=raw.get("category", "outro"),
                    title=raw.get("title", "").strip(),
                    summary=raw.get("summary", "").strip(),
                    requires_action=bool(raw.get("requires_action", False)),
                    action=raw.get("action", "").strip(),
                )
            )
    return results
