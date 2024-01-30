import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import xml.etree.ElementTree as ET
import threading
import queue

def pesquisar_numeros_na_pasta(pasta, numeros_pesquisados, progress_var, progress_queue):
    resultados = []
    total_arquivos = sum(1 for _ in os.walk(pasta) for _ in _[2] if _.endswith('.xml'))
    progress_unit = 100 / total_arquivos  # Unidade de progresso por arquivo

    try:
        for i, (pasta_raiz, _, arquivos) in enumerate(os.walk(pasta)):
            for arquivo in arquivos:
                if arquivo.endswith(".xml"):
                    caminho_arquivo = os.path.join(pasta_raiz, arquivo)
                    if verifica_numero_em_arquivo(caminho_arquivo, numeros_pesquisados):
                        resultados.append(caminho_arquivo)

                progress_var.set((i + 1) * progress_unit)  # Atualiza a barra de progresso
                progress_queue.put(progress_var.get())  # Coloca o valor na fila para atualização na GUI
    except Exception as e:
        print(f"Erro ao pesquisar números na pasta: {e}")
        return []

    return resultados

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

def iniciar_pesquisa():
    try:
        pasta = entry_pasta.get()
        numero_base = int(entry_numero_base.get())
        quantidade = int(entry_quantidade.get())
        incremento = int(entry_incremento.get())

        numeros_pesquisados = gerar_sequencia(numero_base, quantidade, incremento)

        # Criar e iniciar a barra de progresso
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
        progress_bar.grid(row=8, column=0, columnspan=3, pady=5)

        progress_queue = queue.Queue()

        # Criar e iniciar a thread de pesquisa
        pesquisa_thread = threading.Thread(target=lambda: realizar_pesquisa(pasta, numeros_pesquisados, progress_var, progress_queue))
        pesquisa_thread.start()

        # Chamar a função de atualização da barra de progresso em loop
        root.after(100, lambda: atualizar_barra_progresso(progress_queue, progress_bar))

    except Exception as e:
        print(f"Erro ao iniciar a pesquisa: {e}")

def realizar_pesquisa(pasta, numeros_pesquisados, progress_var, progress_queue):
    try:
        resultados = pesquisar_numeros_na_pasta(pasta, numeros_pesquisados, progress_var, progress_queue)
        mostrar_resultados(resultados)
    except Exception as e:
        print(f"Erro ao realizar a pesquisa: {e}")

def atualizar_barra_progresso(progress_queue, progress_bar):
    try:
        while not progress_queue.empty():
            progress_value = progress_queue.get()
            progress_bar['value'] = progress_value
        root.after(100, lambda: atualizar_barra_progresso(progress_queue, progress_bar))
    except Exception as e:
        print(f"Erro ao atualizar a barra de progresso: {e}")

# Restante do código permanece inalterado...

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
entry_incremento = tk.Entry(root)
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