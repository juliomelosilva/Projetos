# ============================================================
# AUTOMAÇÃO COM AUTO CLIQUE + INTERFACE GRÁFICA
# Autor: Ajustável por você
# ============================================================

import pyautogui
import time
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import sys

# ============================================================
# CONFIGURAÇÕES GERAIS (AJUSTE AQUI)
# ============================================================

# Tempo padrão entre ações
DEFAULT_DELAY = 1.0

# Confiança para reconhecimento de imagem (0.7 a 0.9)
IMAGE_CONFIDENCE = 0.8

# Pasta onde ficam as imagens usadas para reconhecimento
IMAGE_DIR = "imagens"

# Flag global para controle Start / Stop
automation_running = False


# ============================================================
# FUNÇÃO DE LOG (MOSTRA NA INTERFACE)
# ============================================================
def log(msg):
    log_area.insert(tk.END, f"{msg}\n")
    log_area.see(tk.END)
    root.update_idletasks()


# ============================================================
# FUNÇÃO: ESPERA INTELIGENTE POR IMAGEM
# Espera até a imagem aparecer na tela
# ============================================================
def wait_for_image(image_name, timeout=15):
    """
    image_name: nome do arquivo dentro da pasta imagens
    timeout: tempo máximo de espera
    """
    log(f"🔍 Aguardando imagem: {image_name}")
    start = time.time()

    while time.time() - start < timeout:
        if not automation_running:
            return None

        try:
            location = pyautogui.locateCenterOnScreen(
                os.path.join(IMAGE_DIR, image_name),
                confidence=IMAGE_CONFIDENCE
            )
            if location:
                log(f"✅ Imagem encontrada: {image_name}")
                return location
        except:
            pass

        time.sleep(0.5)

    log(f"❌ Timeout ao esperar imagem: {image_name}")
    return None


# ============================================================
# FUNÇÃO: CLIQUE POR IMAGEM
# ============================================================
def click_image(image_name, timeout=15):
    pos = wait_for_image(image_name, timeout)
    if pos:
        pyautogui.click(pos)
        time.sleep(DEFAULT_DELAY)
        return True
    return False


# ============================================================
# FUNÇÃO: CLIQUE POR COORDENADA FIXA
# ============================================================
def click_coord(x, y):
    log(f"🖱️ Clique em coordenada: ({x},{y})")
    pyautogui.click(x, y)
    time.sleep(DEFAULT_DELAY)


# ============================================================
# FUNÇÃO: DIGITAR TEXTO
# ============================================================
def type_text(text):
    pyautogui.write(text, interval=0.05)
    time.sleep(DEFAULT_DELAY)


# ============================================================
# AQUI FICA A LÓGICA PRINCIPAL DO PROCESSO
# 👉 É ESTA FUNÇÃO QUE VOCÊ VAI AJUSTAR CONFORME O VÍDEO
# ============================================================
def automation_flow():
    global automation_running

    log("🚀 Automação iniciada")

    # ================================
    # EXEMPLO DE FLUXO
    # ================================

    # 1️⃣ Esperar botão inicial
    if not click_image("botao_iniciar.png", timeout=20):
        log("❌ Falha no botão iniciar")
        automation_running = False
        return

    # 2️⃣ Clique por coordenada (caso posição seja fixa)
    click_coord(500, 400)

    # 3️⃣ Digitar algo em um campo
    type_text("EXEMPLO DE TEXTO")

    # 4️⃣ Confirmar ação
    click_image("botao_confirmar.png", timeout=10)

    # 5️⃣ Exemplo de decisão
    erro = wait_for_image("mensagem_erro.png", timeout=5)
    if erro:
        log("⚠️ Erro detectado, voltando fluxo")
        click_image("botao_voltar.png", timeout=5)

    log("✅ Fluxo finalizado")
    automation_running = False


# ============================================================
# CONTROLE START
# ============================================================
def start_automation():
    global automation_running

    if automation_running:
        messagebox.showwarning("Aviso", "Automação já está rodando")
        return

    automation_running = True
    log_area.delete(1.0, tk.END)

    thread = threading.Thread(target=automation_flow)
    thread.start()


# ============================================================
# CONTROLE STOP
# ============================================================
def stop_automation():
    global automation_running
    automation_running = False
    log("⛔ Automação interrompida pelo usuário")


# ============================================================
# INTERFACE GRÁFICA
# ============================================================
root = tk.Tk()
root.title("Automação de Processo")
root.geometry("600x450")
root.resizable(False, False)

frame = tk.Frame(root)
frame.pack(pady=10)

btn_start = tk.Button(frame, text="▶ Iniciar", width=15, bg="green", fg="white", command=start_automation)
btn_start.grid(row=0, column=0, padx=5)

btn_stop = tk.Button(frame, text="⛔ Parar", width=15, bg="red", fg="white", command=stop_automation)
btn_stop.grid(row=0, column=1, padx=5)

log_area = scrolledtext.ScrolledText(root, width=70, height=20)
log_area.pack(padx=10, pady=10)

root.mainloop()
