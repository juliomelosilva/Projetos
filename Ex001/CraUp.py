from PySimpleGUI import PySimpleGUI as sg
import pyautogui
import time
import os



sg.theme('DarkBlack')
        #layout
layout = [
            [sg.Text('''Este é um controlador
Para Dofus''')],[sg.Button('Iniciar')], [sg.Button('Parar')]
        ]
        #janela 
janela = sg.Window('.....................').layout(layout)
        #Ler eventos
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    if eventos == 'Parar':
        break
    if eventos == 'Iniciar':
        while True:
            time.sleep(3)
            #falar com npc fora do troll
            pyautogui.moveTo(377, 278, duration=0.2)
            pyautogui.click(button='left')
            time.sleep(2)
            pyautogui.moveTo(240, 665, duration=0.2)
            pyautogui.click(button='left')
            time.sleep(2)
            pyautogui.moveTo(399, 669, duration=0.2)
            pyautogui.click(button='left')
            time.sleep(5)
            #falar com o npc dentro da toca
            pyautogui.moveTo(873, 242, duration=0.2)
            pyautogui.click(button='left')
            time.sleep(2)
            pyautogui.moveTo(421, 664, duration=0.2)
            pyautogui.click(button='left')
            time.sleep(2)
            #iniciar a luta (Botão de "pronto")
            pyautogui.moveTo(1039, 691, duration=0.2)
            pyautogui.click(button='left')
            time.sleep(3)
            #andar 1pm
            pyautogui.moveTo(455, 391, duration=0.2)
            pyautogui.doubleClick(button='left')
            time.sleep(2)
            #Sequência de ataques primeiro turno
            #flecha perfurante
            pyautogui.moveTo(1101, 192, duration=0.2)
            pyautogui.click(button='left')
            #time.sleep(2)
            #atacar troll
            pyautogui.moveTo(957, 681, duration=0.2)
            pyautogui.click(button='left')
            #time.sleep(2)
            #flecha de abolição 
            pyautogui.moveTo(1105, 226, duration=0.2)
            pyautogui.click(button='left')
            #time.sleep(2)
            #atacar troll
            pyautogui.moveTo(957, 681, duration=0.2)
            pyautogui.click(button='left')
            #time.sleep(2)
            #flecha de abolição
            pyautogui.moveTo(1105, 226, duration=0.2)
            pyautogui.click(button='left')
            #time.sleep(2)
            #atacar troll
            pyautogui.moveTo(957, 681, duration=0.2)
            pyautogui.click(button='left')
            #time.sleep(2)
            #passar o turno (mesma posição do "pronto")
            pyautogui.moveTo(1039, 691, duration=0.2)
            pyautogui.click(button='left')
            time.sleep(7)
            #andar +1 pm
            pyautogui.moveTo(491, 402, duration=0.2)
            pyautogui.doubleClick(button='left')
            time.sleep(1)
            #Sequência de ataques segundo turno
            #flecha perfurante
            pyautogui.moveTo(1101, 192, duration=0.2)
            pyautogui.click(button='left')
            #time.sleep(2)
            #atacar troll
            pyautogui.moveTo(957, 681, duration=0.2)
            pyautogui.click(button='left')
            #time.sleep(2)
            #flecha de abolição
            pyautogui.moveTo(1105, 226, duration=0.2)
            pyautogui.click(button='left')
            #time.sleep(2)
            #atacar troll
            pyautogui.moveTo(957, 681, duration=0.2)
            pyautogui.click(button='left')
            #time.sleep(2)
            #flecha Flamejante
            pyautogui.moveTo(1111, 277, duration=0.2)
            pyautogui.click(button='left')
            #time.sleep(2)
            #atacar troll
            pyautogui.moveTo(957, 681, duration=0.2)
            pyautogui.click(button='left')
            #passar turno (mesma posição do "pronto")
            pyautogui.moveTo(1039, 691, duration=0.2)
            pyautogui.click(button='left')
            time.sleep(7)
            #fechar janela de luta
            pyautogui.moveTo(1080, 230, duration=0.2)
            pyautogui.click(button='left')
            #time.sleep(3)

            

            
            
            

            
