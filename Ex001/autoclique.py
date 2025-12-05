import threading
import time
import tkinter as tk
import ctypes
import keyboard

# ============================
# CONFIGURAÇÃO DO INTERVALO
# ============================
CLICK_INTERVAL = 0.5   # Clique super rápido

# ============================
# CONFIGURAÇÕES DO WINDOWS
# ============================
user32 = ctypes.windll.user32

# Eventos de clique ESQUERDO no Windows
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP   = 0x0004

def left_click():
    """Executa clique esquerdo."""
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

# ============================
# CONTROLE DO AUTOCLICK
# ============================
running = False

def auto_clicker():
    global running
    while running:
        left_click()
        time.sleep(CLICK_INTERVAL)

def start_clicking():
    global running
    if not running:
        running = True
        threading.Thread(target=auto_clicker, daemon=True).start()
        status_label.config(text="Status: RODANDO", fg="green")

def stop_clicking():
    global running
    running = False
    status_label.config(text="Status: PARADO", fg="red")

# ============================
# HOTKEYS GLOBAIS (F9/F10)
# ============================
keyboard.add_hotkey("f9", start_clicking)
keyboard.add_hotkey("f10", stop_clicking)

# ============================
# INTERFACE GRÁFICA
# ============================
root = tk.Tk()
root.title("Auto Clicker - Clique Esquerdo (Global Hotkeys)")
root.geometry("270x180")
root.resizable(False, False)

title_label = tk.Label(root, text="Auto Clicker", font=("Arial", 14, "bold"))
title_label.pack(pady=10)

status_label = tk.Label(root, text="Status: PARADO", font=("Arial", 10), fg="red")
status_label.pack(pady=5)

btn_start = tk.Button(root, text="START (F9)", font=("Arial", 12),
                      width=15, command=start_clicking)
btn_start.pack(pady=5)

btn_stop = tk.Button(root, text="STOP (F10)", font=("Arial", 12),
                     width=15, command=stop_clicking)
btn_stop.pack(pady=5)

# Mantém a GUI funcionando
root.mainloop()
