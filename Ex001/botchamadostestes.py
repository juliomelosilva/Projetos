import openpyxl
import time
import pyautogui
import webbrowser
import keyboard
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import json
import os

# Caminho do arquivo de configuração para salvar as coordenadas do dia
config_file = "config_dia.json"

# Função para salvar as coordenadas no arquivo
def salvar_configuracao(coordenadas):
    with open(config_file, "w") as file:
        json.dump(coordenadas, file)
    print(f"Coordenadas salvas: {coordenadas}")

# Função para carregar as coordenadas do arquivo
def carregar_configuracao():
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            return json.load(file)
    return None

# Função para capturar o dia desejado do calendário
def configurar_dia():
    messagebox.showinfo("Configuração do Dia", "Posicione o mouse sobre o dia desejado no calendário.\nAguarde 5 segundos.")
    time.sleep(5)  # Contagem de 5 segundos

    # Captura as coordenadas atuais do mouse
    x, y = pyautogui.position()
    coordenadas = {"x": x, "y": y}
    salvar_configuracao(coordenadas)
    messagebox.showinfo("Configuração Salva", f"Dia configurado com sucesso nas coordenadas: ({x}, {y})")

# Função para selecionar o dia com base na configuração salva
def selecionar_dia():
    coordenadas = carregar_configuracao()
    if coordenadas:
        pyautogui.click(x=coordenadas["x"], y=coordenadas["y"])
        print(f"Selecionado o dia configurado nas coordenadas: ({coordenadas['x']}, {coordenadas['y']})")
    else:
        print("Nenhuma configuração de dia encontrada. Configure o dia primeiro.")
        messagebox.showerror("Erro", "Nenhuma configuração de dia encontrada.\nPor favor, configure o dia.")

# Função principal para iniciar a automação
def iniciar_automacao():
    definir_nome = nome_entry.get()

    if not definir_nome:
        messagebox.showerror("Erro", "Por favor, preencha seu nome.")
        return

    arquivo_excel = filedialog.askopenfilename(title="Selecione o arquivo Excel", filetypes=[("Arquivos Excel", "*.xlsx")])

    if not arquivo_excel:
        messagebox.showerror("Erro", "Por favor, selecione a planilha com os chamados registrados.")
        return

    try:
        # Carrega o arquivo Excel
        workbook = openpyxl.load_workbook(arquivo_excel)
        chamados = workbook['Planilha1']

        # Abre o site no navegador
        webbrowser.open('https://smliveloja.bitrix24.site/plantao/')
        time.sleep(2)

        # Automação: Preenche o nome
        pyautogui.click(x=495, y=336)  # Insere o nome do usuário
        keyboard.write(definir_nome)
        time.sleep(0.5)

        # Seleção do dia (posicionamento do mouse e captura das coordenadas)
        pyautogui.click(x=514, y=400)  # Posição para abrir o seletor de data
        time.sleep(0.5)

        # Configuração do dia
        configurar_dia()  # Aguarda 5 segundos para o usuário posicionar o mouse sobre o dia desejado

        # Seleciona o dia de acordo com a configuração salva
        selecionar_dia()

        # Preenche as demais informações
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

            # Insere nome da empresa
            pyautogui.click(x=530, y=477)  # Posição nome da empresa
            keyboard.write(Nome)
            time.sleep(0.5)

            # Insere descrição e resolução
            pyautogui.click(x=548, y=528)  # Posição título
            keyboard.write(Descricao)
            pyautogui.click(x=457, y=626)  # Posição descrição
            keyboard.write(Descricao)
            pyautogui.scroll(-500)
            time.sleep(0.5)
            pyautogui.click(x=448, y=374)  # Posição resolução
            keyboard.write(Resolucao)
            time.sleep(0.5)

            # Preenche prioridade e categoria
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

        messagebox.showinfo("Concluído", "Chamados Registrados!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Configuração da interface gráfica
app = tk.Tk()
app.title("Automação de Chamados Plantão")
app.geometry("250x150")

# Label e campo de entrada para o nome
nome_label = tk.Label(app, text="Nome do Técnico:")
nome_label.pack(pady=5)

nome_entry = tk.Entry(app, width=30)
nome_entry.pack(pady=5)

# Botão para iniciar a automação
iniciar_button = tk.Button(app, text="Abrir Chamados", command=iniciar_automacao, bg="green", fg="white")
iniciar_button.pack(pady=20)

# Loop principal
app.mainloop()
