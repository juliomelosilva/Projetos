
"""
Bingo Profissional
Requisitos opcionais:
pip install customtkinter pyttsx3

Se customtkinter não estiver disponível, usa tkinter padrão.
"""
import json
import random
import sqlite3
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

try:
    import pyttsx3
    VOZ = pyttsx3.init()
except Exception:
    VOZ = None

DB = "bingo.db"

class BingoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bingo Profissional")
        self.root.geometry("1200x750")

        self.minimo = 1
        self.maximo = 75
        self.sorteados = []
        self.disponiveis = list(range(self.minimo, self.maximo + 1))

        self._db()
        self._ui()
        self.carregar_cartelas()

    def _db(self):
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS cartelas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            numeros TEXT NOT NULL
        )
        """)
        con.commit()
        con.close()

    def _ui(self):
        top = tk.Frame(self.root)
        top.pack(fill="x", padx=10, pady=5)

        tk.Button(top, text="Sortear", command=self.sortear).pack(side="left", padx=5)
        tk.Button(top, text="Novo Sorteio", command=self.novo_sorteio).pack(side="left", padx=5)
        tk.Button(top, text="Novo Bingo", command=self.novo_bingo).pack(side="left", padx=5)
        tk.Button(top, text="Gerar Cartela", command=self.gerar_cartela).pack(side="left", padx=5)

        self.lbl_numero = tk.Label(self.root, text="-", font=("Arial", 60, "bold"))
        self.lbl_numero.pack(pady=10)

        main = tk.Frame(self.root)
        main.pack(fill="both", expand=True)

        left = tk.Frame(main)
        left.pack(side="left", fill="both", expand=True)

        right = tk.Frame(main)
        right.pack(side="right", fill="y")

        self.painel = {}
        grid = tk.Frame(left)
        grid.pack()

        n = 1
        for r in range(15):
            for c in range(5):
                lbl = tk.Label(grid, text=f"{n:02}", width=4, relief="ridge")
                lbl.grid(row=r, column=c, padx=1, pady=1)
                self.painel[n] = lbl
                n += 1
                if n > 75:
                    break

        tk.Label(right, text="Cartelas").pack()

        self.lista = tk.Listbox(right, width=50)
        self.lista.pack(fill="y", expand=True)

        tk.Button(right, text="Excluir Cartela", command=self.excluir_cartela).pack(fill="x")
        tk.Button(right, text="Verificar Vencedor", command=self.verificar_vencedores).pack(fill="x")

    def falar(self, texto):
        if VOZ:
            try:
                VOZ.say(texto)
                VOZ.runAndWait()
            except:
                pass

    def gerar_cartela(self):
        nome = simpledialog.askstring("Nome", "Nome da cartela/jogador:")
        if not nome:
            return

        numeros = sorted(random.sample(range(self.minimo, self.maximo + 1), 15))

        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute(
            "INSERT INTO cartelas(nome,numeros) VALUES (?,?)",
            (nome, json.dumps(numeros))
        )
        con.commit()
        con.close()

        self.carregar_cartelas()

    def carregar_cartelas(self):
        self.lista.delete(0, tk.END)

        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("SELECT id,nome,numeros FROM cartelas")
        self.cartelas = cur.fetchall()
        con.close()

        for cid, nome, nums in self.cartelas:
            self.lista.insert(tk.END, f"#{cid} - {nome}")

    def excluir_cartela(self):
        sel = self.lista.curselection()
        if not sel:
            return

        cid = self.cartelas[sel[0]][0]

        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("DELETE FROM cartelas WHERE id=?", (cid,))
        con.commit()
        con.close()

        self.carregar_cartelas()

    def sortear(self):
        if not self.disponiveis:
            messagebox.showinfo("Fim", "Todos os números foram sorteados.")
            return

        numero = random.choice(self.disponiveis)
        self.disponiveis.remove(numero)
        self.sorteados.append(numero)

        self.lbl_numero.config(text=str(numero))
        self.painel[numero].config(bg="green", fg="white")

        self.falar(f"Número {numero}")
        self.verificar_vencedores(auto=True)

    def novo_sorteio(self):
        self.sorteados.clear()
        self.disponiveis = list(range(self.minimo, self.maximo + 1))

        for lbl in self.painel.values():
            lbl.config(bg="SystemButtonFace", fg="black")

        self.lbl_numero.config(text="-")

    def novo_bingo(self):
        if not messagebox.askyesno("Confirmar", "Apagar todas as cartelas e reiniciar?"):
            return

        self.novo_sorteio()

        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("DELETE FROM cartelas")
        con.commit()
        con.close()

        self.carregar_cartelas()

    def verificar_vencedores(self, auto=False):
        sorteados = set(self.sorteados)
        vencedores = []

        for cid, nome, nums in self.cartelas:
            numeros = set(json.loads(nums))

            if numeros.issubset(sorteados):
                vencedores.append(nome)

        if vencedores:
            messagebox.showinfo(
                "BINGO!",
                "Vencedores:\n\n" + "\n".join(vencedores)
            )
        elif not auto:
            messagebox.showinfo("Resultado", "Nenhum vencedor ainda.")


if __name__ == "__main__":
    root = tk.Tk()
    app = BingoApp(root)
    root.mainloop()
