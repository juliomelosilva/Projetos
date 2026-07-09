
"""
BINGO PROFISSIONAL V3
=====================

ALTERAÇÃO DE CORES (PERSONALIZAÇÃO)
-----------------------------------
Edite apenas estes valores:

PRIMARY_COLOR   = "#2563EB"  # Azul principal
SUCCESS_COLOR   = "#16A34A"  # Verde números sorteados
WARNING_COLOR   = "#F59E0B"  # Laranja alertas
DANGER_COLOR    = "#DC2626"  # Vermelho
BG_COLOR        = "#111827"  # Fundo
CARD_COLOR      = "#1F2937"  # Painéis
TEXT_COLOR      = "#F9FAFB"  # Texto

Requer:
pip install customtkinter
"""

import customtkinter as ctk
import sqlite3
import random
import json
from tkinter import messagebox, simpledialog

PRIMARY_COLOR = "#2563EB"
SUCCESS_COLOR = "#16A34A"
WARNING_COLOR = "#F59E0B"
DANGER_COLOR = "#DC2626"
BG_COLOR = "#111827"
CARD_COLOR = "#1F2937"
TEXT_COLOR = "#F9FAFB"

DB = "bingo_v3.db"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class BingoProfissional:

    def __init__(self, root):
        self.root = root
        self.root.title("BINGO PROFISSIONAL")
        self.root.geometry("1400x850")

        self.sorteados = []
        self.disponiveis = list(range(1, 76))

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

        titulo = ctk.CTkLabel(
            self.root,
            text="🎱 BINGO PROFISSIONAL 🎱",
            font=("Arial", 34, "bold"),
            text_color=TEXT_COLOR
        )
        titulo.pack(pady=10)

        topo = ctk.CTkFrame(self.root)
        topo.pack(fill="x", padx=10)

        ctk.CTkButton(
            topo,
            text="Gerar Cartelas",
            fg_color=PRIMARY_COLOR,
            command=self.gerar_lote
        ).pack(side="left", padx=5, pady=5)

        ctk.CTkButton(
            topo,
            text="Sortear",
            fg_color=SUCCESS_COLOR,
            command=self.sortear
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            topo,
            text="Novo Sorteio",
            fg_color=WARNING_COLOR,
            command=self.novo_sorteio
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            topo,
            text="Verificar Cartela",
            fg_color=DANGER_COLOR,
            command=self.verificar_cartela
        ).pack(side="left", padx=5)

        self.numero_label = ctk.CTkLabel(
            self.root,
            text="-",
            font=("Arial", 100, "bold")
        )
        self.numero_label.pack(pady=15)

        self.info = ctk.CTkLabel(
            self.root,
            text="Sorteados: 0 | Restantes: 75"
        )
        self.info.pack()

        centro = ctk.CTkFrame(self.root)
        centro.pack(fill="both", expand=True, padx=10, pady=10)

        esquerda = ctk.CTkFrame(centro)
        esquerda.pack(side="left", fill="both", expand=True, padx=5)

        direita = ctk.CTkFrame(centro, width=350)
        direita.pack(side="right", fill="y", padx=5)

        self.labels = {}

        painel = ctk.CTkFrame(esquerda)
        painel.pack(pady=10)

        n = 1
        for r in range(15):
            for c in range(5):

                if n > 75:
                    break

                lbl = ctk.CTkLabel(
                    painel,
                    text=f"{n:02}",
                    width=60,
                    height=40,
                    fg_color=CARD_COLOR,
                    corner_radius=8
                )

                lbl.grid(row=r, column=c, padx=2, pady=2)

                self.labels[n] = lbl
                n += 1

        ctk.CTkLabel(
            direita,
            text="Últimos Sorteios",
            font=("Arial", 20, "bold")
        ).pack(pady=5)

        self.lista = ctk.CTkTextbox(direita, width=300)
        self.lista.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(
            direita,
            text="Ranking Próximos do Bingo"
        ).pack()

        self.ranking = ctk.CTkTextbox(direita, height=200)
        self.ranking.pack(fill="x", padx=5, pady=5)

    def gerar_lote(self):

        try:
            inicio = int(simpledialog.askstring("Início", "Cartela inicial"))
            fim = int(simpledialog.askstring("Fim", "Cartela final"))

            con = sqlite3.connect(DB)
            cur = con.cursor()

            for numero in range(inicio, fim + 1):

                numeros = sorted(
                    random.sample(range(1, 76), 24)
                )

                cur.execute(
                    "INSERT OR REPLACE INTO cartelas VALUES (?,?)",
                    (numero, json.dumps(numeros))
                )

            con.commit()
            con.close()

            messagebox.showinfo(
                "Sucesso",
                f"{fim - inicio + 1} cartelas geradas."
            )

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_ranking(self):

        con = sqlite3.connect(DB)
        cur = con.cursor()

        cur.execute("SELECT numero,numeros FROM cartelas")

        ranking = []

        for numero, numeros in cur.fetchall():

            nums = set(json.loads(numeros))

            faltantes = len(
                nums - set(self.sorteados)
            )

            ranking.append((numero, faltantes))

        con.close()

        ranking.sort(key=lambda x: x[1])

        self.ranking.delete("1.0", "end")

        for numero, faltam in ranking[:10]:
            self.ranking.insert(
                "end",
                f"Cartela {numero} → faltam {faltam}\n"
            )

        if len(self.sorteados) >= 24 and ranking:

            melhor = ranking[0]

            if melhor[1] <= 1:
                messagebox.showwarning(
                    "Possível vencedor",
                    f"Cartela {melhor[0]} está muito próxima do bingo!"
                )

    def sortear(self):

        if not self.disponiveis:
            messagebox.showinfo("Fim", "Todos os números foram sorteados.")
            return

        numero = random.choice(self.disponiveis)

        self.disponiveis.remove(numero)
        self.sorteados.append(numero)

        self.numero_label.configure(text=str(numero))

        self.labels[numero].configure(
            fg_color=SUCCESS_COLOR
        )

        self.lista.insert(
            "1.0",
            f"{numero:02}\n"
        )

        self.info.configure(
            text=f"Sorteados: {len(self.sorteados)} | Restantes: {len(self.disponiveis)}"
        )

        self.atualizar_ranking()

    def novo_sorteio(self):

        self.sorteados.clear()
        self.disponiveis = list(range(1, 76))

        self.numero_label.configure(text="-")

        self.lista.delete("1.0", "end")
        self.ranking.delete("1.0", "end")

        for lbl in self.labels.values():
            lbl.configure(
                fg_color=CARD_COLOR
            )

    def verificar_cartela(self):

        try:

            numero = int(
                simpledialog.askstring(
                    "Verificar",
                    "Número da cartela"
                )
            )

            con = sqlite3.connect(DB)
            cur = con.cursor()

            cur.execute(
                "SELECT numeros FROM cartelas WHERE numero=?",
                (numero,)
            )

            row = cur.fetchone()
            con.close()

            if not row:
                messagebox.showerror(
                    "Erro",
                    "Cartela não encontrada."
                )
                return

            cartela = set(json.loads(row[0]))

            faltantes = sorted(
                cartela - set(self.sorteados)
            )

            if len(faltantes) == 0:

                messagebox.showinfo(
                    "🏆 BINGO CONFIRMADO",
                    f"Cartela vencedora: {numero}"
                )

            else:

                messagebox.showwarning(
                    "Bingo inválido",
                    f"Faltam {len(faltantes)} números:\n\n{faltantes}"
                )

        except:
            pass


if __name__ == "__main__":
    root = ctk.CTk()
    app = BingoProfissional(root)
    root.mainloop()
