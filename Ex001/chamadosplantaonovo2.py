import openpyxl
import time
import pyautogui
import webbrowser
import keyboard
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# ===============================
# CONFIGURAÇÕES
# ===============================
config_file = "config_dia.json"
imagens = {}

# ===============================
# FUNÇÕES DE CONFIGURAÇÃO
# ===============================
def salvar_configuracao(coordenadas):
    with open(config_file, "w") as file:
        json.dump(coordenadas, file)

def carregar_configuracao():
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            return json.load(file)
    return None

# ===============================
# FUNÇÃO DE CLIQUE POR IMAGEM
# ===============================
def clicar_centro_imagem(nome_imagem, timeout=20):
    if nome_imagem not in imagens:
        raise Exception(f"Imagem não selecionada: {nome_imagem}")

    caminho = imagens[nome_imagem]
    inicio = time.time()
    confidences = [0.9, 0.85, 0.8, 0.75, 0.7, 0.65]

    while time.time() - inicio < timeout:
        for conf in confidences:
            try:
                box = pyautogui.locateOnScreen(
                    caminho,
                    confidence=conf,
                    grayscale=True
                )
                if box:
                    x = box.left + box.width // 2
                    y = box.top + box.height // 2
                    pyautogui.click(x, y)
                    return
            except:
                pass
        time.sleep(0.4)

    # ===== FALLBACK MANUAL =====
    resposta = messagebox.askyesno(
        "Imagem não localizada",
        f"Não foi possível localizar '{nome_imagem}'.\n\nDeseja apontar manualmente?"
    )

    if resposta:
        messagebox.showinfo(
            "Captura Manual",
            "Posicione o mouse no local correto e pressione ENTER."
        )
        keyboard.wait("enter")
        x, y = pyautogui.position()
        pyautogui.click(x, y)
        return

    raise Exception(f"Timeout ao localizar imagem: {nome_imagem}")

# ===============================
# CONFIGURAÇÃO DO DIA
# ===============================
def configurar_dia():
    messagebox.showinfo(
        "Configurar Dia",
        "Abra o calendário.\n\nPosicione o mouse sobre o dia desejado e aguarde 3 segundos."
    )
    time.sleep(3)
    x, y = pyautogui.position()
    salvar_configuracao({"x": x, "y": y})
    messagebox.showinfo("Sucesso", f"Dia configurado em ({x}, {y})")

def selecionar_dia():
    coord = carregar_configuracao()
    if not coord:
        messagebox.showerror("Erro", "Dia não configurado.")
        return
    pyautogui.click(coord["x"], coord["y"])

# ===============================
# SELEÇÃO DE IMAGEM NA INTERFACE
# ===============================
def selecionar_imagem(nome):
    caminho = filedialog.askopenfilename(
        title=f"Selecione a imagem: {nome}",
        filetypes=[("Imagens PNG", "*.png")]
    )
    if caminho:
        imagens[nome] = caminho
        labels_imagens[nome].config(text="✔ Carregada", fg="green")

# ===============================
# AUTOMAÇÃO PRINCIPAL
# ===============================
def iniciar_automacao():
    nome_tecnico = nome_entry.get()

    if not nome_tecnico:
        messagebox.showerror("Erro", "Informe o nome do técnico.")
        return

    arquivo_excel = filedialog.askopenfilename(
        title="Selecione a planilha",
        filetypes=[("Excel", "*.xlsx")]
    )

    if not arquivo_excel:
        return

    try:
        wb = openpyxl.load_workbook(arquivo_excel)
        sheet = wb.active

        webbrowser.open("https://smliveloja.bitrix24.site/plantao/")
        time.sleep(6)

        # Nome do técnico
        clicar_centro_imagem("tecnico")
        keyboard.write(nome_tecnico)

        # Data
        clicar_centro_imagem("data")
        configurar_dia()
        selecionar_dia()

        for row in sheet.iter_rows(min_row=2):
            empresa, descricao, resolucao = [c.value for c in row[:3]]

            if not empresa:
                break

            clicar_centro_imagem("empresa")
            keyboard.write(empresa)

            clicar_centro_imagem("titulo")
            keyboard.write(descricao)

            clicar_centro_imagem("descricao")
            keyboard.write(descricao)

            clicar_centro_imagem("resolucao")
            keyboard.write(resolucao)

            clicar_centro_imagem("enviar")
            time.sleep(6)

        messagebox.showinfo("Sucesso", "Chamados registrados com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# ===============================
# INTERFACE GRÁFICA
# ===============================
app = tk.Tk()
app.title("Automação de Chamados - Plantão")
app.geometry("360x420")

tk.Label(app, text="Nome do Técnico").pack(pady=5)
nome_entry = tk.Entry(app, width=35)
nome_entry.pack()

tk.Label(app, text="Imagens do Sistema").pack(pady=10)

labels_imagens = {}
for nome in ["tecnico", "data", "empresa", "titulo", "descricao", "resolucao", "enviar"]:
    frame = tk.Frame(app)
    frame.pack(pady=3)

    tk.Button(
        frame,
        text=f"Selecionar {nome}.png",
        command=lambda n=nome: selecionar_imagem(n),
        width=20
    ).pack(side="left")

    lbl = tk.Label(frame, text="❌ Não carregada", fg="red")
    lbl.pack(side="left", padx=10)
    labels_imagens[nome] = lbl

tk.Button(
    app,
    text="INICIAR AUTOMAÇÃO",
    bg="green",
    fg="white",
    command=iniciar_automacao,
    width=30
).pack(pady=20)

app.mainloop()
