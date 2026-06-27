# ICG2025 — Briefing diário em áudio

Rotina que gera o áudio do briefing diário, agora com **leitura dos prints**
(e-mail, agenda, WhatsApp) e com o **encerramento do áudio corrigido**.

> O briefing roda como **Rotina local do Claude Code** (`Briefing dirio local
> clickupplaud` + `Leitura fluida briefing`), com áudio pelo **ElevenLabs** e
> envio no **Telegram**. O texto exato para colar em cada rotina está em
> [`ROTINAS.md`](ROTINAS.md). Este repositório fornece o helper local que as
> rotinas chamam (leitura de prints e correção do encerramento do áudio).

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

# Só corrigir o encerramento de um áudio já pronto (ex.: saída do ElevenLabs):
python run_briefing.py --finalize audio.mp3 --out briefing_final.mp3
```

Motor de TTS padrão: **ElevenLabs** (`ELEVENLABS_API_KEY` + `ELEVENLABS_VOICE_ID`).
Fallback: gTTS com `BRIEFING_TTS_ENGINE=gtts`.

## Conector Automia (API Hub)

Cliente autenticado para o [API Hub da Automia](https://apihub.automia.com.br/docs),
via OAuth 2.0 (*Client Credentials*). Ele obtém o `access_token`, anexa o
`Authorization: Bearer` em cada chamada e **renova o token automaticamente**
quando ele expira (~5 min) ou quando uma chamada volta `401`.

Variáveis de ambiente:

| Variável | Para quê | Obrigatória |
|---|---|---|
| `AUTOMIA_CLIENT_SECRET` | Segredo do client (canal seguro) | Sim |
| `AUTOMIA_CLIENT_ID` | ID do client | Não (default: `backend-api`) |
| `AUTOMIA_BASE_URL` | Base do API Hub | Não (default: `https://apihub.automia.com.br`) |
| `AUTOMIA_TOKEN_URL` | Endpoint de token (IdP) | Não (default: realm `master` da Automia) |

> **Nunca** coloque a `client_secret` no código ou no repositório — use a
> variável de ambiente `AUTOMIA_CLIENT_SECRET`.

```python
from briefing import Config, AutomiaClient

client = AutomiaClient.from_config(Config())
dados = client.get("/algum/endpoint")            # GET autenticado (JSON)
novo = client.post("/outro/endpoint", json={...})  # POST autenticado (JSON)
```

## Apresentações e documentos (padrão do Itiel)

O padrão de nomes e a regra de versionamento estão em [`CLAUDE.md`](CLAUDE.md).
O helper `gestao_arquivos.py` aplica esse padrão **localmente** (precisa de
acesso ao disco; o PDF usa LibreOffice headless):

```bash
# Gerar o vFINAL (.pptx + .pdf) a partir de um .pptx:
python gestao_arquivos.py finalize "2026.06.10 - MULTI - Gestão Tática de Obras v11.pptx"

# Podar versões de uma pasta — mantém 3 distribuídas + vFINAL (dry-run por padrão):
python gestao_arquivos.py prune "/caminho/da/pasta"
python gestao_arquivos.py prune "/caminho/da/pasta" --apply   # apaga de verdade
```

> PDF precisa do LibreOffice (Mac: `brew install --cask libreoffice`), ou defina
> `LIBREOFFICE_BIN`. A poda só funciona em superfície local.

## Testes

```bash
python -m pytest tests/ -v
```

Os testes verificam o encerramento do áudio: a frase exata de fechamento e os
5 segundos de silêncio finais de fato presentes no arquivo exportado.
