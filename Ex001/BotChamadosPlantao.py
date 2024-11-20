import openpyxl
import time
import os
import pyautogui
import webbrowser
import keyboard
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

# Função para iniciar o processo de automação
def iniciar_automacao():
    definir_nome = nome_entry.get()

    if not definir_nome:
        messagebox.showerror("Erro", "Por favor, insira o nome a ser preenchido.")
        return

    arquivo_excel = filedialog.askopenfilename(title="Selecione o arquivo Excel", filetypes=[("Arquivos Excel", "*.xlsx")])

    if not arquivo_excel:
        messagebox.showerror("Erro", "Por favor, selecione um arquivo Excel.")
        return

    try:
        # Carrega o arquivo Excel
        workbook = openpyxl.load_workbook(arquivo_excel)
        chamados = workbook['Planilha1']

        # Abre o site no navegador
        webbrowser.open('https://smliveloja.bitrix24.site/plantao/')
        time.sleep(2)

        # Itera sobre as linhas da planilha, começando pela linha 2
        for linha in chamados.iter_rows(min_row=2):
            Nome = linha[0].value
            Descricao = linha[1].value
            Resolucao = linha[2].value

            # Verifica se a linha está vazia (caso todos os campos estejam vazios)
            if Nome is None and Descricao is None and Resolucao is None:
                print("Linha vazia encontrada. Encerrando o processo.")
                break

            # Automação com pyautogui
            pyautogui.PAUSE = 0.3
            time.sleep(1)

            pyautogui.click(x=495, y=336)  # Insere o nome do usuário
            keyboard.write(definir_nome)

            time.sleep(0.5)

            # Seleção automática da data
            dia_atual = datetime.now().day

            pyautogui.click(x=514, y=400)  # Posição para abrir o seletor de data
            time.sleep(0.5)

            # Calcula a posição relativa do dia no calendário
            base_x = 500  # Coordenada x base
            base_y = 600  # Coordenada y base
            offset_x = 30  # Distância horizontal entre os dias
            offset_y = 30  # Distância vertical entre as linhas de dias

            linha = (dia_atual - 1) // 7
            coluna = (dia_atual - 1) % 7

            dia_x = base_x + (coluna * offset_x)
            dia_y = base_y + (linha * offset_y)

            pyautogui.click(x=dia_x, y=dia_y)

            time.sleep(0.5)
            pyautogui.click(x=530, y=477)  # Posição nome da empresa
            keyboard.write(Nome)
            time.sleep(0.5)
            pyautogui.click(x=548, y=528)  # Posição título
            keyboard.write(Descricao)
            pyautogui.click(x=457, y=626)  # Posição descrição
            keyboard.write(Descricao)
            pyautogui.scroll(-500)
            time.sleep(0.5)
            pyautogui.click(x=448, y=374)  # Posição resolução
            keyboard.write(Resolucao)
            time.sleep(0.5)
            pyautogui.click(x=486, y=453)  # Posição prioridade
            pyautogui.click(x=458, y=543)  # Seleção prioridade média
            time.sleep(0.5)
            pyautogui.click(x=586, y=516)  # Posição categoria
            time.sleep(1)
            pyautogui.moveTo(x=623, y=632, duration=0.1)
            pyautogui.scroll(-10000)
            pyautogui.moveTo(x=1084, y=610, duration=0.1)
            pyautogui.scroll(-1000)
            pyautogui.click(x=498, y=689)  # Categoria plantão
            pyautogui.click(x=658, y=523)  # Botão enviar
            pyautogui.click(x=658, y=523)  # Botão enviar 2
            time.sleep(6)

        messagebox.showinfo("Concluído", "Automação concluída com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Configuração da interface gráfica
app = tk.Tk()
app.title("Automação de Chamados")
app.geometry("400x200")

# Label e campo de entrada para o nome
nome_label = tk.Label(app, text="Digite o nome a ser preenchido:")
nome_label.pack(pady=5)

nome_entry = tk.Entry(app, width=30)
nome_entry.pack(pady=5)

# Botão para iniciar a automação
iniciar_button = tk.Button(app, text="Iniciar Automação", command=iniciar_automacao, bg="green", fg="white")
iniciar_button.pack(pady=20)

# Loop principal
app.mainloop()
