import os
import shutil
import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET

def pesquisar_numeros_na_pasta(pasta, numeros_pesquisados):
    resultados = []
    try:
        for pasta_raiz, _, arquivos in os.walk(pasta):
            for arquivo in arquivos:
                if arquivo.endswith(".xml"):
                    caminho_arquivo = os.path.join(pasta_raiz, arquivo)
                    if verifica_numero_em_arquivo(caminho_arquivo, numeros_pesquisados):
                        resultados.append(caminho_arquivo)
        return resultados
    except Exception as e:
        print(f"Erro ao pesquisar números na pasta: {e}")
        return []

def verifica_numero_em_arquivo(caminho_arquivo, numeros_pesquisados):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
            return any(f'<nNF>{numero}</nNF>' in conteudo for numero in numeros_pesquisados)
    except Exception as e:
        print(f"Erro ao ler o arquivo {caminho_arquivo}: {e}")
        return False

def gerar_sequencia(numero_base, quantidade, incremento):
    return [numero_base + i * incremento for i in range(quantidade)]

def selecionar_pasta():
    pasta_selecionada = filedialog.askdirectory()
    entry_pasta.delete(0, tk.END)
    entry_pasta.insert(0, pasta_selecionada)
    resultado_text.config(state=tk.NORMAL)
    resultado_text.delete(1.0, tk.END)
    resultado_text.config(state=tk.DISABLED)

def iniciar_pesquisa():
    try:
        pasta = entry_pasta.get()
        numero_base = int(entry_numero_base.get())
        quantidade = int(entry_quantidade.get())
        incremento = int(entry_incremento.get())

        numeros_pesquisados = gerar_sequencia(numero_base, quantidade, incremento)
        resultados = pesquisar_numeros_na_pasta(pasta, numeros_pesquisados)
        mostrar_resultados(resultados)
    except Exception as e:
        print(f"Erro ao iniciar a pesquisa: {e}")

def mostrar_resultados(resultados):
    resultado_text.config(state=tk.NORMAL)
    resultado_text.delete(1.0, tk.END)
    if resultados:
        resultado_text.insert(tk.END, "Arquivos encontrados:\n")
        for resultado in resultados:
            resultado_text.insert(tk.END, f"{resultado}\n")
        resultado_text.config(state=tk.DISABLED)
    else:
        resultado_text.insert(tk.END, "Nenhum arquivo encontrado.")
        resultado_text.config(state=tk.DISABLED)

def selecionar_destino():
    pasta_destino = filedialog.askdirectory()
    entry_destino.delete(0, tk.END)
    entry_destino.insert(0, pasta_destino)

def copiar_arquivos(destino, resultados):
    try:
        for resultado in resultados:
            if os.path.exists(resultado):
                shutil.copy2(resultado, destino)
                print(f"Arquivo copiado: {resultado}")
            else:
                print(f"Arquivo não encontrado: {resultado}")
        return True
    except FileNotFoundError as e:
        print(f"Erro ao copiar arquivos: {e}")
        return False
    except Exception as e:
        print(f"Erro desconhecido ao copiar arquivos: {e}")
        return False

def iniciar_copia():
    try:
        pasta_destino = entry_destino.get()
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        resultados = resultado_text.get("1.0", tk.END).splitlines()[1:]  # Ignora a primeira linha
        sucesso = copiar_arquivos(pasta_destino, resultados)
        if sucesso:
            tk.messagebox.showinfo("Sucesso", "Arquivos copiados com sucesso.")
        else:
            tk.messagebox.showerror("Erro", "Erro ao copiar arquivos.")
    except Exception as e:
        tk.messagebox.showerror("Erro", f"Erro ao iniciar a cópia: {e}")

# Interface gráfica
root = tk.Tk()
root.title("Pesquisa e Cópia de Números em Arquivos XML")

# Componentes da interface
tk.Label(root, text="Selecione a Pasta:").grid(row=0, column=0, padx=10, pady=5)
entry_pasta = tk.Entry(root)
entry_pasta.grid(row=0, column=1, padx=10, pady=5)
btn_selecionar_pasta = tk.Button(root, text="Selecionar", command=selecionar_pasta)
btn_selecionar_pasta.grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Número Base:").grid(row=1, column=0, padx=10, pady=5)
entry_numero_base = tk.Entry(root)
entry_numero_base.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Quantidade:").grid(row=2, column=0, padx=10, pady=5)
entry_quantidade = tk.Entry(root)
entry_quantidade.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Incremento:").grid(row=3, column=0, padx=10, pady=5)
entry_incremento = tk.Entry(root)novo lino 2
entry_incremento.grid(row=3, column=1, padx=10, pady=5)

btn_pesquisar = tk.Button(root, text="Iniciar Pesquisa", command=iniciar_pesquisa)
btn_pesquisar.grid(row=4, column=0, columnspan=3, pady=10)

resultado_text = tk.Text(root, height=10, width=50, state=tk.DISABLED)
resultado_text.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

tk.Label(root, text="Selecione a Pasta de Destino:").grid(row=6, column=0, padx=10, pady=5)
entry_destino = tk.Entry(root)
entry_destino.grid(row=6, column=1, padx=10, pady=5)
btn_selecionar_destino = tk.Button(root, text="Selecionar", command=selecionar_destino)
btn_selecionar_destino.grid(row=6, column=2, padx=5, pady=5)

btn_iniciar_copia = tk.Button(root, text="Iniciar Cópia", command=iniciar_copia)
btn_iniciar_copia.grid(row=7, column=0, columnspan=3, pady=10)

root.mainloop()