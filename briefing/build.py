"""Montagem do texto do briefing.

Combina o conteúdo que já vem das outras fontes (ClickUp, atas, anotações) com
o bloco gerado a partir dos prints (e-mail, agenda, WhatsApp), organizado de
forma clara e destacando o que exige ação.
"""

from __future__ import annotations

from .audio import ensure_closing_phrase
from .ocr import PrintItem

_CATEGORY_LABELS = {
    "email": "E-mails",
    "agenda": "Compromissos de agenda",
    "whatsapp": "Mensagens de WhatsApp",
    "outro": "Outros",
}
_CATEGORY_ORDER = ("email", "agenda", "whatsapp", "outro")


def render_prints_block(items: list[PrintItem]) -> str:
    """Renderiza o bloco de prints, agrupado por categoria, com ações em destaque."""
    if not items:
        return "Não há novos prints de e-mail, agenda ou WhatsApp para hoje."

    lines: list[str] = ["Resumo dos prints (capturas) de hoje:"]
    for category in _CATEGORY_ORDER:
        group = [it for it in items if it.category == category]
        if not group:
            continue
        lines.append("")
        lines.append(f"{_CATEGORY_LABELS[category]}:")
        for it in group:
            title = it.title or "(sem título)"
            lines.append(f"- {title}: {it.summary}")
            if it.requires_action and it.action:
                lines.append(f"  Ação necessária: {it.action}")

    actions = [it for it in items if it.requires_action and it.action]
    if actions:
        lines.append("")
        lines.append("O que exige a sua ação:")
        for it in actions:
            origem = _CATEGORY_LABELS.get(it.category, "Item")
            lines.append(f"- [{origem}] {it.title}: {it.action}")

    return "\n".join(lines)


def build_briefing_text(items: list[PrintItem], base_sections: str | None = None) -> str:
    """Monta o texto final do briefing e garante a frase de encerramento.

    ``base_sections`` é o conteúdo que já vem das demais fontes (ClickUp, atas,
    anotações). Pode ser ``None``/vazio quando só queremos o bloco de prints.
    """
    parts: list[str] = []
    if base_sections and base_sections.strip():
        parts.append(base_sections.strip())
    parts.append(render_prints_block(items))
    text = "\n\n".join(parts)
    return ensure_closing_phrase(text)
