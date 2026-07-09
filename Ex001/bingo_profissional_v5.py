import customtkinter as ctk
import sqlite3
import json
import secrets
import pyttsx3
from tkinter import messagebox, simpledialog

PRIMARY_COLOR = "#2563EB"
SUCCESS_COLOR = "#16A34A"
WARNING_COLOR = "#F59E0B"
DANGER_COLOR = "#DC2626"
CARD_COLOR = "#1F2937"
TEXT_COLOR = "#F9FAFA"

DB = "bingo_v3.db"

# ================= VOZ =================
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def falar(texto):
    engine.say(texto)
    engine.runAndWait()

# ================= FORMATO =================
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

class BingoProfissional:

    def __init__(self, root):
        self.root = root
        self.root.title("BINGO PROFISSIONAL")
        self.root.geometry("1400x850")

        self.sorteados = []
        self.disponiveis = list(range(1, 76))

        self.criar_db()
        self.criar_interface()

    # ================= DB =================
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

    # ================= INTERFACE =================
    def criar_interface(self):

        ctk.CTkLabel(
            self.root,
            text="🎱 B I N G O 🎱",
            font=("Arial", 34, "bold"),
            text_color=TEXT_COLOR
        ).pack(pady=10)

        topo = ctk.CTkFrame(self.root)
        topo.pack(fill="x", padx=10)

        ctk.CTkButton(topo, text="Gerar Cartelas",
                      fg_color=PRIMARY_COLOR,
                      command=self.gerar_lote).pack(side="left", padx=5)

        ctk.CTkButton(topo, text="Sortear",
                      fg_color=SUCCESS_COLOR,
                      command=self.sortear).pack(side="left", padx=5)

        ctk.CTkButton(topo, text="Verificar Cartela",
                      fg_color=DANGER_COLOR,
                      command=self.verificar_cartela).pack(side="left", padx=5)

        ctk.CTkButton(topo, text="Novo Jogo",
                      fg_color=WARNING_COLOR,
                      command=self.novo_sorteio).pack(side="left", padx=5)

        self.numero_label = ctk.CTkLabel(
            self.root, text="-", font=("Arial", 90, "bold")
        )
        self.numero_label.pack(pady=10)

        self.info = ctk.CTkLabel(self.root, text="Sorteados: 0 | Restantes: 75")
        self.info.pack()

        # ================= CENTRO COM SCROLL =================
        centro = ctk.CTkFrame(self.root)
        centro.pack(fill="both", expand=True, padx=10, pady=10)

        self.scroll = ctk.CTkScrollableFrame(centro)
        self.scroll.pack(side="left", fill="both", expand=True)

        direita = ctk.CTkFrame(centro, width=350)
        direita.pack(side="right", fill="y", padx=10)

        # ================= GRID BINGO =================
        self.labels = {}

        n = 1
        for r in range(15):
            for c in range(5):

                lbl = ctk.CTkLabel(
                    self.scroll,
                    text=formato_bingo(n),
                    width=70,
                    height=40,
                    fg_color=CARD_COLOR,
                    corner_radius=8
                )

                lbl.grid(row=r, column=c, padx=3, pady=3)
                self.labels[n] = lbl
                n += 1

        # ================= LISTA =================
        ctk.CTkLabel(direita, text="Últimos Sorteios",
                     font=("Arial", 18, "bold")).pack()

        self.lista = ctk.CTkTextbox(direita, width=300)
        self.lista.pack(fill="both", expand=True)

        # ================= RANKING =================
        ctk.CTkLabel(direita, text="Ranking Cartelas").pack()

        self.ranking = ctk.CTkTextbox(direita, height=200)
        self.ranking.pack(fill="x")

    # ================= GERAR CARTELAS =================
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

            messagebox.showinfo("OK", "Cartelas geradas!")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ================= SORTEIO =================
    def sortear(self):

        if not self.disponiveis:
            messagebox.showinfo("Fim", "Todos os números foram sorteados.")
            return

        numero = secrets.choice(self.disponiveis)

        self.disponiveis.remove(numero)
        self.sorteados.append(numero)

        texto = formato_bingo(numero)

        self.numero_label.configure(text=texto)

        self.labels[numero].configure(fg_color=SUCCESS_COLOR)

        self.lista.insert("1.0", f"{texto}\n")

        self.info.configure(
            text=f"Sorteados: {len(self.sorteados)} | Restantes: {len(self.disponiveis)}"
        )

        # 🔊 VOZ
        falar(texto)

        # 📊 atualiza ranking
        self.atualizar_ranking()

    # ================= RANKING =================
    def atualizar_ranking(self):

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

    # ================= NOVO JOGO =================
    def novo_sorteio(self):

        self.sorteados.clear()
        self.disponiveis = list(range(1, 76))

        self.numero_label.configure(text="-")

        self.lista.delete("1.0", "end")
        self.ranking.delete("1.0", "end")

        for lbl in self.labels.values():
            lbl.configure(fg_color=CARD_COLOR)

    # ================= VERIFICAR CARTELA (VISUAL) =================
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

            self.abrir_cartela_visual(numero, json.loads(row[0]))

        except:
            pass

    # ================= VISUAL =================
    def abrir_cartela_visual(self, numero, numeros):

        janela = ctk.CTkToplevel(self.root)
        janela.title(f"Cartela {numero}")
        janela.geometry("500x600")

        ctk.CTkLabel(
            janela,
            text=f"Cartela {numero}",
            font=("Arial", 22, "bold")
        ).pack(pady=10)

        frame = ctk.CTkFrame(janela)
        frame.pack()

        numeros = set(numeros)
        sorteados = set(self.sorteados)

        lista = sorted(list(numeros))

        i = 0

        for r in range(5):
            for c in range(5):

                if r == 2 and c == 2:
                    lbl = ctk.CTkLabel(frame, text="X", fg_color="#333", width=70, height=50)
                    lbl.grid(row=r, column=c, padx=5, pady=5)
                    continue

                if i >= len(lista):
                    continue

                val = lista[i]
                i += 1

                marcado = val in sorteados

                lbl = ctk.CTkLabel(
                    frame,
                    text=str(val),
                    width=70,
                    height=50,
                    fg_color=SUCCESS_COLOR if marcado else CARD_COLOR
                )
                lbl.grid(row=r, column=c, padx=5, pady=5)


if __name__ == "__main__":
    root = ctk.CTk()
    app = BingoProfissional(root)
    root.mainloop()