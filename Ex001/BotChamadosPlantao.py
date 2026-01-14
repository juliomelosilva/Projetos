import openpyxl
import time
import pyautogui
import webbrowser
import keyboard
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

# =====================================================
# CONFIGURAÇÕES GERAIS (AJUSTE AQUI)
# =====================================================

URL_SISTEMA = "https://smliveloja.bitrix24.site/plantao/"
PASTA_IMAGENS = "imagens"
CONFIANCA_IMAGEM = 0.8

# 🔽 Scroll padrão (negativo = para baixo)
SCROLL_PADRAO = -1000

CONFIG_DIA = "config_dia.json"

# =====================================================
# FUNÇÕES AUXILIARES DE IMAGEM
# =====================================================
def localizar_imagem(nome, timeout=15):
    """
    Aguarda uma imagem aparecer na tela e retorna sua posição.
    Ajuste CONFIANCA_IMAGEM se necessário.
    """
    caminho = os.path.join(PASTA_IMAGENS, nome)
    inicio = time.time()

    while time.time() - inicio < timeout:
        try:
            pos = pyautogui.locateCenterOnScreen(
                caminho, confidence=CONFIANCA_IMAGEM
            )
            if pos:
                return pos
        except:
            pass
        time.sleep(0.4)

    raise Exception(f"Imagem não encontrada: {nome}")

def clicar_imagem(nome, timeout=15):
    pos = localizar_imagem(nome, timeout)
    pyautogui.click(pos)
    time.sleep(0.4)

# =====================================================
# CONFIGURAÇÃO DO DIA (COORDENADA)
# =====================================================
def salvar_dia(coord):
    with open(CONFIG_DIA, "w") as f:
        json.dump(coord, f, indent=4)

def carregar_dia():
    if os.path.exists(CONFIG_DIA):
        with open(CONFIG_DIA, "r") as f:
            return json.load(f)
    return None

def configurar_dia():
    messagebox.showinfo(
        "Configurar Dia",
        "Abra o calendário, posicione o mouse sobre o DIA desejado\n"
        "e pressione F8"
    )

    keyboard.wait("F8")
    x, y = pyautogui.position()
    salvar_dia({"x": x, "y": y})

    messagebox.showinfo(
        "Salvo",
        f"Dia configurado em: ({x}, {y})"
    )

# =====================================================
# CONFIGURAÇÃO (ABRE O SITE)
# =====================================================
def configurar_campos():
    webbrowser.open(URL_SISTEMA)
    time.sleep(6)

    # Abre o seletor de data por IMAGEM
    clicar_imagem("selecao_data.png")

    # Mantém apenas o DIA por coordenada
    configurar_dia()

# =====================================================
# AUTOMAÇÃO PRINCIPAL
# =====================================================
def iniciar_automacao():
    dia = carregar_dia()
    if not dia:
        messagebox.showerror(
            "Erro",
            "Dia não configurado.\nClique em 'Configurar Campos' primeiro."
        )
        return

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
        workbook = openpyxl.load_workbook(arquivo_excel)
        planilha = workbook["Planilha1"]

        webbrowser.open(URL_SISTEMA)
        time.sleep(6)

        # ================================
        # TÉCNICO
        # ================================
        clicar_imagem("tecnico.png")
        keyboard.write(nome_tecnico)

        # ================================
        # DATA
        # ================================
        clicar_imagem("selecao_data.png")
        pyautogui.click(dia["x"], dia["y"])
        time.sleep(0.5)

        # ================================
        # LOOP DOS CHAMADOS
        # ================================
        for linha in planilha.iter_rows(min_row=2):
            empresa, titulo, resolucao = [c.value for c in linha[:3]]

            if not empresa and not titulo and not resolucao:
                break

            clicar_imagem("empresa.png")
            keyboard.write(str(empresa))

            clicar_imagem("titulo.png")
            keyboard.write(str(titulo))

            clicar_imagem("descricao.png")
            keyboard.write(str(titulo))

            clicar_imagem("resolucao.png")
            keyboard.write(str(resolucao))

            # 🔽 SCROLL APÓS RESOLUÇÃO
            pyautogui.scroll(SCROLL_PADRAO)
            time.sleep(0.4)

            # PRIORIDADE
            clicar_imagem("prioridade.png")
            clicar_imagem("prioridade_opcao.png")

            # CATEGORIA
            clicar_imagem("categoria.png")

            # 🔽 SCROLL APÓS CLICAR NA CATEGORIA
            pyautogui.scroll(SCROLL_PADRAO)
            time.sleep(0.4)

            clicar_imagem("categoria_opcao.png")

            # FINALIZAR
            clicar_imagem("finalizar.png")
            time.sleep(6)

        messagebox.showinfo("Concluído", "Chamados registrados com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# =====================================================
# INTERFACE GRÁFICA
# =====================================================
app = tk.Tk()
app.title("Automação Plantão")
app.geometry("300x230")

tk.Label(app, text="Nome do Técnico:").pack(pady=5)
nome_entry = tk.Entry(app, width=30)
nome_entry.pack(pady=5)

tk.Button(
    app,
    text="Configurar Campos",
    command=configurar_campos,
    bg="#1f6aa5",
    fg="white"
).pack(pady=10)

tk.Button(
    app,
    text="Abrir Chamados",
    command=iniciar_automacao,
    bg="green",
    fg="white"
).pack(pady=10)

app.mainloop()
