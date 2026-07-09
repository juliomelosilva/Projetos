import customtkinter as ctk
import sqlite3
import json
import secrets
from tkinter import messagebox, simpledialog

PRIMARY_COLOR = "#2563EB"
SUCCESS_COLOR = "#16A34A"
WARNING_COLOR = "#F59E0B"
DANGER_COLOR = "#DC2626"
CARD_COLOR = "#1F2937"
TEXT_COLOR = "#F9FAFB"

DB = "bingo_v3.db"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def formato_bingo(n):
    if 1 <= n <= 15:
        return f"B{n}"
    elif 16 <= n <= 30:
        return f"I{n}"
    elif 31 <= n <= 45:
        return f"N{n}"
    elif 46 <= n <= 60:
        return f"G{n}"
    elif 61 <= n <= 75:
        return f"O{n}"
    return str(n)


class BingoProfissional:

    def __init__(self, root):
        self.root = root
        self.root.title("BINGO PROFISSIONAL")
        self.root.geometry("1400x850")

        self.sorteados = []
        self.disponiveis = list(range(1, 76))
        self.bloqueado = False

        self.criar_db()
        self.criar_interface()

    def criar_db(self):
        con = sqlite3.connect(DB)
        cur = con.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS cartelas(
            numero INTEGER PRIMARY KEY,
            numeros TEXT NOT NULL
        )
        """)

        con.commit()
        con.close()

    def criar_interface(self):

        ctk.CTkLabel(
            self.root,
            text="🎱 B I N G O 🎱",
            font=("Arial", 34, "bold"),
            text_color=TEXT_COLOR
        ).pack(pady=10)

        topo = ctk.CTkFrame(self.root)
        topo.pack(fill="x", padx=10)

        ctk.CTkButton(topo, text="Gerar Cartelas", fg_color=PRIMARY_COLOR,
                      command=self.gerar_lote).pack(side="left", padx=5)

        ctk.CTkButton(topo, text="Sortear", fg_color=SUCCESS_COLOR,
                      command=self.sortear).pack(side="left", padx=5)

        ctk.CTkButton(topo, text="Novo Sorteio", fg_color=WARNING_COLOR,
                      command=self.novo_sorteio).pack(side="left", padx=5)

        ctk.CTkButton(topo, text="Verificar Cartela", fg_color=DANGER_COLOR,
                      command=self.verificar_cartela).pack(side="left", padx=5)

        self.numero_label = ctk.CTkLabel(self.root, text="-",
                                         font=("Arial", 90, "bold"))
        self.numero_label.pack(pady=10)

        self.info = ctk.CTkLabel(self.root, text="Sorteados: 0 | Restantes: 75")
        self.info.pack()

        centro = ctk.CTkFrame(self.root)
        centro.pack(fill="both", expand=True, padx=10, pady=10)

        esquerda = ctk.CTkFrame(centro)
        esquerda.pack(side="left", fill="both", expand=True)

        direita = ctk.CTkFrame(centro, width=350)
        direita.pack(side="right", fill="y")

        self.labels = {}

        painel = ctk.CTkFrame(esquerda)
        painel.pack(pady=10)

        n = 1
        for r in range(15):
            for c in range(5):

                lbl = ctk.CTkLabel(
                    painel,
                    text=formato_bingo(n),
                    width=70,
                    height=40,
                    fg_color=CARD_COLOR,
                    corner_radius=8
                )
                lbl.grid(row=r, column=c, padx=2, pady=2)

                self.labels[n] = lbl
                n += 1

        ctk.CTkLabel(direita, text="Últimos Sorteios",
                     font=("Arial", 18, "bold")).pack(pady=5)

        self.lista = ctk.CTkTextbox(direita, width=300)
        self.lista.pack(fill="both", expand=True)

        ctk.CTkLabel(direita, text="Ranking").pack()

        self.ranking = ctk.CTkTextbox(direita, height=200)
        self.ranking.pack(fill="x", padx=5, pady=5)

    def gerar_lote(self):
        try:
            inicio = int(simpledialog.askstring("Início", "Cartela inicial"))
            fim = int(simpledialog.askstring("Fim", "Cartela final"))

            con = sqlite3.connect(DB)
            cur = con.cursor()

            for numero in range(inicio, fim + 1):
                numeros = sorted(secrets.SystemRandom().sample(range(1, 76), 24))

                cur.execute(
                    "INSERT OR REPLACE INTO cartelas VALUES (?,?)",
                    (numero, json.dumps(numeros))
                )

            con.commit()
            con.close()

            messagebox.showinfo("Sucesso", "Cartelas geradas!")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def sortear(self):

        if self.bloqueado:
            messagebox.showwarning("Bloqueado", "Sorteio pausado.")
            return

        if not self.disponiveis:
            messagebox.showinfo("Fim", "Todos os números foram sorteados.")
            return

        numero = secrets.choice(self.disponiveis)

        self.disponiveis.remove(numero)
        self.sorteados.append(numero)

        self.numero_label.configure(text=formato_bingo(numero))

        self.labels[numero].configure(fg_color=SUCCESS_COLOR)

        self.lista.insert("1.0", f"{formato_bingo(numero)}\n")

        self.info.configure(
            text=f"Sorteados: {len(self.sorteados)} | Restantes: {len(self.disponiveis)}"
        )

        self.verificar_possivel_bingo()

    def verificar_possivel_bingo(self):

        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("SELECT numero,numeros FROM cartelas")

        ranking = []

        for numero, numeros in cur.fetchall():
            nums = set(json.loads(numeros))
            faltam = len(nums - set(self.sorteados))
            ranking.append((numero, faltam))

        con.close()

        ranking.sort(key=lambda x: x[1])

        self.ranking.delete("1.0", "end")

        for num, faltam in ranking[:10]:
            self.ranking.insert("end", f"Cartela {num} → faltam {faltam}\n")

        if ranking and ranking[0][1] <= 1:
            self.bloqueado = True

            resp = messagebox.askyesno(
                "⚠ POSSÍVEL BINGO",
                f"Cartela {ranking[0][0]} está MUITO próxima de ganhar.\n\nContinuar sorteando?"
            )

            if resp:
                self.bloqueado = False
            else:
                messagebox.showinfo("Pausado", "Sorteio interrompido.")

    def novo_sorteio(self):

        self.sorteados.clear()
        self.disponiveis = list(range(1, 76))
        self.bloqueado = False

        self.numero_label.configure(text="-")

        self.lista.delete("1.0", "end")
        self.ranking.delete("1.0", "end")

        for lbl in self.labels.values():
            lbl.configure(fg_color=CARD_COLOR)

    def verificar_cartela(self):

        try:
            numero = int(simpledialog.askstring("Verificar", "Número da cartela"))

            con = sqlite3.connect(DB)
            cur = con.cursor()

            cur.execute("SELECT numeros FROM cartelas WHERE numero=?", (numero,))
            row = cur.fetchone()
            con.close()

            if not row:
                messagebox.showerror("Erro", "Cartela não encontrada.")
                return

            cartela = set(json.loads(row[0]))
            faltantes = sorted(cartela - set(self.sorteados))

            if len(faltantes) == 0:
                messagebox.showinfo("🏆 BINGO", f"Cartela {numero} VENCEU!")
            else:
                messagebox.showwarning(
                    "Ainda não ganhou",
                    f"Faltam {len(faltantes)} números:\n{faltantes}"
                )

        except:
            pass


if __name__ == "__main__":
    root = ctk.CTk()
    app = BingoProfissional(root)
    root.mainloop()