import threading
import time
import tkinter as tk
from tkinter import ttk
import ctypes
import keyboard

# ============================
# SENDINPUT (CLIQUE REAL)
# ============================
PUL = ctypes.POINTER(ctypes.c_ulong)

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("mi", MOUSEINPUT)
    ]

def send_click():
    extra = ctypes.c_ulong(0)

    ii_ = INPUT(type=0,
        mi=MOUSEINPUT(0, 0, 0, 0x0002, 0, ctypes.pointer(extra)))
    ctypes.windll.user32.SendInput(1, ctypes.pointer(ii_), ctypes.sizeof(ii_))

    ii_ = INPUT(type=0,
        mi=MOUSEINPUT(0, 0, 0, 0x0004, 0, ctypes.pointer(extra)))
    ctypes.windll.user32.SendInput(1, ctypes.pointer(ii_), ctypes.sizeof(ii_))

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
        delay = speed_scale.get() / 1000

        send_click()
        click_count += 1

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

tk.Label(root, text="AUTO CLICKER",
         font=("Arial", 14, "bold"),
         fg="white", bg="#1e1e1e").pack(pady=10)

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