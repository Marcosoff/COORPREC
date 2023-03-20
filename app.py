import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe
from PIL import Image
import pandas as pd
import re
import time

st.set_page_config(layout="centered", page_icon="⚖", page_title="Tribunal de Justiça do MA")
image = Image.open('logoTJMA.jpg')
st.image(image)
st.title("⚖ Tribunal de Justiça do MA")
st.write("Emissão de comprovante DIRF 2023.")

st.write(
    "Este App emite o comprovante de rendimentos referente ao recebimento de até 1 precatório no ano de 2022. Caso tenha recebido mais de um pagamento, por favor entrar em contato com a Coordenadoria de Precatórios. Fone: (98) 3261-6237."
)

left, right = st.columns(2)

right.write("Este é o modelo que será emitido:")

right.image("Comprovante de rendimentos DIRF2023_2.png", width=300)

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("Comprovante de rendimentos DIRF2023.html")


left.write("Informe os Dados:")
form = left.form("template_form")
CPF = form.text_input("CPF (sem pontos):", max_chars=11)
#student = form.text_input("Nome Completo:")
cpfPontuado = re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', CPF)

#grade = 'R$ 1.000.000,00'

submit = form.form_submit_button("Generate PDF")

DIRF2023 = pd.read_excel('DIRF2023.xlsx', dtype=str)

DIRF2023['VALOR'] = DIRF2023['VALOR'].astype(str)
#DIRF2023['VALOR'] = DIRF2023['VALOR'].str.replace('.', ',')
DIRF2023['PREVIDENCIA'] = DIRF2023['PREVIDENCIA'].astype(str)
DIRF2023['PREVIDENCIA'] = DIRF2023['PREVIDENCIA'].str.replace('.', ',')
DIRF2023['IR'] = DIRF2023['IR'].astype(str)
DIRF2023['IR'] = DIRF2023['IR'].str.replace('.', ',')
DIRF2023['QTD_MESES'] = DIRF2023['QTD_MESES'].astype(str)
DIRF2023['PROCESSO'] = DIRF2023['PROCESSO'].astype(str)
DIRF2023['PROCESSO'] = DIRF2023['PROCESSO'].str.replace(',', '.')


#CPF2 = {'CPF':{},'VALOR':{},'PREVIDENCIA':{},'IR':{}}
#CPF3 = pd.DataFrame(CPF2)
#TABELA = pd.merge(CPF3, DIRF2023, left_on=['CPF','VALOR'], right_on=['CPF','VALOR'], how='right')
#grade = DIRF2023.loc[DIRF2023.CPF == course,'VALOR'].values
#grade = DIRF2023.loc[DIRF2023['CPF'] == CPF,'VALOR'].values
#DIRF2023 = DIRF2023.set_index('CPF')
#DIRF2023.index.names = [None]
grade = DIRF2023.loc[DIRF2023['CPF'] == CPF,'VALOR'].values
student = DIRF2023.loc[DIRF2023['CPF_N_DUPLICADO'] == CPF,'NOME_N_DUPLICADO'].values
QTD_MESES = DIRF2023.loc[DIRF2023['CPF'] == CPF,'QTD_MESES'].values
PROCESSO = DIRF2023.loc[DIRF2023['CPF'] == CPF,'PROCESSO'].values
VALOR = DIRF2023.loc[DIRF2023['CPF'] == CPF,'VALOR'].values
PREVIDENCIA = DIRF2023.loc[DIRF2023['CPF'] == CPF,'PREVIDENCIA'].values
IR = DIRF2023.loc[DIRF2023['CPF'] == CPF,'IR'].values

#grade = re.search('02439232360', grade.decode('utf-8'))
#grade = grade.encode(encoding='utf-8')

#grade = re.sub("\[|\'|\]","",grade)

characters = "'[]"

grade = ''.join( x for x in grade if x not in characters)
student = ''.join( x for x in student if x not in characters)
#QTD_MESES =  ''.join( x for x in QTD_MESES if x not in characters)
#PROCESSO =  ''.join( x for x in PROCESSO if x not in characters)





try:
	if submit:
		PROCESSO = PROCESSO[0]
		QTD_MESES = QTD_MESES[0]
		VALOR = VALOR[0]
		PREVIDENCIA = PREVIDENCIA[0]
		IR = IR[0]
		VALOR = float(VALOR)
		VALOR = round(VALOR,2)
		VALOR = str(VALOR).replace('.', ',')
		html = template.render(
		course=cpfPontuado,
		student=student,
		date=date.today().strftime("%d / %m / %Y"),
		grade=grade,
		PROCESSO=PROCESSO,
		QTD_MESES=QTD_MESES,
    		VALOR=VALOR,
		PREVIDENCIA=PREVIDENCIA,
    		IR=IR
		)

		pdf = pdfkit.from_string(html, False)
		st.balloons()

		right.success("⚖ Comprovante Emitido com Sucesso!")
		right.download_button("⬇️ Download PDF",data=pdf,file_name="Comprovante de Rendimentos.pdf",mime="application/octet-stream")


except IndexError:
	right.write("CPF não encontrado! Entre em contato com a Coordenadoria de Precatórios. Fone:(98) 3261-6237.")

