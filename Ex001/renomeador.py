import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def renomear_xmls():
    # Abre a janela para selecionar a pasta
    pasta_selecionada = filedialog.askdirectory(title="Selecione a pasta com os arquivos XML")
    
    if not pasta_selecionada:
        return  # Usuário cancelou a seleção

    # Limpa a caixa de logs
    txt_log.delete("1.0", tk.END)
    txt_log.insert(tk.END, f"Pasta selecionada: {pasta_selecionada}\n\n")

    cont_renomeados = 0
    cont_ignorados = 0

    # Lista todos os arquivos da pasta
    for nome_arquivo in os.listdir(pasta_selecionada):
        # Processa apenas arquivos com extensão .xml (ignorando maiúsculas/minúsculas)
        if nome_arquivo.lower().endswith('.xml'):
            
            # Remove a extensão .xml para analisar apenas o nome base
            nome_base = nome_arquivo[:-4]

            # Verifica a regra de ignorar se já tiver -canc ou -nfce no final do nome
            if nome_base.lower().endswith('-canc') or nome_base.lower().endswith('-nfce'):
                txt_log.insert(tk.END, f"IGNORADO: {nome_arquivo} (já possui sufixo protegido)\n")
                cont_ignorados += 1
                continue

            # Define o novo nome adicionando o sufixo -canc
            novo_nome = f"{nome_base}-canc.xml"

            caminho_antigo = os.path.join(pasta_selecionada, nome_arquivo)
            caminho_novo = os.path.join(pasta_selecionada, novo_nome)

            try:
                os.rename(caminho_antigo, caminho_novo)
                txt_log.insert(tk.END, f"SUCESSO: {nome_arquivo} -> {novo_nome}\n")
                cont_renomeados += 1
            except Exception as e:
                txt_log.insert(tk.END, f"ERRO ao renomear {nome_arquivo}: {e}\n")

    # Exibe resumo final
    txt_log.insert(tk.END, f"\n--- Processamento Concluído ---\n")
    txt_log.insert(tk.END, f"Arquivos renomeados: {cont_renomeados}\n")
    txt_log.insert(tk.END, f"Arquivos ignorados: {cont_ignorados}\n")
    
    messagebox.showinfo("Concluído", f"Processo finalizado!\n\nRenomeados: {cont_renomeados}\nIgnorados: {cont_ignorados}")

# --- Configuração da Interface Gráfica ---
root = tk.Tk()
root.title("Renomeador de XMLs (-canc)")
root.geometry("600x400")
root.minsize(500, 300)

# Frame Superior (Botão)
frame_topo = tk.Frame(root, padx=10, pady=10)
frame_topo.pack(fill=tk.X)

lbl_instrucao = tk.Label(frame_topo, text="Clique no botão para escolher a pasta e renomear os arquivos XML:")
lbl_instrucao.pack(side=tk.LEFT, pady=5)

btn_selecionar = tk.Button(
    frame_topo, 
    text="Selecionar Pasta", 
    command=renomear_xmls, 
    bg="#2e7d32", 
    fg="white", 
    font=("Arial", 10, "bold"),
    padx=10,
    pady=5
)
btn_selecionar.pack(side=tk.RIGHT)

# Frame Inferior (Área de Log de Histórico)
frame_log = tk.Frame(root, padx=10, pady=10)
frame_log.pack(fill=tk.BOTH, expand=True)

lbl_log = tk.Label(frame_log, text="Histórico de Alterações:")
lbl_log.pack(anchor="w")

txt_log = scrolledtext.ScrolledText(frame_log, wrap=tk.WORD, font=("Consolas", 9))
txt_log.pack(fill=tk.BOTH, expand=True, pady=5)

# Inicia a aplicação
root.mainloop()