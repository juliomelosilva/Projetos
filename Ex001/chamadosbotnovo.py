import openpyxl
import time
import pyautogui
import webbrowser
import keyboard
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog  # Importação corrigida
import json
import os

# Caminho do arquivo de configuração para salvar as imagens de referência
config_file = "config_imagens.json"

def salvar_configuracao(imagens):
    with open(config_file, "w") as file:
        json.dump(imagens, file)
    print(f"Imagens de referência salvas: {imagens}")

def carregar_configuracao():
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            return json.load(file)
    return {}

def configurar_imagens():
    imagens = {}
    arquivos_selecionados = filedialog.askopenfilenames(title="Selecione as imagens de referência", filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
    if not arquivos_selecionados:
        messagebox.showerror("Erro", "Nenhuma imagem selecionada. Configuração cancelada.")
        return
    
    nomes_campos = [
        "tecnico", "selecao_data", "dia", "empresa", "titulo", "descricao", 
        "resolucao", "prioridade", "prioridade_opcao", "categoria", "categoria_opcao", "finalizar"
    ]
    
    arquivos_disponiveis = {os.path.basename(arquivo).split('.')[0]: arquivo for arquivo in arquivos_selecionados}
    
    for nome in nomes_campos:
        if nome in arquivos_disponiveis:
            imagens[nome] = arquivos_disponiveis[nome]
        else:
            messagebox.showerror("Erro", f"Imagem para '{nome}' não encontrada entre os arquivos selecionados. Configuração cancelada.")
            return
    
    salvar_configuracao(imagens)
    messagebox.showinfo("Configuração Salva", "Todas as imagens foram configuradas com sucesso!")

def validar_imagens():
    config = carregar_configuracao()
    nomes_campos = [
        "tecnico", "selecao_data", "dia", "empresa", "titulo", "descricao", 
        "resolucao", "prioridade", "prioridade_opcao", "categoria", "categoria_opcao", "finalizar"
    ]
    
    imagens_faltando = [nome for nome in nomes_campos if nome not in config]
    if imagens_faltando:
        messagebox.showerror("Erro", f"As seguintes imagens não estão configuradas: {', '.join(imagens_faltando)}")
        return False
    return True

def clicar_na_imagem(nome):
    config = carregar_configuracao()
    if nome in config:
        imagem = config[nome]
        posicao = pyautogui.locateCenterOnScreen(imagem, confidence=0.8)
        if posicao:
            pyautogui.click(posicao.x, posicao.y)
            print(f"Clicado na imagem {nome} na posição {posicao}")
            return True
        else:
            messagebox.showerror("Erro", f"Imagem '{nome}' não encontrada na tela.")
            return False
    else:
        messagebox.showerror("Erro", f"Imagem '{nome}' não configurada. Configure as imagens primeiro.")
        return False

def iniciar_automacao():
    if not validar_imagens():
        return
    
    nome_tecnico = input_tecnico.get().strip()
    if not nome_tecnico:
        messagebox.showerror("Erro", "Nome do Técnico não pode ser vazio.")
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
        time.sleep(5)

        # Preenche os chamados
        for linha in chamados.iter_rows(min_row=2):
            Nome = linha[0].value
            Descricao = linha[1].value
            Resolucao = linha[2].value

            
            if not clicar_na_imagem("tecnico"):
                return
            
            if Nome is None and Descricao is None and Resolucao is None:
                print("Linha vazia encontrada. Encerrando o processo.")
                break

            time.sleep(1.0)
            keyboard.write(nome_tecnico)  # Correção aqui
            time.sleep(1.0)
            
            clicar_na_imagem("selecao_data")
            time.sleep(0.5)
            clicar_na_imagem("dia")
            time.sleep(0.5)
            
            clicar_na_imagem("empresa")
            time.sleep(0.5)
            keyboard.write(Nome)
            time.sleep(0.5)
            
            clicar_na_imagem("titulo")
            time.sleep(0.5)
            keyboard.write(Descricao)
            time.sleep(0.5)
            
            clicar_na_imagem("descricao")
            time.sleep(0.5)
            keyboard.write(Descricao)
            time.sleep(0.5)
            pyautogui.scroll(-500)
            clicar_na_imagem("resolucao")
            time.sleep(0.5)
            keyboard.write(Resolucao)
            time.sleep(0.5)
            
            clicar_na_imagem("prioridade")
            time.sleep(0.5)
            clicar_na_imagem("prioridade_opcao")
            time.sleep(0.5)
            
            clicar_na_imagem("categoria")
            time.sleep(0.5)
            pyautogui.moveRel(0, 50)
            pyautogui.scroll(-10000)
            time.sleep(0.5)
            pyautogui.moveRel(500, 0)
            time.sleep(0.5)
            pyautogui.scroll(-10000)
            time.sleep(0.5)
            clicar_na_imagem("categoria_opcao")
            time.sleep(0.5)
            
            clicar_na_imagem("finalizar")
            time.sleep(6)
        
        messagebox.showinfo("Concluído", "Chamados registrados com sucesso!")
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar o arquivo Excel: {e}")

app = tk.Tk()
app.title("Automação de Chamados por Imagem")
app.geometry("350x300")

label_tecnico = tk.Label(app, text="Nome do Técnico:")
label_tecnico.pack(pady=1)
input_tecnico = tk.Entry(app)
input_tecnico.pack(pady=1)

configurar_button = tk.Button(app, text="Configurar Imagens", command=configurar_imagens, bg="blue", fg="white")
configurar_button.pack(pady=10)

iniciar_button = tk.Button(app, text="Iniciar Automação", command=iniciar_automacao, bg="green", fg="white")
iniciar_button.pack(pady=10)

app.mainloop()
