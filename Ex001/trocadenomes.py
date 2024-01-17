import os
import glob
import tkinter as tk
from tkinter import filedialog

def renomear_arquivos(pasta_origem):
    # Lista todos os arquivos com extensão .xml na pasta
    arquivos_xml = glob.glob(os.path.join(pasta_origem, '*.xml'))

    for arquivo_path in arquivos_xml:
        # Obtém apenas o nome do arquivo (sem o caminho completo)
        nome_arquivo = os.path.basename(arquivo_path)

        # Remove o prefixo 'xmlDfe-' do nome do arquivo
        novo_nome = nome_arquivo.replace('xmlDfe-', '')

        # Remove a extensão .xml
        novo_nome = os.path.splitext(novo_nome)[0]

        # Adiciona '-nfe.xml' ao final do nome do arquivo
        novo_nome = f"{novo_nome}-nfe.xml"

        # Caminho completo para o novo nome do arquivo
        novo_caminho = os.path.join(pasta_origem, novo_nome)

        # Renomeia o arquivo
        os.rename(arquivo_path, novo_caminho)

def selecionar_pasta():
    pasta_origem = filedialog.askdirectory(title="Selecione a pasta contendo os arquivos .xml")
    if pasta_origem:
        renomear_arquivos(pasta_origem)
        resultado_label.config(text="Arquivos renomeados com sucesso!")

# Criar a janela principal
janela = tk.Tk()
janela.title("Renomeador de Arquivos XML")

# Botão para selecionar a pasta
selecionar_botao = tk.Button(janela, text="Selecionar Pasta", command=selecionar_pasta)
selecionar_botao.pack(pady=20)

# Rótulo para exibir o resultado
resultado_label = tk.Label(janela, text="")
resultado_label.pack()

# Iniciar o loop da interface gráfica
janela.mainloop()
