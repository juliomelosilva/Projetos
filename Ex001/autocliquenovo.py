import threading
import time
import tkinter as tk
from tkinter import ttk
from pynput.mouse import Controller, Button
import keyboard

# ============================
# CONTROLE DO MOUSE (PYNPUT)
# ============================
mouse = Controller()

def send_click():
    mouse.click(Button.left)

# ============================
# CONTROLE
# ============================
running = False
click_thread = None
click_count = 0

def auto_clicker():
    global running, click_count

    click_count = 0

    while running:
        delay = speed_scale.get() / 1000  # ms → segundos

        send_click()
        click_count += 1

        # Atualiza interface com segurança
        root.after(0, lambda: label_counter.config(text=f"Cliques: {click_count}"))

        time.sleep(delay)

def start_clicking():
    global running, click_thread

    if running:
        return

    running = True
    status_label.config(text="● RODANDO", fg="green")

    click_thread = threading.Thread(target=auto_clicker, daemon=True)
    click_thread.start()

def stop_clicking():
    global running
    running = False
    status_label.config(text="● PARADO", fg="red")

# ============================
# HOTKEY GLOBAL
# ============================
keyboard.add_hotkey("f9", start_clicking)
keyboard.add_hotkey("f10", stop_clicking)

# ============================
# INTERFACE
# ============================
root = tk.Tk()
root.title("Auto Clicker PRO")
root.geometry("320x280")
root.resizable(False, False)
root.configure(bg="#1e1e1e")

# Título
tk.Label(root, text="AUTO CLICKER",
         font=("Arial", 14, "bold"),
         fg="white", bg="#1e1e1e").pack(pady=10)

# Status
status_label = tk.Label(root, text="● PARADO",
                        fg="red", bg="#1e1e1e")
status_label.pack()

# ============================
# SLIDER VELOCIDADE
# ============================
frame_speed = tk.Frame(root, bg="#1e1e1e")
frame_speed.pack(pady=15)

tk.Label(frame_speed, text="Velocidade (ms)",
         fg="white", bg="#1e1e1e").pack()

speed_value = tk.Label(frame_speed, text="500 ms",
                       fg="#00e5ff", bg="#1e1e1e")
speed_value.pack()

def update_speed(val):
    speed_value.config(text=f"{int(float(val))} ms")

speed_scale = ttk.Scale(frame_speed,
                        from_=1, to=1000,
                        orient="horizontal",
                        command=update_speed)
speed_scale.set(500)
speed_scale.pack(padx=20, fill="x")

# ============================
# CONTADOR
# ============================
label_counter = tk.Label(root,
                         text="Cliques: 0",
                         fg="#cccccc", bg="#1e1e1e")
label_counter.pack(pady=10)

# ============================
# BOTÕES
# ============================
frame_buttons = tk.Frame(root, bg="#1e1e1e")
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="START",
          width=12, command=start_clicking).grid(row=0, column=0, padx=5)

tk.Button(frame_buttons, text="STOP",
          width=12, command=stop_clicking).grid(row=0, column=1, padx=5)

# ============================
# LOOP
# ============================
root.mainloop()