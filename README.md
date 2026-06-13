# ICG2025 — Briefing diário em áudio

Rotina que gera o áudio do briefing diário, agora com **leitura dos prints**
(e-mail, agenda, WhatsApp) e com o **encerramento do áudio corrigido**.

## O que a rotina faz

1. **Lê a pasta de prints** (OCR/visão) — capturas de e-mail, agenda e WhatsApp.
2. Classifica e resume cada item, **destacando o que exige a sua ação**.
3. Monta o texto do briefing, combinando os prints com o conteúdo que já vem de
   ClickUp, atas e anotações (passado via `--base`).
4. Gera o áudio terminando **sempre** com a frase exata
   **"E por aqui é isso por hoje."** seguida de **5 segundos de silêncio**.
5. Envia o áudio pelo Telegram, com o silêncio final incluído no arquivo.

## Pasta de prints (caminho configurado)

- **Padrão:** `prints/` na raiz do repositório.
- **Para trocar:** defina `BRIEFING_PRINTS_DIR` com o caminho desejado.

Detalhes em [`prints/README.md`](prints/README.md).

## Configuração

Variáveis de ambiente:

| Variável | Para quê | Obrigatória |
|---|---|---|
| `BRIEFING_PRINTS_DIR` | Caminho da pasta de prints | Não (default: `prints/`) |
| `ANTHROPIC_API_KEY` | OCR/visão dos prints | Sim (se houver prints) |
| `BRIEFING_MODEL` | Modelo de visão | Não (default: `claude-opus-4-8`) |
| `TELEGRAM_BOT_TOKEN` | Bot do Telegram | Só para enviar |
| `TELEGRAM_CHAT_ID` | Chat de destino | Só para enviar |
| `BRIEFING_TTS_LANG` / `BRIEFING_TTS_TLD` | Voz (idioma/sotaque) | Não (default: `pt` / `com.br`) |

## Uso

```bash
pip install -r requirements.txt

python run_briefing.py                 # briefing do dia (prints + áudio + Telegram)
python run_briefing.py --base hoje.txt # injeta o conteúdo de ClickUp/atas/anotações
python run_briefing.py --no-telegram   # só gera o áudio
python run_briefing.py --test          # teste rápido, sem ler prints
```

## Testes

```bash
python -m pytest tests/ -v
```

Os testes verificam o encerramento do áudio: a frase exata de fechamento e os
5 segundos de silêncio finais de fato presentes no arquivo exportado.
