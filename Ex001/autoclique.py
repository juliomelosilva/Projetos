import openpyxl
import time
import os
import pyautogui
import webbrowser

workbook = openpyxl.load_workbook("C:\\Users\\jean_\\OneDrive\\Área de Trabalho\\Chamados_Plantao.xlsx")
chamados = workbook['Planilha1']
webbrowser.open('https://smliveloja.bitrix24.site/plantao/')
time.sleep(2)
for linha in chamados.iter_rows(min_row=2):
    Nome = linha[0].value
    Descricao = linha[1].value
    Resolucao = linha[2].value
    print(Nome)
    print(Descricao)
    print(Resolucao)