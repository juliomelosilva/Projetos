import openpyxl
import time
import os
import pyautogui
import webbrowser

workbook = openpyxl.load_workbook("C:\\Users\\Growth Live\\Documents\\DESKTOP\\Júlio\\Códigos\\HTML - CSS (Curso em Vídeo)\\M2\\Projetos\\Ex001\\chamados.xlsx")
chamados = workbook['Planilha1']
webbrowser.open('https://smliveloja.bitrix24.site/plantao/')
time.sleep(2)

while chamados != '':
            for linha in chamados.iter_rows(min_row=2):
                Nome = linha[0].value
                Descricao = linha[1].value
                Resolucao = linha[2].value

                pyautogui.PAUSE=0.3
                time.sleep(1)
                #insere meu nome
                pyautogui.click(x=495, y=336)
                pyautogui.write('Julio')

                time.sleep(0.5)
                #clica na data
                pyautogui.click(x=514, y=400)
                pyautogui.click(x=695, y=552) #posição da data
                time.sleep(0.5)
                pyautogui.click(x=530, y=477) #posicao nome da empresa
                pyautogui.write(Nome)
                time.sleep(0.5)
                pyautogui.click(x=548, y=528) #posicao titulo
                pyautogui.write(Descricao)
                pyautogui.click(x=457, y=626) #posicao descricao
                pyautogui.write(Descricao)
                pyautogui.scroll(-500)
                time.sleep(0.5)
                pyautogui.click(x=448, y=374) #posicao resolucao
                pyautogui.write(Resolucao)
                time.sleep(0.5)
                pyautogui.click(x=486, y=453) #posicao prioridade
                pyautogui.click(x=458, y=543) #selecao prioridade media
                time.sleep(0.5)
                pyautogui.click(x=586, y=516)#posicao Categoria
                time.sleep(1)
                pyautogui.moveTo(x=623, y=632, duration=0.1)
                pyautogui.scroll(-10000)
                pyautogui.moveTo(x=1084, y=610, duration=0.1)
                pyautogui.scroll(-1000)
                pyautogui.click(x=498, y=689) #categoria plantao
                #pyautogui.hotkey('f5')
                pyautogui.click(x=658, y=523) #botao enviar
                pyautogui.click(x=658, y=523) #botao enviar 2
                time.sleep(8)
                #pyautogui.scroll(50000)

        