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
pyautogui.PAUSE=0.3
time.sleep(2)
#insere meu nome
pyautogui.click(x=495, y=336)
pyautogui.write('Julio')

time.sleep(2)
#clica na data
pyautogui.click(x=514, y=400)
pyautogui.click(x=457, y=678) #posição da data
time.sleep(2)
pyautogui.click(x=530, y=477) #posicao nome da empresa
time.sleep(1)
pyautogui.write(Nome)
time.sleep(2)
pyautogui.click(x=548, y=528) #posicao titulo
pyautogui.write(Descricao)
pyautogui.click(x=457, y=626) #posicao descricao
pyautogui.write(Descricao)
pyautogui.scroll(-500)
time.sleep(0.5)
pyautogui.click(x=448, y=374) #posicao resolucao
pyautogui.write(Resolucao)








    

    


