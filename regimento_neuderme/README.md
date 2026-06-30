# Regimento Interno — NewDerm (Ribeiro e Gonçalves Ltda.)

Minuta do Regimento Interno da clínica de estética **NewDerm**, elaborada para
atender à exigência da Vigilância Sanitária:

> **RDC ANVISA nº 63/2011, art. 9º** — apresentar regimento interno (ou
> documento equivalente), atualizado, contemplando a definição e a descrição de
> **todas as atividades técnicas, administrativas e assistenciais,
> responsabilidades e competências**. *(Prazo concedido: 30 dias.)*

## Arquivos
- `Regimento Interno - NEWDERM - Minuta v01.docx` — documento editável (Word).
- `gerar_regimento.py` — gerador do documento (reexecutável).
- `assets/` — local para o logotipo (ver instruções na pasta).

## Estrutura (29 seções + capa, folha de aprovação e sumário)
Capa · Folha de aprovação · Sumário · Objetivo · Base legal · Dados da empresa ·
Organograma · Estrutura organizacional · Missão/visão/valores · Política da
qualidade · Estrutura física · Atividades técnicas · Atividades administrativas ·
Atividades assistenciais · Competências (RT, recepção, apoio) · Fluxo de
atendimento · Segurança do paciente · Humanização · Biossegurança · EPIs ·
Limpeza/desinfecção/esterilização · Resíduos (PGRSS) · Estoque · Equipamentos ·
Controle de documentos · Sigilo e LGPD · Treinamento · Auditoria interna ·
Disposições finais · Termo de ciência.

## Pendências para finalização (preencher/confirmar)
1. **Logo** — colocar o PNG em `assets/` e regenerar (ver `assets/`).
2. **Grafia da marca** — confirmar se o nome de fantasia registrado é
   `NewDerm`, `NEWDERM` ou outro.
3. **Dados a preencher** — horário de funcionamento e telefone de contato.
4. **Complementos** — POPs e PGRSS detalhados (citados como anexos).

## Como regenerar
```bash
pip install python-docx
python3 regimento_neuderme/gerar_regimento.py
```
