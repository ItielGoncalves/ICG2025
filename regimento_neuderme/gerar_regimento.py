# -*- coding: utf-8 -*-
"""
Gerador da Minuta de Regimento Interno da NewDerm (Ribeiro e Gonçalves Ltda.).
Versão 02 — ampliada e detalhada (15 a 20 páginas), texto justificado,
organograma embutido. Mantém EXATAMENTE os 9 procedimentos do documento
original (sem acréscimos). Atende à RDC ANVISA nº 63/2011, art. 9º.
"""

import glob, os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

J = WD_ALIGN_PARAGRAPH.JUSTIFY
C = WD_ALIGN_PARAGRAPH.CENTER

# ---------------------------------------------------------------------------
RAZAO_SOCIAL = "Ribeiro e Gonçalves Ltda."
NOME_FANTASIA = "NewDerm"
CNPJ = "47.607.774/0001-49"
ENDERECO = "Rua Presidente Vargas, 1695, Sala 912, Vila Progresso, Dourados-MS"
RT_NOME = "Dra. Paula Alice Rodolfo Ribeiro Gonçalves"
RT_TITULO = "Farmacêutica – CRF-MS 7048 – Habilitada em Farmácia/Saúde Estética"
RECEP_NOME = "Emanoelly Carneiro de Almeida"
CIDADE = "Dourados-MS"
DATA_EXTENSO = "30 de junho de 2026"
VERSAO = "02"
HORARIO = "das 8h00 às 11h30 e das 13h30 às 18h00"

AZUL = RGBColor(0x1F, 0x3A, 0x5F)
CINZA = RGBColor(0x55, 0x55, 0x55)

doc = Document()

for s in doc.sections:
    s.top_margin = Cm(2.5)
    s.bottom_margin = Cm(2.5)
    s.left_margin = Cm(3.0)
    s.right_margin = Cm(2.5)

normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.line_spacing = 1.15
normal.paragraph_format.alignment = J

for lvl, sz in ((1, 14), (2, 12)):
    st = doc.styles[f"Heading {lvl}"]
    st.font.name = "Calibri"
    st.font.size = Pt(sz)
    st.font.bold = True
    st.font.color.rgb = AZUL
    st.paragraph_format.space_before = Pt(12)
    st.paragraph_format.space_after = Pt(4)
    st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT


def p(text="", *, bold=False, italic=False, size=11, align=J, color=None,
      space_after=6):
    par = doc.add_paragraph()
    par.alignment = align
    run = par.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = color
    par.paragraph_format.space_after = Pt(space_after)
    return par


def bullet(text, bold_lead=None, justify=True):
    par = doc.add_paragraph(style="List Bullet")
    if justify:
        par.alignment = J
    if bold_lead:
        r = par.add_run(bold_lead)
        r.bold = True
    par.add_run(text)
    par.paragraph_format.space_after = Pt(2)
    return par


def num(text):
    par = doc.add_paragraph(style="List Number")
    par.alignment = J
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
    par = doc.add_paragraph()
    run = par.add_run()
    b = OxmlElement("w:fldChar"); b.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText"); instr.set(qn("xml:space"), "preserve")
    instr.text = 'TOC \\o "1-2" \\h \\z \\u'
    sep = OxmlElement("w:fldChar"); sep.set(qn("w:fldCharType"), "separate")
    t = OxmlElement("w:t"); t.text = "Atualize o sumário no Word: clique aqui e pressione F9."
    e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), "end")
    for x in (b, instr, sep, t, e):
        run._r.append(x)


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def achar(padroes):
    for base in ("regimento_neuderme/assets", "regimento_neuderme",
                 "/root/.claude/uploads/b5aa057c-3a1e-5345-8e88-62a0d712271e"):
        for pat in padroes:
            for ext in ("png", "PNG", "jpg", "jpeg", "webp"):
                r = glob.glob(os.path.join(base, f"{pat}.{ext}"))
                if r:
                    return r[0]
    return None


# ===========================================================================
# CAPA
# ===========================================================================
for _ in range(2):
    doc.add_paragraph()
logo_box = doc.add_paragraph(); logo_box.alignment = C
_logo = achar(["*logo*", "*newderm*", "*new*derm*"])
if _logo:
    logo_box.add_run().add_picture(_logo, width=Cm(7.5))
    print("Logo embutido:", _logo)
else:
    lr = logo_box.add_run("[ INSERIR LOGOTIPO DA NEWDERM AQUI ]")
    lr.font.size = Pt(12); lr.font.color.rgb = CINZA; lr.italic = True
    print("Logo -> placeholder")

for _ in range(2):
    doc.add_paragraph()
p(NOME_FANTASIA, bold=True, size=34, align=C, color=AZUL, space_after=2)
p(RAZAO_SOCIAL, size=14, align=C, color=CINZA)
for _ in range(3):
    doc.add_paragraph()
p("REGIMENTO INTERNO", bold=True, size=26, align=C, color=AZUL, space_after=2)
p("Documento de organização administrativa, técnica e assistencial",
  italic=True, size=12, align=C, color=CINZA)
for _ in range(6):
    doc.add_paragraph()
p(f"Versão {VERSAO}", bold=True, size=12, align=C)
p(f"{CIDADE} – {DATA_EXTENSO}", size=12, align=C, color=CINZA)
page_break()

# ===========================================================================
# FOLHA DE APROVAÇÃO
# ===========================================================================
h1("Folha de Aprovação")
p("Este Regimento Interno foi elaborado, revisado e aprovado pelos responsáveis "
  "abaixo identificados, passando a vigorar a partir da data de sua aprovação. "
  "A presente folha de aprovação constitui registro formal do compromisso da "
  "Direção e da Responsável Técnica com o conteúdo aqui estabelecido, atestando "
  "que o documento foi analisado quanto à sua adequação técnica, à sua "
  "conformidade legal e à sua aderência à realidade operacional da clínica. "
  "Qualquer alteração posterior deverá ser formalmente registrada na seção de "
  "controle de documentos e refletida em nova folha de aprovação, com a "
  "respectiva atualização do número de versão e da data de vigência.")

tbl = doc.add_table(rows=4, cols=3)
tbl.style = "Table Grid"
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, t in enumerate(["Etapa", "Responsável", "Data / Assinatura"]):
    c = tbl.rows[0].cells[i]; c.text = ""
    rr = c.paragraphs[0].add_run(t); rr.bold = True
    rr.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); shade(c, "1F3A5F")
linhas = [
    ("Elaborado por", f"{RT_NOME}\n{RT_TITULO}", "____ /____ /______\n\n______________________"),
    ("Revisado por", f"{RT_NOME}\nResponsável Técnica", "____ /____ /______\n\n______________________"),
    ("Aprovado por", "Sócios-administradores\nRibeiro e Gonçalves Ltda.", "____ /____ /______\n\n______________________"),
]
for r, (a, b, cc) in enumerate(linhas, 1):
    tbl.rows[r].cells[0].text = a
    tbl.rows[r].cells[1].text = b
    tbl.rows[r].cells[2].text = cc
page_break()

# ===========================================================================
# SUMÁRIO
# ===========================================================================
h1("Sumário")
add_toc()
page_break()

# ===========================================================================
# 1. OBJETIVO
# ===========================================================================
h1("1. Objetivo")
p("O presente Regimento Interno tem por objetivo estabelecer, descrever e "
  "formalizar a organização administrativa, técnica e assistencial da clínica "
  f"{NOME_FANTASIA}, de modo a definir com clareza a sua estrutura funcional, as "
  "rotinas de funcionamento, os fluxos de trabalho, as linhas de subordinação e "
  "as responsabilidades e competências atribuídas a cada integrante da equipe. "
  "Constitui, portanto, o documento normativo de referência que orienta a "
  "conduta profissional e operacional de todos os que atuam no estabelecimento, "
  "assegurando uniformidade de procedimentos, previsibilidade das rotinas e "
  "padrão consistente de qualidade e segurança na prestação dos serviços de "
  "saúde estética.")
p("De forma específica, este documento tem por finalidade: (i) padronizar a "
  "execução das atividades por meio da definição de responsabilidades e da "
  "vinculação a Procedimentos Operacionais Padrão (POPs); (ii) resguardar a "
  "segurança do paciente e da equipe, mediante a adoção de boas práticas "
  "sanitárias e de biossegurança; (iii) orientar a integração e a capacitação "
  "de novos colaboradores; (iv) servir de instrumento de gestão para a Direção e "
  "a Responsável Técnica no acompanhamento e na melhoria contínua dos processos; "
  "e (v) comprovar, perante os órgãos de fiscalização, o cumprimento das "
  "exigências legais aplicáveis ao serviço.")
p("Este Regimento Interno atende, em especial, ao disposto na RDC ANVISA nº "
  "63/2011, artigo 9º, que determina que o serviço de saúde deve possuir "
  "regimento interno, ou documento equivalente, atualizado, contemplando a "
  "definição e a descrição de todas as suas atividades técnicas, administrativas "
  "e assistenciais, bem como as responsabilidades e competências de seus "
  "profissionais. Suas disposições aplicam-se, sem exceção, a todos os sócios, "
  "profissionais, colaboradores, estagiários e prestadores de serviço que atuem "
  "nas dependências da clínica, os quais deverão dele tomar ciência formal e "
  "observá-lo integralmente no exercício de suas funções.")

# ===========================================================================
# 2. BASE LEGAL
# ===========================================================================
h1("2. Base Legal")
p("As disposições deste Regimento Interno fundamentam-se no conjunto de normas "
  "sanitárias, trabalhistas e profissionais aplicáveis aos serviços de saúde e, "
  "de modo particular, às atividades de saúde estética. A observância dessa base "
  "legal é condição indispensável ao regular funcionamento da clínica e à "
  "segurança dos pacientes e da equipe. Destacam-se, entre as principais normas "
  "de referência, as seguintes:")
base = [
    ("RDC ANVISA nº 63/2011 – ", "dispõe sobre os Requisitos de Boas Práticas de Funcionamento para os Serviços de Saúde e constitui o fundamento direto da exigência de regimento interno (art. 9º), estabelecendo princípios de organização, qualidade e segurança do paciente."),
    ("RDC ANVISA nº 50/2002 – ", "aprova o regulamento técnico para planejamento, programação, elaboração e avaliação de projetos físicos de estabelecimentos assistenciais de saúde, orientando o dimensionamento e a adequação da estrutura física."),
    ("RDC ANVISA nº 222/2018 – ", "regulamenta as Boas Práticas de Gerenciamento dos Resíduos de Serviços de Saúde (PGRSS), disciplinando a segregação, o acondicionamento, o armazenamento e a destinação final dos resíduos."),
    ("RDC ANVISA nº 15/2012 – ", "dispõe sobre os requisitos de boas práticas para o processamento de produtos para a saúde, orientando as etapas de limpeza, desinfecção e esterilização de materiais."),
    ("Lei nº 13.021/2014 – ", "dispõe sobre o exercício e a fiscalização das atividades farmacêuticas, estabelecendo deveres e responsabilidades do profissional farmacêutico."),
    ("Resoluções CFF nº 616/2015 e nº 645/2017 – ", "dispõem sobre a atuação e a habilitação do farmacêutico na área de saúde estética, normas atualmente em vigor que fundamentam a atuação da Responsável Técnica."),
    ("Lei nº 13.709/2018 (LGPD) – ", "Lei Geral de Proteção de Dados Pessoais, aplicável ao tratamento dos dados pessoais e sensíveis dos pacientes, inclusive dados de saúde."),
    ("Norma Regulamentadora NR-32 – ", "estabelece diretrizes de segurança e saúde no trabalho em serviços de saúde, base das medidas de biossegurança adotadas."),
    ("Norma Regulamentadora NR-6 – ", "disciplina o fornecimento e o uso obrigatório de Equipamentos de Proteção Individual (EPI)."),
    ("Legislações sanitárias estaduais e municipais – ", "normas da Vigilância Sanitária do Estado de Mato Grosso do Sul (SES-MS) e do Município de Dourados-MS, além das demais legislações pertinentes ao funcionamento do estabelecimento."),
]
for lead, txt in base:
    bullet(txt, bold_lead=lead)
p("Nas hipóteses de eventual conflito ou de sobreposição entre normas, "
  "prevalecerá sempre a disposição mais restritiva e mais protetiva à saúde e à "
  "segurança do paciente e da equipe. A clínica compromete-se a manter-se "
  "permanentemente atualizada quanto às alterações legislativas, revisando este "
  "Regimento Interno sempre que houver modificação relevante no arcabouço "
  "normativo aplicável.")
p("Observação: a Resolução CFF nº 573/2013, anteriormente utilizada como "
  "referência em documentos semelhantes, teve a sua eficácia suspensa por "
  "decisão judicial; por essa razão, este Regimento não a adota como fundamento, "
  "amparando a atuação do farmacêutico em saúde estética exclusivamente nas "
  "normas atualmente vigentes acima indicadas.", italic=True, size=10,
  color=CINZA)

# ===========================================================================
# 3. DADOS DA EMPRESA
# ===========================================================================
h1("3. Dados da Empresa")
p("A seguir são apresentados os dados cadastrais e de identificação do "
  "estabelecimento, que devem ser mantidos permanentemente atualizados e em "
  "consonância com os registros oficiais da empresa e com as licenças e alvarás "
  "em vigor:")
dt = doc.add_table(rows=0, cols=2); dt.style = "Table Grid"
dados = [
    ("Razão Social", RAZAO_SOCIAL),
    ("Nome Fantasia", NOME_FANTASIA),
    ("CNPJ", CNPJ),
    ("Endereço", ENDERECO),
    ("Atividade", "Clínica de saúde estética"),
    ("Responsável Técnica", f"{RT_NOME} – {RT_TITULO}"),
    ("Horário de funcionamento", HORARIO),
    ("Contato / telefone", "+55 67 99968-0240"),
]
for k, v in dados:
    row = dt.add_row().cells
    rr = row[0].paragraphs[0].add_run(k); rr.bold = True
    shade(row[0], "EAEFF5"); row[1].text = v
p("Os dados acima integram o cadastro do estabelecimento junto aos órgãos "
  "competentes e devem ser revistos sempre que houver alteração contratual, "
  "mudança de endereço, substituição da Responsável Técnica ou modificação do "
  "escopo das atividades, garantindo-se a fidedignidade das informações "
  "prestadas à Vigilância Sanitária.", size=10, color=CINZA)

# ===========================================================================
# 4. ORGANOGRAMA
# ===========================================================================
h1("4. Organograma")
p("A estrutura hierárquica da clínica está representada no organograma "
  "funcional a seguir, que evidencia as linhas de autoridade, de subordinação e "
  "de comunicação entre os diferentes níveis do estabelecimento. O organograma "
  "traduz, de forma gráfica, a organização adotada e serve de referência para a "
  "compreensão das relações de responsabilidade e para a definição dos fluxos de "
  "decisão internos:")
_org = achar(["organograma*", "*organograma*"])
if _org:
    pic = doc.add_paragraph(); pic.alignment = C
    pic.add_run().add_picture(_org, width=Cm(15.5))
    print("Organograma embutido:", _org)
else:
    p("Sócios-administradores (Ribeiro e Gonçalves Ltda.)", bold=True, align=C, color=AZUL, space_after=0)
    p("│", align=C, space_after=0)
    p(f"Responsável Técnica – {RT_NOME}", bold=True, align=C, color=AZUL, space_after=0)
    p("Recepção / Administrativo        |        Equipe de Apoio", align=C, space_after=0)
    print("Organograma -> texto (imagem nao encontrada)")
p("No topo da estrutura situam-se os sócios-administradores, responsáveis pela "
  "direção geral do negócio; a eles subordina-se, no plano técnico-sanitário, a "
  "Responsável Técnica, à qual compete a supervisão de toda a atividade "
  "assistencial e da equipe operacional, composta pela recepção/administrativo e "
  "pela equipe de apoio. Essa disposição assegura que todas as decisões de "
  "natureza técnica e sanitária estejam sob a coordenação de profissional "
  "legalmente habilitado.", size=10, color=CINZA)

# ===========================================================================
# 5. ESTRUTURA ORGANIZACIONAL
# ===========================================================================
h1("5. Estrutura Organizacional")
p("A clínica organiza-se em níveis funcionais integrados e complementares, cada "
  "qual com atribuições próprias, porém articuladas entre si, de modo a "
  "assegurar a continuidade e a qualidade do atendimento. A descrição de cada "
  "nível a seguir delimita o seu papel dentro da organização:")
h2("Direção (sócios-administradores)")
p("Constitui a instância máxima de decisão da clínica, responsável pela gestão "
  "administrativa, financeira e estratégica, pela definição e aprovação das "
  "políticas internas, pela alocação de recursos e pela garantia das condições "
  "materiais e humanas necessárias ao pleno funcionamento do estabelecimento em "
  "conformidade com a legislação. Cabe à Direção, ainda, deliberar sobre os "
  "casos omissos deste Regimento, ouvida a Responsável Técnica.")
h2("Responsabilidade Técnica")
p("Exercida por profissional legalmente habilitado, é responsável pela "
  "supervisão de todos os procedimentos técnicos e assistenciais, pela garantia "
  "do cumprimento das normas sanitárias e de biossegurança, pela elaboração e "
  "atualização dos Procedimentos Operacionais Padrão e pela coordenação, "
  "capacitação e avaliação da equipe. Representa a clínica perante a Vigilância "
  "Sanitária e os conselhos profissionais no âmbito de sua competência.")
h2("Setor administrativo / recepção")
p("Responsável pelo acolhimento e atendimento ao público, pelo agendamento e "
  "confirmação de procedimentos, pelo cadastro de pacientes, pela organização e "
  "guarda dos prontuários e da documentação, pelo controle da agenda e pelo "
  "apoio operacional às demais atividades, sempre com observância do sigilo e da "
  "proteção dos dados dos pacientes.")
h2("Setor de apoio")
p("Responsável pelo suporte à execução dos procedimentos, pela limpeza, "
  "higienização e organização dos ambientes, pelo apoio ao manejo dos materiais "
  "e resíduos e pela manutenção das condições gerais de conservação e ordem do "
  "estabelecimento, em conformidade com os padrões de biossegurança.")

# ===========================================================================
# 6. MISSÃO, VISÃO E VALORES
# ===========================================================================
h1("6. Missão, Visão e Valores")
h2("Missão")
p("Promover saúde, bem-estar e autoestima por meio de procedimentos estéticos "
  "seguros, éticos e de qualidade, prestados com atendimento humanizado, "
  "responsabilidade técnica e respeito integral à individualidade, às "
  "expectativas e à segurança de cada paciente.")
h2("Visão")
p("Ser reconhecida como referência em saúde estética na região de Dourados-MS, "
  "destacando-se pela excelência técnica, pela segurança e pela ética de seus "
  "procedimentos, pela constante atualização profissional e pela relação de "
  "confiança e credibilidade construída com seus pacientes.")
h2("Valores")
p("Os valores a seguir orientam a conduta cotidiana da clínica e de todos os "
  "seus colaboradores:")
vals = [
    ("Ética e responsabilidade profissional: ", "atuação pautada pela honestidade, pela transparência e pelo estrito respeito aos limites legais e técnicos de cada profissão."),
    ("Segurança do paciente: ", "prioridade absoluta à prevenção de riscos e à proteção da integridade física e da saúde de quem confia seus cuidados à clínica."),
    ("Qualidade e melhoria contínua: ", "compromisso permanente com a padronização, a avaliação e o aperfeiçoamento dos processos e dos resultados."),
    ("Respeito e atendimento humanizado: ", "acolhimento cordial, escuta atenta e tratamento digno e individualizado a cada pessoa atendida."),
    ("Sigilo e proteção de dados: ", "guarda rigorosa das informações e dos dados pessoais e de saúde dos pacientes, em conformidade com a legislação."),
    ("Cumprimento das normas sanitárias: ", "observância integral e permanente das exigências legais e regulamentares aplicáveis ao serviço."),
]
for lead, txt in vals:
    bullet(txt, bold_lead=lead)

# ===========================================================================
# 7. POLÍTICA DA QUALIDADE
# ===========================================================================
h1("7. Política da Qualidade")
p(f"A {NOME_FANTASIA} assume o compromisso de prestar serviços de saúde estética "
  "com segurança, eficácia e qualidade, em plena conformidade com as normas "
  "sanitárias vigentes e com as legítimas expectativas de seus pacientes. Essa "
  "política é entendida como um compromisso permanente da Direção e de toda a "
  "equipe, e não como uma meta pontual, materializando-se por meio das seguintes "
  "diretrizes:")
qual = [
    ("padronização das atividades ", "por meio da elaboração, da implantação e da revisão periódica de Procedimentos Operacionais Padrão (POPs), que descrevem detalhadamente cada rotina técnica e administrativa;"),
    ("capacitação contínua da equipe, ", "com treinamentos regulares e atualização técnica constante dos profissionais;"),
    ("controle e rastreabilidade ", "de produtos, materiais e equipamentos, com registro de lotes, validades e manutenções;"),
    ("monitoramento da satisfação e da segurança ", "dos pacientes, com registro e tratamento de manifestações, sugestões e eventuais intercorrências;"),
    ("avaliação periódica dos processos ", "por meio de auditorias internas e de indicadores que permitam identificar oportunidades de melhoria;"),
    ("melhoria contínua ", "dos serviços prestados, com base no ciclo de planejar, executar, verificar e agir (PDCA), promovendo a correção de desvios e o aperfeiçoamento constante."),
]
for lead, txt in qual:
    bullet(txt, bold_lead=lead)
p("A Política da Qualidade é comunicada a todos os colaboradores e deve ser "
  "compreendida, assumida e praticada por cada integrante da equipe, "
  "independentemente de sua função, como responsabilidade compartilhada.")

# ===========================================================================
# 8. ESTRUTURA FÍSICA
# ===========================================================================
h1("8. Estrutura Física da Clínica")
p("A clínica dispõe de instalações físicas projetadas e dimensionadas em "
  "conformidade com a RDC ANVISA nº 50/2002 e com as demais normas sanitárias "
  "aplicáveis, de modo a assegurar fluxos adequados de pessoas e materiais, "
  "conforto, privacidade e segurança nos atendimentos. Os ambientes são "
  "concebidos para permitir a separação entre áreas limpas e áreas "
  "potencialmente contaminadas, evitando cruzamentos indevidos e favorecendo a "
  "higienização. A estrutura contempla, no mínimo, os seguintes ambientes:")
amb = [
    ("recepção e sala de espera, ", "destinadas ao acolhimento, ao cadastro e à permanência confortável dos pacientes antes do atendimento;"),
    ("sala(s) de procedimentos estéticos, ", "com superfícies laváveis, lisas, impermeáveis e de fácil higienização, dotadas de mobiliário adequado e privacidade para a realização dos procedimentos;"),
    ("área ou local para o processamento e a esterilização de materiais, ", "com organização que separe o material sujo do material limpo e esterilizado;"),
    ("local para a guarda de produtos e materiais (estoque), ", "protegido de luz, calor e umidade, com controle de validade;"),
    ("sanitário(s), ", "em condições adequadas de higiene e conservação, dotados de insumos para a higienização das mãos;"),
    ("abrigo ou local de armazenamento temporário dos resíduos de serviços de saúde, ", "identificado e de acesso restrito, conforme o PGRSS;"),
    ("depósito de material de limpeza (DML), ", "destinado à guarda dos saneantes e utensílios de higienização."),
]
for lead, txt in amb:
    bullet(txt, bold_lead=lead)
p("Todos os ambientes são mantidos em adequado estado de conservação, limpeza, "
  "ventilação e iluminação, com mobiliário, revestimentos e instalações "
  "compatíveis com a atividade assistencial. A clínica zela, ainda, pelas "
  "condições de acessibilidade e pela sinalização adequada dos ambientes, "
  "promovendo a manutenção preventiva e corretiva das instalações sempre que "
  "necessário.")

# ===========================================================================
# 9. ATIVIDADES TÉCNICAS
# ===========================================================================
h1("9. Descrição Detalhada das Atividades Técnicas")
p("As atividades técnicas compreendem o conjunto de procedimentos estéticos "
  "executados ou supervisionados pela Responsável Técnica, sempre precedidos de "
  "avaliação individualizada do paciente, de verificação de indicações e "
  "contraindicações, de esclarecimento e obtenção de consentimento e de "
  "observância rigorosa da técnica asséptica e das boas práticas sanitárias. "
  "Todos os procedimentos são registrados em prontuário e realizados com "
  "produtos e materiais regularizados junto à ANVISA, respeitando-se os limites "
  "legais de atuação de cada profissional. São realizados na clínica, "
  "exclusivamente, os seguintes procedimentos:")
proc = [
    ("Limpeza de pele com extração",
     "consiste na higienização profunda da pele, com remoção de comedões, "
     "impurezas e células mortas, por meio de etapas de higienização, "
     "esfoliação, emolência, extração manual ou instrumental e aplicação de "
     "ativos e produtos calmantes e finalizadores. O procedimento é realizado "
     "com assepsia da área a ser tratada, com utilização de materiais "
     "esterilizados ou descartáveis de uso único e com orientação do paciente "
     "quanto aos cuidados posteriores, especialmente a fotoproteção. A avaliação "
     "prévia da pele orienta a intensidade e as etapas adotadas em cada caso."),
    ("Microagulhamento",
     "técnica de indução percutânea de colágeno realizada por meio de "
     "microagulhas que promovem microlesões controladas na pele, estimulando os "
     "processos naturais de reparação e a produção de colágeno. Exige "
     "antissepsia rigorosa da área, utilização de dispositivo e ponteiras "
     "estéreis e descartáveis de uso único, técnica asséptica durante toda a "
     "execução e descarte imediato e seguro dos perfurocortantes em coletor "
     "rígido apropriado. O paciente recebe orientações específicas de cuidados "
     "pós-procedimento, incluindo higienização, hidratação e fotoproteção."),
    ("Peelings químicos",
     "consistem na aplicação controlada de agentes químicos sobre a pele com a "
     "finalidade de promover a renovação celular e a esfoliação em diferentes "
     "profundidades, conforme o ativo e a concentração empregados. São "
     "precedidos de avaliação do fototipo, da indicação e de eventuais "
     "contraindicações, com controle rigoroso do tempo de ação, observação da "
     "resposta da pele e neutralização quando aplicável. Ao final, o paciente é "
     "orientado quanto aos cuidados pós-procedimento e à fotoproteção, "
     "essenciais à segurança e ao resultado do tratamento."),
    ("Aplicação de toxina botulínica",
     "procedimento injetável destinado ao relaxamento temporário da musculatura, "
     "realizado conforme avaliação individualizada, indicação técnica e "
     "legislação vigente. É executado com técnica asséptica, antissepsia da "
     "pele, utilização de produto regularizado com controle de lote e validade, "
     "reconstituição adequada, registro completo em prontuário e descarte "
     "imediato dos perfurocortantes em coletor apropriado. O paciente é "
     "informado sobre as orientações pré e pós-procedimento e sobre os cuidados "
     "necessários nas horas subsequentes à aplicação."),
    ("Preenchimento facial",
     "procedimento injetável que utiliza produtos preenchedores com a finalidade "
     "de restaurar volumes, contornos e harmonia facial. É precedido de "
     "avaliação criteriosa, com observância das indicações e contraindicações, e "
     "executado com técnica asséptica, rastreabilidade do produto (registro de "
     "lote e validade), registro em prontuário e descarte adequado dos materiais "
     "perfurocortantes. O paciente recebe orientações detalhadas sobre os "
     "cuidados posteriores e sobre os sinais que demandam retorno à clínica."),
    ("Bioestimuladores faciais",
     "consistem na aplicação de substâncias bioestimuladoras de colágeno, que "
     "atuam estimulando a produção fisiológica de colágeno ao longo do tempo. O "
     "procedimento pressupõe avaliação prévia do paciente, reconstituição do "
     "produto conforme as instruções do fabricante, técnica asséptica e "
     "aplicação de acordo com a bula e a legislação aplicável, com registro em "
     "prontuário e controle de lote e validade. São fornecidas orientações "
     "específicas de cuidados pós-procedimento, incluindo, quando indicado, a "
     "realização de massagem na área tratada."),
    ("Eletroporação",
     "técnica não invasiva de introdução transdérmica de ativos por meio da "
     "aplicação de corrente elétrica, que promove a abertura temporária de "
     "canais na membrana celular, favorecendo a permeação dos princípios ativos. "
     "É realizada com higienização prévia da pele, com limpeza e desinfecção do "
     "equipamento e dos eletrodos entre os atendimentos e com utilização de "
     "produtos regularizados, observando-se a avaliação prévia do paciente e as "
     "orientações posteriores pertinentes."),
    ("Epilação",
     "procedimento destinado à remoção de pelos pelo método disponível na "
     "clínica, precedido de avaliação da área e da indicação. É executado com "
     "higienização e desinfecção adequadas dos equipamentos entre os "
     "atendimentos e com utilização de insumos descartáveis sempre que "
     "aplicável, observando-se os cuidados de assepsia e as orientações ao "
     "paciente quanto à preparação e aos cuidados posteriores, especialmente a "
     "fotoproteção da região tratada."),
    ("Tratamentos capilares",
     "compreendem procedimentos estéticos voltados ao couro cabeludo e aos fios, "
     "com o objetivo de promover a saúde, a higiene e a aparência capilar. São "
     "precedidos de avaliação do couro cabeludo e da indicação, com utilização "
     "de produtos regularizados e observância das técnicas adequadas e das "
     "condições de higiene, sendo o paciente orientado quanto aos cuidados de "
     "manutenção recomendados."),
]
for nome, desc in proc:
    h2(nome)
    p(desc)
p("Independentemente do procedimento, são observados de forma sistemática: a "
  "avaliação prévia e a anamnese do paciente; o preenchimento e a assinatura do "
  "Termo de Consentimento Livre e Esclarecido (TCLE), quando aplicável; o "
  "registro completo em prontuário; a utilização de produtos regularizados na "
  "ANVISA, com controle de lote e validade; a adoção de técnica asséptica; o "
  "descarte adequado de resíduos e perfurocortantes; e o respeito rigoroso aos "
  "limites legais de atuação de cada profissional, sob supervisão da "
  "Responsável Técnica.")

# ===========================================================================
# 10. ATIVIDADES ADMINISTRATIVAS
# ===========================================================================
h1("10. Descrição das Atividades Administrativas")
p("As atividades administrativas constituem o conjunto de rotinas de suporte "
  "indispensáveis ao funcionamento regular e organizado da clínica, garantindo o "
  "adequado fluxo de informações, o controle documental e a sustentação "
  "operacional dos serviços assistenciais. Compreendem, entre outras, as "
  "seguintes tarefas:")
adm = [
    ("agendamento e confirmação ", "de consultas e procedimentos, com organização racional da agenda e comunicação prévia ao paciente;"),
    ("cadastro de pacientes ", "e abertura, organização e atualização dos respectivos prontuários;"),
    ("controle de documentos, ", "contratos, arquivos e registros da clínica, físicos e digitais;"),
    ("controle de estoque ", "de produtos e materiais, com acompanhamento de entradas, saídas, lotes e validades;"),
    ("gestão financeira ", "e de pagamentos, incluindo faturamento e controle de recebimentos;"),
    ("guarda e manutenção ", "das licenças, alvarás, documentos legais e comprovantes exigidos pelos órgãos de fiscalização;"),
    ("atendimento ao público ", "e gestão da comunicação com pacientes e fornecedores;"),
    ("apoio ao cumprimento ", "das obrigações sanitárias, fiscais e trabalhistas do estabelecimento."),
]
for lead, txt in adm:
    bullet(txt, bold_lead=lead)
p("O desempenho dessas atividades observa, em todas as etapas, o dever de sigilo "
  "e a proteção dos dados pessoais dos pacientes, nos termos da legislação "
  "aplicável.")

# ===========================================================================
# 11. ATIVIDADES ASSISTENCIAIS
# ===========================================================================
h1("11. Descrição das Atividades Assistenciais")
p("As atividades assistenciais referem-se ao cuidado direto prestado ao "
  "paciente, desde o seu acolhimento até o acompanhamento posterior ao "
  "procedimento, e representam o núcleo da atuação da clínica. Compreendem as "
  "seguintes etapas:")
ass = [
    ("acolhimento e recepção ", "do paciente, com atendimento cordial e identificação correta;"),
    ("avaliação inicial e anamnese estética, ", "com levantamento do histórico, das expectativas, das indicações e das contraindicações;"),
    ("orientação ", "sobre o procedimento indicado, seus benefícios, riscos, limitações e cuidados prévios e posteriores;"),
    ("obtenção do consentimento informado, ", "assegurando que o paciente compreenda e concorde com o procedimento;"),
    ("execução e acompanhamento ", "do procedimento, com observância das boas práticas e da segurança do paciente;"),
    ("orientações pós-procedimento ", "e agendamento de retornos e reavaliações;"),
    ("registro completo ", "de todas as etapas no prontuário do paciente, assegurando a rastreabilidade do cuidado."),
]
for lead, txt in ass:
    bullet(txt, bold_lead=lead)

# ===========================================================================
# 12. COMPETÊNCIAS DA RT
# ===========================================================================
h1("12. Competências da Responsável Técnica")
p(f"A Responsável Técnica, {RT_NOME} ({RT_TITULO}), é a profissional legalmente "
  "habilitada responsável pela condução técnica e sanitária da clínica, "
  "competindo-lhe, entre outras atribuições:")
rt = [
    "responder tecnicamente pela clínica perante a Vigilância Sanitária, os conselhos profissionais e os demais órgãos de fiscalização;",
    "supervisionar todos os procedimentos técnicos e assistenciais realizados no estabelecimento, zelando por sua correta execução;",
    "elaborar, revisar, implantar e fazer cumprir os Procedimentos Operacionais Padrão (POPs) e os demais documentos técnicos;",
    "garantir o cumprimento das normas sanitárias, de biossegurança e de boas práticas em todas as atividades;",
    "assegurar a regularidade, o controle de lote e a validade dos produtos, materiais e insumos utilizados;",
    "coordenar o gerenciamento dos resíduos de serviços de saúde (PGRSS) e o processamento dos materiais;",
    "treinar, orientar, supervisionar e avaliar continuamente a equipe;",
    "controlar a documentação técnica e os registros em prontuário, zelando por sua completude e guarda;",
    "zelar pela segurança do paciente e pela qualidade e humanização dos atendimentos;",
    "adotar as providências cabíveis diante de intercorrências, eventos adversos e não conformidades;",
    "atuar estritamente dentro dos limites legais de sua habilitação profissional.",
]
for x in rt:
    bullet(x)

# ===========================================================================
# 13. COMPETÊNCIAS DA RECEPÇÃO
# ===========================================================================
h1("13. Competências da Recepcionista")
p(f"A colaboradora {RECEP_NOME}, responsável pela recepção e pelo apoio "
  "administrativo, desempenha papel essencial no acolhimento do paciente e na "
  "organização das rotinas administrativas, competindo-lhe:")
rec = [
    "realizar agendamentos, confirmações e o atendimento cordial ao público, presencial e por meios de comunicação;",
    "efetuar o cadastro dos pacientes e organizar e manter atualizados os prontuários;",
    "prestar apoio administrativo e organizar a documentação e os arquivos da clínica;",
    "controlar a agenda e o fluxo de atendimento, otimizando os horários e evitando sobreposições;",
    "manter rigoroso sigilo e assegurar a proteção dos dados pessoais dos pacientes, em conformidade com a LGPD;",
    "apoiar o controle de estoque e a recepção e a conferência de mercadorias;",
    "zelar pela organização, pela limpeza e pela boa apresentação dos ambientes de recepção e espera.",
]
for x in rec:
    bullet(x)

# ===========================================================================
# 14. COMPETÊNCIAS DA EQUIPE DE APOIO
# ===========================================================================
h1("14. Competências da Equipe de Apoio")
p("A equipe de apoio é responsável pelas atividades de suporte que garantem as "
  "condições de higiene, ordem e funcionamento do estabelecimento, "
  "competindo-lhe:")
apo = [
    "executar a limpeza, a higienização e a desinfecção dos ambientes e superfícies conforme os Procedimentos Operacionais Padrão;",
    "apoiar a organização, a reposição e a guarda dos materiais e insumos;",
    "auxiliar no manejo, na segregação e no acondicionamento adequado dos resíduos, conforme o PGRSS;",
    "comunicar imediatamente à Responsável Técnica qualquer não conformidade, avaria ou situação de risco observada;",
    "cumprir as normas de biossegurança e utilizar corretamente os Equipamentos de Proteção Individual (EPIs) fornecidos.",
]
for x in apo:
    bullet(x)

# ===========================================================================
# 15. FLUXO DE ATENDIMENTO
# ===========================================================================
h1("15. Fluxo Completo de Atendimento ao Paciente")
p("O atendimento ao paciente segue um fluxo padronizado, concebido para "
  "assegurar organização, segurança e qualidade em todas as etapas, desde o "
  "primeiro contato até o acompanhamento dos resultados. As etapas do fluxo são "
  "as seguintes:")
fluxo = [
    "Agendamento e cadastro do paciente, com registro dos dados e da solicitação.",
    "Acolhimento na recepção e confirmação dos dados e do procedimento agendado.",
    "Avaliação e anamnese, com definição do procedimento pela Responsável Técnica.",
    "Orientação sobre o procedimento e assinatura do Termo de Consentimento Livre e Esclarecido (TCLE).",
    "Preparo do ambiente e dos materiais, com adoção de assepsia, EPIs e materiais esterilizados ou descartáveis.",
    "Execução do procedimento conforme o Procedimento Operacional Padrão correspondente.",
    "Registro completo do atendimento no prontuário do paciente.",
    "Orientações pós-procedimento e agendamento de retorno ou reavaliação.",
    "Descarte adequado dos resíduos e higienização e desinfecção do ambiente e dos materiais.",
    "Acompanhamento e avaliação dos resultados obtidos, com registro das ocorrências.",
]
for f in fluxo:
    num(f)
p("O cumprimento integral e ordenado dessas etapas é obrigatório e constitui "
  "instrumento de proteção tanto do paciente quanto da equipe e da clínica.")

# ===========================================================================
# 16. SEGURANÇA DO PACIENTE
# ===========================================================================
h1("16. Segurança do Paciente")
p("A segurança do paciente é prioridade absoluta e norteia todas as práticas da "
  "clínica. Com o objetivo de prevenir a ocorrência de danos evitáveis e de "
  "minimizar riscos, são adotadas, entre outras, as seguintes práticas:")
seg = [
    "identificação correta do paciente antes do início de cada procedimento;",
    "avaliação prévia de indicações, contraindicações, alergias e histórico de saúde relevante;",
    "utilização exclusiva de produtos regularizados, com controle de lote e validade;",
    "adoção de técnica asséptica e uso de materiais esterilizados ou descartáveis de uso único;",
    "registro fiel, completo e legível de todas as etapas no prontuário;",
    "fornecimento de orientações claras de pré e pós-procedimento, verbalmente e por escrito quando pertinente;",
    "definição de conduta para intercorrências, com encaminhamento a serviço de referência quando necessário;",
    "identificação, registro, tratamento e notificação de eventos adversos, com adoção de medidas preventivas.",
]
for x in seg:
    bullet(x)
p("A cultura de segurança é estimulada de forma contínua, incentivando-se a "
  "comunicação aberta de riscos e de quase-erros, sem caráter punitivo, como "
  "meio de aprendizado e de melhoria dos processos.")

# ===========================================================================
# 17. HUMANIZAÇÃO
# ===========================================================================
h1("17. Humanização do Atendimento")
p("O atendimento prestado pela clínica pauta-se pelo respeito, pela empatia e "
  "pela valorização da individualidade de cada paciente. Desde o acolhimento na "
  "recepção até o acompanhamento posterior, busca-se estabelecer uma relação de "
  "confiança, baseada na escuta atenta, na comunicação clara e acessível e no "
  "esclarecimento honesto quanto às possibilidades, aos limites e aos resultados "
  "esperados de cada procedimento.")
p("São assegurados a privacidade e o conforto do paciente durante os "
  "atendimentos, o respeito às suas expectativas e decisões e o tratamento "
  "digno, cordial e livre de qualquer forma de discriminação. A humanização é "
  "compreendida não como uma etapa isolada, mas como um princípio que permeia "
  "todas as ações da equipe, contribuindo para uma experiência segura, "
  "acolhedora e positiva.")

# ===========================================================================
# 18. BIOSSEGURANÇA
# ===========================================================================
h1("18. Biossegurança")
p("A clínica observa rigorosamente as normas de biossegurança, com destaque "
  "para a NR-32 e para a legislação sanitária aplicável, com o objetivo de "
  "prevenir riscos biológicos, químicos e físicos à saúde da equipe e dos "
  "pacientes. Entre as medidas de biossegurança adotadas, destacam-se:")
bio = [
    "higienização das mãos antes e após cada atendimento e sempre que necessário, observando-se os momentos preconizados;",
    "utilização de Equipamentos de Proteção Individual adequados a cada procedimento;",
    "antissepsia da pele e adoção de técnica asséptica em todos os procedimentos que a exijam;",
    "uso de materiais esterilizados ou descartáveis de uso único;",
    "descarte imediato e seguro dos perfurocortantes em coletor rígido apropriado, sem reencape de agulhas;",
    "imunização da equipe conforme as recomendações aplicáveis, com destaque para a vacinação contra hepatite B;",
    "limpeza e desinfecção de superfícies, mobiliário e equipamentos entre os atendimentos.",
]
for x in bio:
    bullet(x)
p("Na hipótese de acidente com material biológico ou perfurocortante, são "
  "adotadas de imediato as medidas de primeiros cuidados e de notificação "
  "previstas em procedimento específico, com o devido acompanhamento do "
  "colaborador envolvido.")

# ===========================================================================
# 19. EPIs
# ===========================================================================
h1("19. Uso de EPIs")
p("Os Equipamentos de Proteção Individual (EPIs) são fornecidos gratuitamente "
  "pela clínica e o seu uso é obrigatório, nos termos da NR-6 e da NR-32, sempre "
  "que a natureza do procedimento assim o exigir. Conforme o risco envolvido, "
  "são utilizados, entre outros:")
epi = [
    ("luvas de procedimento e/ou estéreis, ", "para a proteção das mãos e a prevenção de contaminação cruzada;"),
    ("máscara facial, ", "para a proteção das vias respiratórias e a contenção de gotículas;"),
    ("óculos de proteção ou protetor facial, ", "quando houver risco de respingos, indicados conforme o procedimento;"),
    ("avental ou jaleco, ", "para a proteção do tronco e da vestimenta;"),
    ("touca ou gorro, ", "quando aplicável, para a contenção dos cabelos."),
]
for lead, txt in epi:
    bullet(txt, bold_lead=lead)
p("É expressamente vedada a reutilização de EPIs descartáveis. Os equipamentos "
  "são substituídos sempre que se apresentarem contaminados, úmidos ou "
  "danificados, e a equipe é orientada e treinada quanto ao uso correto, à "
  "colocação, à retirada e ao descarte adequado de cada item.")

# ===========================================================================
# 20. LIMPEZA, DESINFECÇÃO E ESTERILIZAÇÃO
# ===========================================================================
h1("20. Limpeza, Desinfecção e Esterilização")
p("O processamento dos produtos para a saúde utilizados na clínica observa a "
  "RDC ANVISA nº 15/2012 e Procedimento Operacional Padrão específico, "
  "considerando a classificação dos materiais em críticos, semicríticos e não "
  "críticos, conforme o risco de infecção associado ao seu uso. As etapas do "
  "processamento compreendem:")
est = [
    "limpeza dos materiais imediatamente após o uso, com remoção da sujidade visível;",
    "desinfecção de superfícies, mobiliário e equipamentos com saneantes regularizados e na concentração adequada;",
    "esterilização dos materiais críticos em autoclave, com controle dos parâmetros de cada ciclo;",
    "monitoramento do processo de esterilização por meio de indicadores físicos, químicos e biológicos;",
    "armazenamento adequado dos materiais esterilizados, protegidos e identificados com a respectiva data de validade da esterilização;",
    "priorização, sempre que possível, do uso de materiais descartáveis de uso único.",
]
for x in est:
    bullet(x)
p("Os registros do processamento e do monitoramento da esterilização são "
  "mantidos e arquivados, permitindo a rastreabilidade e a comprovação da "
  "eficácia do processo perante a fiscalização.")

# ===========================================================================
# 21. PGRSS
# ===========================================================================
h1("21. Gerenciamento de Resíduos (PGRSS)")
p("A clínica mantém e implementa Plano de Gerenciamento de Resíduos de Serviços "
  "de Saúde (PGRSS), em conformidade com a RDC ANVISA nº 222/2018, que disciplina "
  "todas as etapas de manejo dos resíduos gerados, desde a geração até a "
  "destinação final, contemplando a segregação, o acondicionamento, a "
  "identificação, o armazenamento, a coleta e a destinação ambientalmente "
  "adequada. Os resíduos são classificados e manejados conforme os respectivos "
  "grupos:")
grp = [
    ("Grupo A (potencialmente infectantes): ", "acondicionados em saco branco leitoso, devidamente identificado, e destinados a tratamento específico;"),
    ("Grupo B (químicos): ", "acondicionados de acordo com as suas características de risco e destinados conforme a legislação aplicável;"),
    ("Grupo D (comuns): ", "resíduos recicláveis e rejeitos não contaminados, equiparados aos resíduos domiciliares;"),
    ("Grupo E (perfurocortantes): ", "descartados em coletor rígido, resistente à punctura, sem reencape de agulhas e respeitado o limite de preenchimento."),
]
for lead, txt in grp:
    bullet(txt, bold_lead=lead)
p("Os resíduos são coletados por empresa devidamente licenciada, mantendo-se a "
  "guarda dos comprovantes de coleta, transporte e destinação final "
  "(manifestos). A equipe é capacitada quanto à correta segregação e ao manejo "
  "seguro dos resíduos, sob coordenação da Responsável Técnica.")

# ===========================================================================
# 22. ESTOQUE
# ===========================================================================
h1("22. Controle de Estoque")
p("O controle de estoque tem por finalidade assegurar a disponibilidade, a "
  "rastreabilidade e a qualidade dos produtos, materiais e insumos utilizados "
  "nos procedimentos, prevenindo o uso de itens vencidos, avariados ou "
  "irregulares. É realizado por meio de:")
estq = [
    "recebimento com conferência da nota fiscal, do lote, da validade e das condições de integridade dos produtos;",
    "armazenamento adequado, com controle de temperatura e proteção contra luz e umidade quando exigido;",
    "controle de validade com utilização prioritária dos lotes de vencimento mais próximo (sistema PEPS - primeiro que expira, primeiro que sai);",
    "registro organizado das entradas e saídas de produtos e materiais;",
    "aquisição exclusiva de produtos regularizados junto à ANVISA e de fornecedores idôneos;",
    "segregação, identificação e descarte adequado de produtos vencidos, avariados ou reprovados.",
]
for x in estq:
    bullet(x)

# ===========================================================================
# 23. EQUIPAMENTOS
# ===========================================================================
h1("23. Controle de Equipamentos e Manutenção")
p("Os equipamentos utilizados na clínica são mantidos em condições adequadas de "
  "uso, funcionamento e segurança, de forma a garantir a sua eficácia e a "
  "proteção do paciente e da equipe. O controle é realizado mediante:")
equi = [
    "cadastro e inventário atualizado dos equipamentos existentes;",
    "manutenção preventiva e corretiva, com registro das intervenções realizadas;",
    "calibração e aferição periódicas, quando aplicáveis ao tipo de equipamento;",
    "higienização e desinfecção entre os atendimentos, conforme Procedimento Operacional Padrão;",
    "guarda organizada dos manuais, das notas fiscais e dos comprovantes de manutenção e assistência técnica.",
]
for x in equi:
    bullet(x)

# ===========================================================================
# 24. CONTROLE DE DOCUMENTOS
# ===========================================================================
h1("24. Controle de Documentos")
p("A clínica mantém sistema de controle de seus documentos técnicos e legais — "
  "entre os quais o presente Regimento Interno, os Procedimentos Operacionais "
  "Padrão (POPs), o PGRSS, os manuais, os registros e as licenças — de modo a "
  "assegurar a sua integridade, a sua atualização e a sua disponibilidade. Para "
  "tanto, adota:")
docs = [
    "identificação de cada documento, com título, número de versão e data de vigência;",
    "aprovação formal por responsável competente antes de sua entrada em vigor;",
    "revisão periódica e sempre que houver mudança relevante na legislação, na estrutura ou nas atividades;",
    "guarda organizada e de fácil acesso, permitindo a pronta consulta pela equipe e pela fiscalização;",
    "retirada de circulação e identificação das versões obsoletas, evitando o seu uso indevido.",
]
for x in docs:
    bullet(x)

# ===========================================================================
# 25. SIGILO E LGPD
# ===========================================================================
h1("25. Sigilo Profissional e LGPD")
p("A clínica e todos os seus colaboradores comprometem-se com o dever de sigilo "
  "profissional e com a proteção dos dados pessoais dos pacientes, em especial "
  "dos dados de saúde, considerados dados sensíveis pela Lei nº 13.709/2018 "
  "(Lei Geral de Proteção de Dados Pessoais - LGPD). Para o cumprimento dessa "
  "obrigação, são observadas as seguintes medidas:")
lgpd = [
    "coleta de dados limitada ao estritamente necessário à finalidade do atendimento;",
    "informação ao paciente e obtenção de consentimento quanto ao tratamento de seus dados, quando exigido;",
    "guarda segura dos prontuários e documentos, físicos e digitais, com medidas de proteção contra acesso não autorizado, perda ou extravio;",
    "restrição do acesso aos dados apenas aos profissionais autorizados e no limite de suas atribuições;",
    "vedação absoluta à divulgação de imagens, informações ou dados de pacientes sem autorização expressa e específica;",
    "manutenção do dever de sigilo inclusive após o término do vínculo profissional ou empregatício.",
]
for x in lgpd:
    bullet(x)
p("Eventuais incidentes de segurança envolvendo dados pessoais são tratados com "
  "prioridade, adotando-se as medidas de contenção e de comunicação cabíveis, "
  "resguardados os direitos dos titulares.")

# ===========================================================================
# 26. TREINAMENTO
# ===========================================================================
h1("26. Treinamento da Equipe")
p("A clínica promove a capacitação e a educação permanente de sua equipe como "
  "instrumento essencial de qualidade e de segurança. O programa de treinamento "
  "contempla, entre outros:")
trein = [
    "treinamento de integração dos novos colaboradores, com apresentação do Regimento Interno e dos POPs;",
    "treinamento em biossegurança, uso de EPIs e higienização das mãos;",
    "capacitação quanto aos Procedimentos Operacionais Padrão e ao PGRSS;",
    "atualização técnica periódica, acompanhando a evolução das práticas e das normas;",
    "registro documentado dos treinamentos realizados, com data, conteúdo, carga horária e participantes.",
]
for x in trein:
    bullet(x)

# ===========================================================================
# 27. AUDITORIA INTERNA
# ===========================================================================
h1("27. Auditoria Interna")
p("A clínica realiza auditorias internas periódicas, sob a coordenação da "
  "Responsável Técnica, com o propósito de verificar a conformidade dos "
  "processos com este Regimento Interno, com os Procedimentos Operacionais "
  "Padrão e com a legislação sanitária, promovendo a melhoria contínua. As "
  "auditorias compreendem:")
aud = [
    "verificação do cumprimento das rotinas, das boas práticas e dos registros obrigatórios;",
    "identificação e documentação de não conformidades e de oportunidades de melhoria;",
    "definição de ações corretivas e preventivas, com indicação de responsáveis e de prazos;",
    "acompanhamento da implementação e da eficácia das medidas adotadas;",
    "registro e arquivamento dos resultados das auditorias e dos respectivos planos de ação.",
]
for x in aud:
    bullet(x)

# ===========================================================================
# 28. DISPOSIÇÕES FINAIS
# ===========================================================================
h1("28. Disposições Finais")
p("Este Regimento Interno entra em vigor na data de sua aprovação e permanece "
  "válido por prazo indeterminado, devendo ser revisado periodicamente e sempre "
  "que houver alteração relevante na legislação, na estrutura física, no quadro "
  "de pessoal ou nas atividades desenvolvidas pela clínica.")
p("O presente documento é complementado pelos Procedimentos Operacionais Padrão "
  "(POPs), pelo Plano de Gerenciamento de Resíduos de Serviços de Saúde (PGRSS) "
  "e pelos demais manuais, registros e documentos exigidos pela Vigilância "
  "Sanitária e pela legislação aplicável, os quais integram, para todos os fins, "
  "o sistema de gestão da clínica.")
p("Todos os colaboradores, independentemente do vínculo, devem conhecer, "
  "observar e cumprir integralmente as disposições deste Regimento, registrando "
  "a sua ciência conforme o termo constante da seção seguinte. Os casos omissos "
  "e as situações não expressamente previstas serão resolvidos pela Direção, "
  "ouvida a Responsável Técnica, sempre à luz da legislação vigente e do "
  "interesse da segurança do paciente.")

# ===========================================================================
# 29. TERMO DE CIÊNCIA
# ===========================================================================
page_break()
h1("29. Termo de Ciência dos Colaboradores")
p("Declaro, para os devidos fins, que recebi, li, compreendi e concordo com o "
  f"Regimento Interno da {NOME_FANTASIA} ({RAZAO_SOCIAL}), comprometendo-me a "
  "cumprir integralmente as suas disposições, bem como as normas sanitárias, de "
  "biossegurança, de sigilo e de proteção de dados nele previstas, no exercício "
  "das minhas funções.")
doc.add_paragraph()
tc = doc.add_table(rows=1, cols=4); tc.style = "Table Grid"
for i, t in enumerate(["Nome completo", "Função", "Data", "Assinatura"]):
    c = tc.rows[0].cells[i]
    rr = c.paragraphs[0].add_run(t); rr.bold = True
    rr.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); shade(c, "1F3A5F")
for _ in range(10):
    r = tc.add_row().cells
    for c in r:
        c.paragraphs[0].add_run("\n")
doc.add_paragraph()
p("____________________________________", align=C, space_after=0)
p(RT_NOME, bold=True, align=C, space_after=0)
p(f"Responsável Técnica – {RT_TITULO}", size=10, color=CINZA, align=C)

# ---------------------------------------------------------------------------
OUT = "regimento_neuderme/Regimento Interno - NEWDERM - Minuta v02.docx"
doc.save(OUT)
print("OK ->", OUT)
