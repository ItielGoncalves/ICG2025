# -*- coding: utf-8 -*-
"""
Gerador da Minuta de Regimento Interno da NEWDERM (Ribeiro e Gonçalves Ltda.).
Atende à RDC ANVISA nº 63/2011, art. 9º (regimento interno / documento
equivalente contemplando todas as atividades técnicas, administrativas e
assistenciais, responsabilidades e competências).

Saída: .docx editável, com capa, folha de aprovação, sumário (TOC do Word),
seções numeradas e termo de ciência dos colaboradores.
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ---------------------------------------------------------------------------
# Dados reais da clínica
# ---------------------------------------------------------------------------
import glob, os

RAZAO_SOCIAL = "Ribeiro e Gonçalves Ltda."
NOME_FANTASIA = "NewDerm"
CNPJ = "47.607.774/0001-49"
ENDERECO = "Rua Presidente Vargas, 1695, Sala 912, Vila Progresso, Dourados-MS"
RT_NOME = "Dra. Paula Alice Rodolfo Ribeiro Gonçalves"
RT_TITULO = "Farmacêutica – CRF-MS 7048 – Habilitada em Farmácia/Saúde Estética"
RECEP_NOME = "Emanoelly Carneiro de Almeida"
CIDADE = "Dourados-MS"
DATA_EXTENSO = "30 de junho de 2026"
VERSAO = "01"

AZUL = RGBColor(0x1F, 0x3A, 0x5F)
CINZA = RGBColor(0x55, 0x55, 0x55)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
doc = Document()

# Margens
for s in doc.sections:
    s.top_margin = Cm(2.5)
    s.bottom_margin = Cm(2.5)
    s.left_margin = Cm(3.0)
    s.right_margin = Cm(2.5)

# Fonte base
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.line_spacing = 1.15

# Estilo de títulos
for lvl, sz, color in ((1, 14, AZUL), (2, 12, AZUL)):
    st = doc.styles[f"Heading {lvl}"]
    st.font.name = "Calibri"
    st.font.size = Pt(sz)
    st.font.bold = True
    st.font.color.rgb = color
    st.paragraph_format.space_before = Pt(12)
    st.paragraph_format.space_after = Pt(4)


def p(text="", *, bold=False, italic=False, size=11, align=None, color=None,
      space_after=6):
    par = doc.add_paragraph()
    if align:
        par.alignment = align
    run = par.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = color
    par.paragraph_format.space_after = Pt(space_after)
    return par


def bullet(text, bold_lead=None):
    par = doc.add_paragraph(style="List Bullet")
    if bold_lead:
        r = par.add_run(bold_lead)
        r.bold = True
        par.add_run(text)
    else:
        par.add_run(text)
    par.paragraph_format.space_after = Pt(2)
    return par


def h1(text):
    return doc.add_heading(text, level=1)


def h2(text):
    return doc.add_heading(text, level=2)


def page_break():
    doc.add_page_break()


def add_toc():
    """Insere campo de sumário automático que o Word atualiza (F9)."""
    par = doc.add_paragraph()
    run = par.add_run()
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = 'TOC \\o "1-2" \\h \\z \\u'
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    txt = OxmlElement("w:t")
    txt.text = "Atualize o sumário no Word: clique aqui e pressione F9."
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_begin)
    run._r.append(instr)
    run._r.append(fld_sep)
    run._r.append(txt)
    run._r.append(fld_end)


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


# ===========================================================================
# 1. CAPA
# ===========================================================================
for _ in range(2):
    doc.add_paragraph()

# Logo: embute se houver arquivo; senão deixa placeholder.
def achar_logo():
    cand = []
    for base in ("regimento_neuderme/assets", "regimento_neuderme",
                 "/root/.claude/uploads/b5aa057c-3a1e-5345-8e88-62a0d712271e"):
        for ext in ("png", "PNG", "jpg", "jpeg", "webp"):
            cand += glob.glob(os.path.join(base, f"*logo*.{ext}"))
            cand += glob.glob(os.path.join(base, f"*newderm*.{ext}"))
            cand += glob.glob(os.path.join(base, f"*new*derm*.{ext}"))
    return cand[0] if cand else None

logo_box = doc.add_paragraph()
logo_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
_logo = achar_logo()
if _logo:
    logo_box.add_run().add_picture(_logo, width=Cm(7.5))
    print("Logo embutido:", _logo)
else:
    lr = logo_box.add_run("[ INSERIR LOGOTIPO DA NEWDERM AQUI ]")
    lr.font.size = Pt(12)
    lr.font.color.rgb = CINZA
    lr.italic = True
    print("Logo nao encontrado em disco -> placeholder mantido.")

for _ in range(2):
    doc.add_paragraph()

p(NOME_FANTASIA, bold=True, size=34, align=WD_ALIGN_PARAGRAPH.CENTER, color=AZUL,
  space_after=2)
p(RAZAO_SOCIAL, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, color=CINZA)

for _ in range(3):
    doc.add_paragraph()

p("REGIMENTO INTERNO", bold=True, size=26, align=WD_ALIGN_PARAGRAPH.CENTER,
  color=AZUL, space_after=2)
p("Documento de organização administrativa, técnica e assistencial",
  italic=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, color=CINZA)

for _ in range(6):
    doc.add_paragraph()

p(f"Versão {VERSAO}", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER)
p(f"{CIDADE} – {DATA_EXTENSO}", size=12, align=WD_ALIGN_PARAGRAPH.CENTER,
  color=CINZA)
page_break()

# ===========================================================================
# 2. FOLHA DE APROVAÇÃO
# ===========================================================================
h1("Folha de Aprovação")
p("Este Regimento Interno foi elaborado, revisado e aprovado pelos "
  "responsáveis abaixo identificados, passando a vigorar a partir da data de "
  "sua aprovação. Qualquer alteração deve ser formalmente registrada na seção "
  "de controle de documentos e em nova folha de aprovação.")

tbl = doc.add_table(rows=4, cols=3)
tbl.style = "Table Grid"
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr = ["Etapa", "Responsável", "Data / Assinatura"]
for i, t in enumerate(hdr):
    c = tbl.rows[0].cells[i]
    c.text = ""
    rr = c.paragraphs[0].add_run(t)
    rr.bold = True
    rr.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    shade(c, "1F3A5F")
linhas = [
    ("Elaborado por", f"{RT_NOME}\n{RT_TITULO}", "____ /____ /______\n\n______________________"),
    ("Revisado por", f"{RT_NOME}\nResponsável Técnica", "____ /____ /______\n\n______________________"),
    ("Aprovado por", "Sócios-administradores\nRibeiro e Gonçalves Ltda.", "____ /____ /______\n\n______________________"),
]
for r, (a, b, cc) in enumerate(linhas, start=1):
    tbl.rows[r].cells[0].text = a
    tbl.rows[r].cells[1].text = b
    tbl.rows[r].cells[2].text = cc
page_break()

# ===========================================================================
# 3. ÍNDICE / SUMÁRIO
# ===========================================================================
h1("Sumário")
add_toc()
page_break()

# ===========================================================================
# 4. OBJETIVO
# ===========================================================================
h1("1. Objetivo")
p("Este Regimento Interno tem por objetivo estabelecer e descrever a "
  "organização administrativa, técnica e assistencial da clínica "
  f"{NOME_FANTASIA}, definindo a estrutura, as rotinas de funcionamento, as "
  "responsabilidades e as competências de todos os integrantes da equipe, de "
  "modo a assegurar a qualidade, a segurança do paciente e o pleno cumprimento "
  "das normas sanitárias vigentes.")
p("O documento serve, ainda, como instrumento de padronização das atividades, "
  "de orientação dos colaboradores e de comprovação, perante a Vigilância "
  "Sanitária, do atendimento ao disposto na RDC ANVISA nº 63/2011, art. 9º, que "
  "exige documento atualizado contemplando a definição e a descrição de todas "
  "as atividades técnicas, administrativas e assistenciais, responsabilidades e "
  "competências do serviço de saúde.")

# ===========================================================================
# 5. BASE LEGAL
# ===========================================================================
h1("2. Base Legal")
p("Este Regimento Interno fundamenta-se na legislação sanitária e profissional "
  "aplicável aos serviços de saúde e à atividade de saúde estética, "
  "destacando-se:")
base = [
    ("RDC ANVISA nº 63/2011 – ", "Dispõe sobre os Requisitos de Boas Práticas de Funcionamento para os Serviços de Saúde (fundamento da exigência do regimento interno – art. 9º)."),
    ("RDC ANVISA nº 50/2002 – ", "Regulamento técnico para planejamento, programação, elaboração e avaliação de projetos físicos de estabelecimentos assistenciais de saúde (estrutura física)."),
    ("RDC ANVISA nº 222/2018 – ", "Regulamenta as Boas Práticas de Gerenciamento dos Resíduos de Serviços de Saúde (PGRSS)."),
    ("RDC ANVISA nº 15/2012 – ", "Requisitos de boas práticas para o processamento de produtos para a saúde (limpeza, desinfecção e esterilização de materiais)."),
    ("Lei nº 13.021/2014 – ", "Dispõe sobre o exercício e a fiscalização das atividades farmacêuticas."),
    ("Resoluções CFF nº 616/2015 e nº 645/2017 – ", "Dispõem sobre a atuação e a habilitação do farmacêutico na área de saúde estética (normas em vigor)."),
    ("Lei nº 13.709/2018 (LGPD) – ", "Lei Geral de Proteção de Dados Pessoais, aplicável ao tratamento de dados de pacientes."),
    ("Norma Regulamentadora NR-32 – ", "Segurança e saúde no trabalho em serviços de saúde (biossegurança)."),
    ("Norma Regulamentadora NR-6 – ", "Equipamentos de Proteção Individual (EPI)."),
    ("Legislações sanitárias estaduais e municipais – ", "Normas da Vigilância Sanitária do Estado de Mato Grosso do Sul (SES-MS) e do Município de Dourados-MS, bem como demais legislações pertinentes."),
]
for lead, txt in base:
    bullet(txt, bold_lead=lead)
p("Observação: a Resolução CFF nº 573/2013, anteriormente utilizada como "
  "referência, teve sua eficácia suspensa por decisão judicial; por essa razão, "
  "a atuação do farmacêutico em saúde estética nesta clínica fundamenta-se nas "
  "normas atualmente vigentes acima indicadas.", italic=True, size=10,
  color=CINZA)

# ===========================================================================
# 6. DADOS DA EMPRESA
# ===========================================================================
h1("3. Dados da Empresa")
dt = doc.add_table(rows=0, cols=2)
dt.style = "Table Grid"
dados = [
    ("Razão Social", RAZAO_SOCIAL),
    ("Nome Fantasia", NOME_FANTASIA),
    ("CNPJ", CNPJ),
    ("Endereço", ENDERECO),
    ("Atividade", "Clínica de saúde estética"),
    ("Responsável Técnica", f"{RT_NOME} – {RT_TITULO}"),
    ("Horário de funcionamento", "________________________ (preencher)"),
    ("Contato / telefone", "________________________ (preencher)"),
]
for k, v in dados:
    row = dt.add_row().cells
    rr = row[0].paragraphs[0].add_run(k)
    rr.bold = True
    shade(row[0], "EAEFF5")
    row[1].text = v

# ===========================================================================
# 7. ORGANOGRAMA
# ===========================================================================
h1("4. Organograma")
p("A estrutura hierárquica da clínica é representada da seguinte forma:")
p("Sócios-administradores (Ribeiro e Gonçalves Ltda.)", bold=True,
  align=WD_ALIGN_PARAGRAPH.CENTER, color=AZUL, space_after=0)
p("│", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
p(f"Responsável Técnica – {RT_NOME}", bold=True,
  align=WD_ALIGN_PARAGRAPH.CENTER, color=AZUL, space_after=0)
p("┌───────────────┴───────────────┐", align=WD_ALIGN_PARAGRAPH.CENTER,
  space_after=0)
p("Recepção / Administrativo            Equipe de Apoio",
  align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
p(f"({RECEP_NOME})            (limpeza, serviços gerais, apoio técnico)",
  align=WD_ALIGN_PARAGRAPH.CENTER, size=10, color=CINZA)

# ===========================================================================
# 8. ESTRUTURA ORGANIZACIONAL
# ===========================================================================
h1("5. Estrutura Organizacional")
p("A clínica organiza-se em três níveis funcionais integrados:")
bullet("instância máxima de decisão, responsável pela gestão administrativa e financeira e pela aprovação das políticas internas.", bold_lead="Direção (sócios-administradores): ")
bullet("responsável pela supervisão de todos os procedimentos técnicos e assistenciais, pela garantia do cumprimento das normas sanitárias e pela coordenação da equipe.", bold_lead="Responsabilidade Técnica: ")
bullet("recepção, agendamento, cadastro de pacientes, controle de documentos e apoio operacional.", bold_lead="Setor administrativo / recepção: ")
bullet("apoio à execução dos procedimentos, limpeza, higienização e organização dos ambientes.", bold_lead="Setor de apoio: ")

# ===========================================================================
# 9. MISSÃO, VISÃO E VALORES
# ===========================================================================
h1("6. Missão, Visão e Valores")
h2("Missão")
p("Promover saúde, bem-estar e autoestima por meio de procedimentos estéticos "
  "seguros, éticos e de qualidade, com atendimento humanizado e respeito à "
  "individualidade de cada paciente.")
h2("Visão")
p("Ser referência em saúde estética na região de Dourados-MS, reconhecida pela "
  "excelência técnica, pela segurança dos procedimentos e pela confiança dos "
  "pacientes.")
h2("Valores")
for v in ["Ética e responsabilidade profissional", "Segurança do paciente",
          "Qualidade e melhoria contínua", "Respeito e atendimento humanizado",
          "Sigilo e proteção de dados", "Cumprimento das normas sanitárias"]:
    bullet(v)

# ===========================================================================
# 10. POLÍTICA DA QUALIDADE
# ===========================================================================
h1("7. Política da Qualidade")
p(f"A {NOME_FANTASIA} compromete-se a prestar serviços de saúde estética com "
  "segurança, qualidade e em conformidade com as normas sanitárias vigentes, "
  "mediante:")
for v in ["padronização das atividades por meio de Procedimentos Operacionais Padrão (POPs);",
          "capacitação contínua da equipe;",
          "controle e rastreabilidade de produtos, materiais e equipamentos;",
          "monitoramento da satisfação e da segurança dos pacientes;",
          "avaliação periódica dos processos por meio de auditorias internas;",
          "melhoria contínua dos serviços prestados."]:
    bullet(v)

# ===========================================================================
# 11. ESTRUTURA FÍSICA
# ===========================================================================
h1("8. Estrutura Física da Clínica")
p("A clínica dispõe de ambientes projetados e dimensionados de acordo com a RDC "
  "ANVISA nº 50/2002 e demais normas sanitárias aplicáveis, garantindo fluxos "
  "adequados, conforto e segurança. A estrutura contempla, no mínimo:")
for v in ["recepção e sala de espera;",
          "sala(s) de procedimentos estéticos, com superfícies laváveis e de fácil higienização;",
          "área/local para processamento e esterilização de materiais;",
          "local para guarda de produtos e materiais (estoque);",
          "sanitário(s);",
          "abrigo/local de armazenamento temporário de resíduos de serviços de saúde;",
          "depósito de material de limpeza (DML)."]:
    bullet(v)
p("Os ambientes são mantidos em adequado estado de conservação, higiene e "
  "iluminação, com mobiliário e revestimentos compatíveis com a atividade "
  "assistencial.", size=10, color=CINZA)

# ===========================================================================
# 12. ATIVIDADES TÉCNICAS  (núcleo da exigência do fiscal)
# ===========================================================================
h1("9. Descrição Detalhada das Atividades Técnicas")
p("As atividades técnicas compreendem os procedimentos estéticos executados ou "
  "supervisionados pela Responsável Técnica, observados a indicação, a avaliação "
  "prévia, o consentimento informado, a técnica asséptica e o registro em "
  "prontuário. São realizados na clínica os seguintes procedimentos:")

proc = [
    ("Limpeza de pele com extração", "higienização profunda da pele, com extração de comedões e impurezas, esfoliação e aplicação de ativos, observando assepsia e uso de material esterilizado/descartável."),
    ("Microagulhamento", "indução percutânea de colágeno por meio de microagulhas, com antissepsia rigorosa, uso de material estéril/descartável de uso único e descarte adequado de perfurocortantes."),
    ("Peelings químicos", "aplicação de agentes químicos para renovação celular, com avaliação prévia do fototipo e da indicação, controle de tempo de ação e orientações pós-procedimento."),
    ("Aplicação de toxina botulínica", "procedimento injetável realizado conforme avaliação, indicação e legislação vigente, com técnica asséptica, controle de lote/validade do produto, registro em prontuário e descarte de perfurocortantes."),
    ("Preenchimento facial", "procedimento injetável com preenchedores, observada avaliação prévia, rastreabilidade do produto (lote/validade), técnica asséptica e registro em prontuário."),
    ("Bioestimuladores faciais", "aplicação de substâncias bioestimuladoras de colágeno, com avaliação, reconstituição e técnica conforme bula e legislação aplicável."),
    ("Eletroporação", "introdução transdérmica de ativos por meio de corrente elétrica, com higienização do equipamento e dos eletrodos entre atendimentos."),
    ("Epilação", "remoção de pelos por método disponível na clínica, com higienização de equipamentos e uso de descartáveis quando aplicável."),
    ("Tratamentos capilares", "procedimentos estéticos voltados ao couro cabeludo e aos fios, com avaliação prévia e uso de produtos regularizados."),
]
for nome, desc in proc:
    h2(nome)
    p(desc)
p("Todos os procedimentos observam: avaliação prévia do paciente; preenchimento "
  "do Termo de Consentimento Livre e Esclarecido (TCLE) quando aplicável; "
  "registro em prontuário; uso de produtos regularizados na ANVISA; controle de "
  "lote e validade; técnica asséptica; e o respeito aos limites legais de "
  "atuação de cada profissional, sob supervisão da Responsável Técnica.",
  bold=False, size=10, color=CINZA)

# ===========================================================================
# 13. ATIVIDADES ADMINISTRATIVAS
# ===========================================================================
h1("10. Descrição das Atividades Administrativas")
p("As atividades administrativas dão suporte ao funcionamento da clínica e "
  "compreendem:")
for v in ["agendamento e confirmação de consultas e procedimentos;",
          "cadastro de pacientes e abertura/organização de prontuários;",
          "controle de documentos, contratos e arquivos;",
          "controle de estoque de produtos e materiais;",
          "gestão financeira e de pagamentos;",
          "guarda e manutenção das licenças, alvarás e documentos legais da clínica;",
          "atendimento ao público e gestão da comunicação;",
          "apoio ao cumprimento das obrigações sanitárias e fiscais."]:
    bullet(v)

# ===========================================================================
# 14. ATIVIDADES ASSISTENCIAIS
# ===========================================================================
h1("11. Descrição das Atividades Assistenciais")
p("As atividades assistenciais referem-se ao cuidado direto ao paciente e "
  "compreendem:")
for v in ["acolhimento e recepção do paciente;",
          "avaliação inicial e anamnese estética;",
          "orientação sobre o procedimento, riscos, cuidados prévios e posteriores;",
          "obtenção do consentimento informado;",
          "execução e acompanhamento do procedimento;",
          "orientações pós-procedimento e agendamento de retornos;",
          "registro completo no prontuário do paciente."]:
    bullet(v)

# ===========================================================================
# 15. COMPETÊNCIAS DA RT
# ===========================================================================
h1("12. Competências da Responsável Técnica")
p(f"A Responsável Técnica, {RT_NOME} ({RT_TITULO}), tem as seguintes "
  "competências e responsabilidades:")
for v in ["responder tecnicamente pela clínica perante a Vigilância Sanitária e demais órgãos;",
          "supervisionar todos os procedimentos técnicos e assistenciais;",
          "elaborar, revisar e fazer cumprir os Procedimentos Operacionais Padrão (POPs);",
          "garantir o cumprimento das normas sanitárias e de biossegurança;",
          "assegurar a regularidade, o controle de lote e a validade de produtos e materiais;",
          "coordenar o gerenciamento de resíduos (PGRSS) e o processamento de materiais;",
          "treinar, orientar e avaliar a equipe;",
          "controlar a documentação técnica e os registros em prontuário;",
          "zelar pela segurança do paciente e pela qualidade dos atendimentos;",
          "atuar dentro dos limites legais de sua habilitação profissional."]:
    bullet(v)

# ===========================================================================
# 16. COMPETÊNCIAS DA RECEPÇÃO
# ===========================================================================
h1("13. Competências da Recepcionista")
p(f"A colaboradora {RECEP_NOME}, responsável pela recepção e pelo apoio "
  "administrativo, tem as seguintes competências:")
for v in ["realizar agendamentos, confirmações e o atendimento ao público;",
          "efetuar o cadastro de pacientes e organizar os prontuários;",
          "prestar apoio administrativo e organizar a documentação;",
          "controlar a agenda e o fluxo de atendimento;",
          "manter o sigilo e a proteção dos dados dos pacientes (LGPD);",
          "apoiar o controle de estoque e a recepção de mercadorias;",
          "zelar pela organização e pela boa apresentação dos ambientes de recepção."]:
    bullet(v)

# ===========================================================================
# 17. COMPETÊNCIAS DA EQUIPE DE APOIO
# ===========================================================================
h1("14. Competências da Equipe de Apoio")
p("A equipe de apoio é responsável por:")
for v in ["executar a limpeza e a higienização dos ambientes conforme POP;",
          "apoiar a organização e a reposição de materiais;",
          "auxiliar no manejo e na segregação dos resíduos;",
          "comunicar à Responsável Técnica qualquer não conformidade observada;",
          "cumprir as normas de biossegurança e utilizar os EPIs adequados."]:
    bullet(v)

# ===========================================================================
# 18. FLUXO DE ATENDIMENTO
# ===========================================================================
h1("15. Fluxo Completo de Atendimento ao Paciente")
fluxo = [
    "Agendamento e cadastro do paciente.",
    "Acolhimento na recepção e confirmação dos dados.",
    "Avaliação/anamnese e definição do procedimento pela Responsável Técnica.",
    "Orientação sobre o procedimento e assinatura do Termo de Consentimento Livre e Esclarecido (TCLE).",
    "Preparo do ambiente e dos materiais (assepsia, EPIs, esterilização).",
    "Execução do procedimento conforme POP.",
    "Registro completo no prontuário.",
    "Orientações pós-procedimento e agendamento de retorno.",
    "Descarte adequado de resíduos e higienização do ambiente.",
    "Acompanhamento e avaliação dos resultados.",
]
for i, f in enumerate(fluxo, 1):
    par = doc.add_paragraph(style="List Number")
    par.add_run(f)
    par.paragraph_format.space_after = Pt(2)

# ===========================================================================
# 19. SEGURANÇA DO PACIENTE
# ===========================================================================
h1("16. Segurança do Paciente")
p("A clínica adota práticas voltadas à segurança do paciente, entre elas:")
for v in ["identificação correta do paciente antes de cada procedimento;",
          "avaliação prévia de indicações, contraindicações e alergias;",
          "uso de produtos regularizados, com controle de lote e validade;",
          "técnica asséptica e materiais esterilizados ou descartáveis;",
          "registro fiel em prontuário;",
          "orientações claras de pré e pós-procedimento;",
          "conduta definida para intercorrências e encaminhamento quando necessário;",
          "notificação de eventos adversos."]:
    bullet(v)

# ===========================================================================
# 20. HUMANIZAÇÃO
# ===========================================================================
h1("17. Humanização do Atendimento")
p("O atendimento na clínica pauta-se pelo respeito, pela empatia e pela "
  "individualidade do paciente, assegurando acolhimento, escuta atenta, "
  "privacidade, informação clara e linguagem acessível em todas as etapas, "
  "promovendo uma experiência segura e de confiança.")

# ===========================================================================
# 21. BIOSSEGURANÇA
# ===========================================================================
h1("18. Biossegurança")
p("A clínica observa as normas de biossegurança (NR-32 e legislação sanitária "
  "aplicável) para prevenir riscos à saúde da equipe e dos pacientes, incluindo:")
for v in ["higienização das mãos antes e após cada atendimento;",
          "uso de EPIs adequados a cada procedimento;",
          "antissepsia da pele e técnica asséptica;",
          "uso de materiais esterilizados ou de uso único;",
          "descarte imediato e seguro de perfurocortantes;",
          "imunização da equipe conforme recomendação (ex.: hepatite B);",
          "limpeza e desinfecção de superfícies e equipamentos entre atendimentos."]:
    bullet(v)

# ===========================================================================
# 22. EPIs
# ===========================================================================
h1("19. Uso de EPIs")
p("Os Equipamentos de Proteção Individual são disponibilizados pela clínica e "
  "de uso obrigatório conforme a NR-6 e a NR-32. Conforme o procedimento, "
  "utilizam-se:")
for v in ["luvas de procedimento e/ou estéreis;",
          "máscara facial;",
          "óculos de proteção / protetor facial, quando indicado;",
          "avental/jaleco;",
          "touca/gorro, quando aplicável."]:
    bullet(v)
p("É vedada a reutilização de EPIs descartáveis. Os EPIs são trocados sempre "
  "que contaminados ou danificados.", size=10, color=CINZA)

# ===========================================================================
# 23. LIMPEZA, DESINFECÇÃO E ESTERILIZAÇÃO
# ===========================================================================
h1("20. Limpeza, Desinfecção e Esterilização")
p("O processamento de produtos para a saúde segue a RDC ANVISA nº 15/2012 e POP "
  "específico, observando as etapas:")
for v in ["limpeza dos materiais imediatamente após o uso;",
          "desinfecção de superfícies e equipamentos com saneantes regularizados;",
          "esterilização de materiais críticos em autoclave, com controle de ciclo;",
          "monitoramento da esterilização (indicadores físicos, químicos e biológicos);",
          "armazenamento adequado dos materiais esterilizados, com data de validade;",
          "prioridade ao uso de materiais descartáveis de uso único."]:
    bullet(v)

# ===========================================================================
# 24. GERENCIAMENTO DE RESÍDUOS
# ===========================================================================
h1("21. Gerenciamento de Resíduos (PGRSS)")
p("A clínica mantém Plano de Gerenciamento de Resíduos de Serviços de Saúde "
  "(PGRSS), em conformidade com a RDC ANVISA nº 222/2018, contemplando a "
  "segregação, o acondicionamento, a identificação, o armazenamento, a coleta e "
  "a destinação final dos resíduos:")
for lead, txt in [
    ("Grupo A (infectantes): ", "acondicionados em saco branco leitoso identificado;"),
    ("Grupo B (químicos): ", "acondicionados conforme características de risco;"),
    ("Grupo D (comuns): ", "recicláveis e rejeitos não contaminados;"),
    ("Grupo E (perfurocortantes): ", "descartados em coletor rígido apropriado, sem reencape de agulhas."),
]:
    bullet(txt, bold_lead=lead)
p("Os resíduos são coletados por empresa licenciada, com guarda dos "
  "comprovantes de coleta e destinação (manifestos).", size=10, color=CINZA)

# ===========================================================================
# 25. CONTROLE DE ESTOQUE
# ===========================================================================
h1("22. Controle de Estoque")
p("O controle de estoque assegura a rastreabilidade e a qualidade dos produtos "
  "utilizados, por meio de:")
for v in ["recebimento com conferência de nota fiscal, lote e validade;",
          "armazenamento adequado (temperatura, ao abrigo de luz e umidade, quando exigido);",
          "controle de validade com uso prioritário dos lotes mais antigos (PEPS);",
          "registro de entradas e saídas;",
          "aquisição de produtos regularizados na ANVISA;",
          "segregação e descarte de produtos vencidos ou avariados."]:
    bullet(v)

# ===========================================================================
# 26. EQUIPAMENTOS E MANUTENÇÃO
# ===========================================================================
h1("23. Controle de Equipamentos e Manutenção")
p("Os equipamentos são mantidos em condições adequadas de uso e segurança, "
  "mediante:")
for v in ["cadastro/inventário dos equipamentos;",
          "manutenção preventiva e corretiva, com registro;",
          "calibração/aferição quando aplicável;",
          "higienização entre atendimentos conforme POP;",
          "guarda dos manuais e dos comprovantes de manutenção."]:
    bullet(v)

# ===========================================================================
# 27. CONTROLE DE DOCUMENTOS
# ===========================================================================
h1("24. Controle de Documentos")
p("A clínica mantém controle de seus documentos (regimento interno, POPs, "
  "PGRSS, manuais, registros e licenças), assegurando:")
for v in ["identificação, versão e data de cada documento;",
          "aprovação por responsável antes da vigência;",
          "atualização periódica e sempre que houver mudança relevante;",
          "guarda organizada e de fácil acesso para consulta e fiscalização;",
          "retirada de circulação de versões obsoletas."]:
    bullet(v)

# ===========================================================================
# 28. SIGILO E LGPD
# ===========================================================================
h1("25. Sigilo Profissional e LGPD")
p("A clínica e seus colaboradores comprometem-se com o sigilo profissional e "
  "com a proteção dos dados pessoais dos pacientes, em conformidade com a Lei "
  "nº 13.709/2018 (LGPD), observando:")
for v in ["coleta de dados estritamente necessária à finalidade do atendimento;",
          "consentimento e informação ao paciente sobre o uso de seus dados;",
          "guarda segura de prontuários e documentos, físicos e digitais;",
          "acesso restrito aos profissionais autorizados;",
          "vedação à divulgação de imagens ou informações sem autorização expressa;",
          "dever de sigilo mantido inclusive após o término do vínculo."]:
    bullet(v)

# ===========================================================================
# 29. TREINAMENTO
# ===========================================================================
h1("26. Treinamento da Equipe")
p("A clínica promove a capacitação contínua da equipe, contemplando:")
for v in ["treinamento de integração de novos colaboradores;",
          "treinamento em biossegurança, EPIs e higienização das mãos;",
          "treinamento nos POPs e no PGRSS;",
          "atualização técnica periódica;",
          "registro dos treinamentos realizados (data, conteúdo e participantes)."]:
    bullet(v)

# ===========================================================================
# 30. AUDITORIA INTERNA
# ===========================================================================
h1("27. Auditoria Interna")
p("A clínica realiza auditorias internas periódicas, sob coordenação da "
  "Responsável Técnica, para verificar a conformidade dos processos com este "
  "regimento, os POPs e a legislação sanitária, incluindo:")
for v in ["verificação do cumprimento das rotinas e dos registros;",
          "identificação de não conformidades;",
          "definição de ações corretivas e preventivas com prazos e responsáveis;",
          "acompanhamento da implementação das melhorias;",
          "registro dos resultados das auditorias."]:
    bullet(v)

# ===========================================================================
# 31. DISPOSIÇÕES FINAIS
# ===========================================================================
h1("28. Disposições Finais")
p("Este Regimento Interno entra em vigor na data de sua aprovação e deve ser "
  "revisado periodicamente, ou sempre que houver alteração relevante na "
  "legislação, na estrutura ou nas atividades da clínica.")
p("É complementado por Procedimentos Operacionais Padrão (POPs), pelo Plano de "
  "Gerenciamento de Resíduos de Serviços de Saúde (PGRSS) e pelos demais manuais "
  "e registros exigidos pela Vigilância Sanitária.")
p("Todos os colaboradores devem conhecer e cumprir as disposições deste "
  "regimento, registrando ciência conforme termo a seguir. Os casos omissos "
  "serão resolvidos pela Direção, ouvida a Responsável Técnica.")

# ===========================================================================
# 32. TERMO DE CIÊNCIA
# ===========================================================================
page_break()
h1("29. Termo de Ciência dos Colaboradores")
p("Declaro, para os devidos fins, que recebi, li e compreendi o Regimento "
  f"Interno da {NOME_FANTASIA} ({RAZAO_SOCIAL}), comprometendo-me a cumprir "
  "integralmente suas disposições, bem como as normas sanitárias, de "
  "biossegurança e de sigilo nele previstas.")
doc.add_paragraph()
tc = doc.add_table(rows=1, cols=4)
tc.style = "Table Grid"
for i, t in enumerate(["Nome completo", "Função", "Data", "Assinatura"]):
    c = tc.rows[0].cells[i]
    rr = c.paragraphs[0].add_run(t)
    rr.bold = True
    rr.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    shade(c, "1F3A5F")
for _ in range(8):
    r = tc.add_row().cells
    for c in r:
        c.paragraphs[0].add_run("\n")

doc.add_paragraph()
p("____________________________________", align=WD_ALIGN_PARAGRAPH.CENTER,
  space_after=0)
p(RT_NOME, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
p(f"Responsável Técnica – {RT_TITULO}", size=10, color=CINZA,
  align=WD_ALIGN_PARAGRAPH.CENTER)

# ---------------------------------------------------------------------------
OUT = "regimento_neuderme/Regimento Interno - NEWDERM - Minuta v01.docx"
doc.save(OUT)
print("OK ->", OUT)
