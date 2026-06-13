# Ajustes nas Rotinas do Claude Code

As rotinas do briefing são **rotinas locais do Claude Code** (rodam na sua
máquina enquanto ela está ativa). O prompt de cada rotina fica salvo na UI do
Claude Code — não neste repositório. Abaixo está o **texto para colar** em cada
rotina, mais o helper local deste repo que garante o encerramento do áudio.

> Caminho da pasta de prints configurado: **`prints/`** na raiz do repositório
> (`<repo>/prints`). Para usar outra pasta, defina `BRIEFING_PRINTS_DIR`.

---

## Rotina 1 — `Briefing dirio local clickupplaud` (≈03:00)

É a rotina que **monta o conteúdo** do briefing (ClickUp + Plaud/atas + notas).
Acrescente ao prompt dela o bloco abaixo, para incluir os prints:

```
LEITURA DOS PRINTS (e-mail, agenda, WhatsApp):
- Liste as imagens da pasta de prints. O caminho está na variável de ambiente
  BRIEFING_PRINTS_DIR; se ela não existir, use a pasta "prints/" deste projeto.
  Formatos: .png .jpg .jpeg .webp .gif.
- Para cada imagem, leia o conteúdo (OCR/visão) e classifique em:
  E-MAIL, COMPROMISSO DE AGENDA, MENSAGEM DE WHATSAPP, ou OUTRO.
- Inclua no briefing um bloco "Prints de hoje", organizado em três seções
  claras (E-mails / Compromissos de agenda / Mensagens de WhatsApp), com um
  resumo curto de cada item.
- Ao final desse bloco, acrescente a seção "O que exige a minha ação", listando
  apenas os itens que pedem uma ação minha (responder, decidir, comparecer, pagar...).
- Esse bloco entra JUNTO com o que já vem do ClickUp, atas e anotações.
```

> Como rotina local, o Claude Code consegue abrir as imagens diretamente (visão).
> Se preferir uma extração estruturada via API, há o módulo `briefing/ocr.py`
> (precisa de `ANTHROPIC_API_KEY`): `python run_briefing.py --no-telegram`.

---

## Rotina 2 — `Leitura fluida briefing` (≈04:10)

É a rotina que **gera o áudio** (ElevenLabs) e envia pelo Telegram. Dois ajustes:

### a) Frase de encerramento
No texto que vai para o ElevenLabs, garanta que ele **termine sempre** com a
frase exata, em uma linha própria:

```
E por aqui é isso por hoje.
```

### b) 5 segundos de silêncio no fim, sem corte na exportação
O ElevenLabs costuma "aparar" o silêncio final, o que dá a impressão de corte.
Para garantir os 5 segundos, **pós-processe o áudio** com o helper deste repo
antes de enviar no Telegram. Acrescente ao prompt da rotina:

```
ENCERRAMENTO DO ÁUDIO:
- Depois de gerar o áudio com o ElevenLabs, salve-o em um arquivo (ex.: audio.mp3).
- Rode, na pasta deste projeto:
      python run_briefing.py --finalize audio.mp3 --no-telegram --out briefing_final.mp3
  Isso garante a frase "E por aqui é isso por hoje." e acrescenta 5 segundos de
  silêncio reais ao final do arquivo (sem corte na exportação).
- Envie no Telegram o arquivo briefing_final.mp3 (NÃO o original), para que o
  silêncio final vá incluído.
```

> Se a frase de encerramento já estiver no texto enviado ao ElevenLabs, troque
> `--finalize` por `--finalize audio.mp3 --no-closing` (veja `--help`) para não
> repetir a fala — ou deixe como está, que o helper não duplica a frase.

#### Alternativa: deixar o helper gerar o áudio inteiro
Se preferir centralizar tudo aqui (ElevenLabs via este repo), configure
`ELEVENLABS_API_KEY` e `ELEVENLABS_VOICE_ID` e rode:

```
python run_briefing.py            # lê prints, monta texto, gera áudio (ElevenLabs) e envia
python run_briefing.py --base hoje.txt   # injeta o conteúdo de ClickUp/atas/notas
```

---

## Variáveis de ambiente

| Variável | Para quê |
|---|---|
| `BRIEFING_PRINTS_DIR` | Caminho da pasta de prints (default: `prints/`) |
| `ANTHROPIC_API_KEY` | OCR/visão dos prints via `briefing/ocr.py` (opcional) |
| `ELEVENLABS_API_KEY` / `ELEVENLABS_VOICE_ID` | TTS pelo ElevenLabs |
| `ELEVENLABS_MODEL` | Modelo do ElevenLabs (default: `eleven_multilingual_v2`) |
| `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` | Envio pelo Telegram |
| `BRIEFING_TTS_ENGINE` | `elevenlabs` (padrão) ou `gtts` |

> **Observação:** o `--finalize` lê e regrava o áudio com `ffmpeg`/`ffprobe`.
> Na sua máquina local, tenha o ffmpeg instalado (`brew install ffmpeg` no Mac).
