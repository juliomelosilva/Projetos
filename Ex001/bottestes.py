import tkinter as tk
from tkinter import filedialog, messagebox
import os
import webbrowser
import time
import openpyxl

# Função para selecionar a planilha
def selecionar_planilha():
    arquivo_planilha = filedialog.askopenfilename(title="Selecionar Planilha",
                                                  filetypes=[("Planilhas Excel", "*.xlsx;*.xls"), ("Arquivos CSV", "*.csv")])
    
    if arquivo_planilha:
        # Salva o nome da planilha selecionada em um arquivo de texto
        caminho, nome_arquivo = os.path.split(arquivo_planilha)
        caminho_salvar = os.path.join(caminho, "planilha_chamados")
        with open(caminho_salvar, "w") as arquivo_txt:
            arquivo_txt.write(nome_arquivo)
        
        messagebox.showinfo("Arquivo Selecionado", f"Planilha selecionada: {nome_arquivo}")
    else:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado.")

# Criação da interface gráfica
root = tk.Tk()
root.title("Selecionar Planilha")

# Botão para selecionar a planilha
btn_selecionar_planilha = tk.Button(root, text="Selecionar Planilha", command=selecionar_planilha)
btn_selecionar_planilha.pack(pady=20)

workbook = openpyxl.load_workbook(planilha_chamados)
chamados = workbook['Planilha1']
webbrowser.open('https://smliveloja.bitrix24.site/plantao/')
time.sleep(2)


root.mainloop()





