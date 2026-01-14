import openpyxl
import time
import pyautogui
import webbrowser
import keyboard
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

# ==================================================
# CONFIGURAÇÕES GERAIS
# ==================================================

SITE_URL = "https://smliveloja.bitrix24.site/plantao/"
CONFIG_DIA = "config_dia.json"

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# ==================================================
# VARIÁVEIS GLOBAIS
# ==================================================

IMAGENS = {}      # Dicionário: nome.png -> caminho
PLANILHA = ""     # Caminho da planilha Excel

# ==================================================
# FUNÇÃO DE CLIQUE POR IMAGEM
# ==================================================

def clicar_imagem(nome, timeout=15, confidence=0.8):
    """
    Localiza uma imagem na tela e clica no centro.
    Ajuste confidence se necessário.
    """
    inicio = time.time()

    while time.time() - inicio < timeout:
        pos = pyautogui.locateCenterOnScreen(
            IMAGENS[nome],
            confidence=confidence
        )
        if pos:
            pyautogui.click(pos)
            return
        time.sleep(0.5)

    raise Exception(f"Imagem não encontrada: {nome}")

# ==================================================
# SELEÇÃO DO DIA (COORDENADA COM F8)
# ==================================================

def salvar_dia(coord):
    with open(CONFIG_DIA, "w") as f:
        json.dump(coord, f)

def carregar_dia():
    if os.path.exists(CONFIG_DIA):
        with open(CONFIG_DIA, "r") as f:
            return json.load(f)
    return None

def configurar_dia():
    # 1️⃣ Clica no seletor de data pela imagem
    clicar_imagem("selecao_data.png")

    # 2️⃣ Solicita ao usuário posicionar o mouse
    messagebox.showinfo(
        "Configurar Dia",
        "Posicione o mouse sobre o DIA desejado\n"
        "e pressione F8 para gravar"
    )

    # 3️⃣ Aguarda F8
    keyboard.wait("f8")

    # 4️⃣ Captura coordenada
    x, y = pyautogui.position()
    salvar_dia({"x": x, "y": y})

    messagebox.showinfo(
        "Sucesso",
        f"Dia gravado com sucesso em:\nX={x} | Y={y}"
    )

# ==================================================
# INTERFACE – SELEÇÃO DE ARQUIVOS
# ==================================================

def selecionar_imagens():
    arquivos = filedialog.askopenfilenames(
        title="Selecione todas as imagens",
        filetypes=[("PNG", "*.png")]
    )

    for img in arquivos:
        IMAGENS[os.path.basename(img)] = img

    messagebox.showinfo(
        "Imagens carregadas",
        f"{len(IMAGENS)} imagens selecionadas com sucesso"
    )

def selecionar_planilha():
    global PLANILHA
    PLANILHA = filedialog.askopenfilename(
        title="Selecione a planilha Excel",
        filetypes=[("Excel", "*.xlsx")]
    )

# ==================================================
# AUTOMAÇÃO PRINCIPAL
# ==================================================

def iniciar_automacao():
    nome_tecnico = nome_entry.get()

    # 🔴 Validações
    if not nome_tecnico:
        messagebox.showerror("Erro", "Informe o nome do técnico")
        return

    if not PLANILHA:
        messagebox.showerror("Erro", "Selecione a planilha")
        return

    dia = carregar_dia()
    if not dia:
        messagebox.showerror("Erro", "Configure o dia antes de iniciar")
        return

    # 📘 Abre a planilha
    wb = openpyxl.load_workbook(PLANILHA)
    sheet = wb.active

    # ==================================================
    # ETAPA 1 – NOME DO TÉCNICO
    # ==================================================
    clicar_imagem("tecnico.png")
    keyboard.write(nome_tecnico)
    time.sleep(0.5)

    # ==================================================
    # ETAPA 2 – SELEÇÃO DA DATA
    # ==================================================
    clicar_imagem("selecao_data.png")
    time.sleep(0.5)
    pyautogui.click(dia["x"], dia["y"])
    time.sleep(0.5)

    # ==================================================
    # LOOP DA PLANILHA
    # ==================================================
    for linha in sheet.iter_rows(min_row=2):

        empresa = linha[0].value
        titulo = linha[1].value
        descricao = linha[1].value
        resolucao = linha[2].value

        # 🛑 Encerra ao encontrar linha vazia
        if not empresa:
            break

        # ================= EMPRESA =================
        clicar_imagem("empresa.png")
        keyboard.write(str(empresa))
        time.sleep(0.3)

        # ================= TÍTULO =================
        clicar_imagem("titulo.png")
        keyboard.write(str(titulo))
        time.sleep(0.3)

        # ================= DESCRIÇÃO =================
        clicar_imagem("descricao.png")
        keyboard.write(str(descricao))
        time.sleep(0.3)

        # ================= RESOLUÇÃO =================
        clicar_imagem("resolucao.png")
        keyboard.write(str(resolucao))
        time.sleep(0.3)

        # 🔽 Scroll após resolução
        pyautogui.scroll(-100000)
        time.sleep(0.3)

# ================= PRIORIDADE =================

# 1️⃣ Clica no campo PRIORIDADE (abre o dropdown)
        clicar_imagem("prioridade.png")
        time.sleep(0.4)

# 2️⃣ Clica na opção desejada
        clicar_imagem("prioridade_opcao.png")
        time.sleep(0.4)

# ================= CATEGORIA (SCROLL ATÉ O FINAL REAL) =================

        # 1️⃣ Abre o dropdown da categoria
        clicar_imagem("categoria.png")
        time.sleep(0.5)

        # 2️⃣ Garante que o mouse esteja dentro do dropdown
        pyautogui.moveRel(0, 100)

        # 3️⃣ Scroll progressivo forte para baixo (força ir ao final)
        
        pyautogui.scroll(-100000)
        time.sleep(0.15)

        pyautogui.moveRel(500, 0)

        
        pyautogui.scroll(-100000)
        time.sleep(0.15)

        # 8️⃣ Clica na ÚLTIMA categoria
        clicar_imagem("categoria_opcao.png")
        time.sleep(0.6)


        # ================= FINALIZAR =================
        clicar_imagem("finalizar.png")
        time.sleep(6)

    messagebox.showinfo("Finalizado", "Todos os chamados foram registrados com sucesso!")

# ==================================================
# INTERFACE GRÁFICA
# ==================================================

app = tk.Tk()
app.title("Bot Chamados Plantão")
app.geometry("320x340")

# 🌐 Abre o site junto com a interface
webbrowser.open(SITE_URL)

tk.Label(app, text="Nome do Técnico").pack(pady=5)
nome_entry = tk.Entry(app, width=30)
nome_entry.pack()

tk.Button(app, text="Selecionar Imagens", command=selecionar_imagens).pack(pady=5)
tk.Button(app, text="Selecionar Planilha", command=selecionar_planilha).pack(pady=5)
tk.Button(app, text="Configurar Dia (F8)", command=configurar_dia, bg="#ffaa00").pack(pady=10)
tk.Button(app, text="Iniciar Automação", command=iniciar_automacao, bg="green", fg="white").pack(pady=10)

app.mainloop()
