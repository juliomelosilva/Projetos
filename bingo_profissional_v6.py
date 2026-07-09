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
TEXT_COLOR = "#F9FAFA"

DB = "bingo_v3.db"

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

        # ================= CENTRO =================
        centro = ctk.CTkFrame(self.root)
        centro.pack(fill="both", expand=True, padx=10, pady=10)

        self.scroll = ctk.CTkScrollableFrame(centro)
        self.scroll.pack(side="left", fill="both", expand=True)

        direita = ctk.CTkFrame(centro, width=350)
        direita.pack(side="right", fill="y", padx=10)

        # ================= HEADER BINGO PRINCIPAL =================
        header = ctk.CTkFrame(self.scroll)
        header.grid(row=0, column=0, columnspan=5, pady=(0, 10))

        for i, letra in enumerate(["B", "I", "N", "G", "O"]):
            ctk.CTkLabel(
                header,
                text=letra,
                width=70,
                font=("Arial", 18, "bold"),
                text_color=TEXT_COLOR
            ).grid(row=0, column=i, padx=3)

        # ================= GRID PRINCIPAL =================
        self.labels = {}

        for r in range(15):
            for c in range(5):
                n = c * 15 + (r + 1)

                lbl = ctk.CTkLabel(
                    self.scroll,
                    text=formato_bingo(n),
                    width=70,
                    height=40,
                    fg_color=CARD_COLOR,
                    corner_radius=8
                )

                lbl.grid(row=r + 1, column=c, padx=3, pady=3)
                self.labels[n] = lbl

        # ================= LISTA E BUSCA =================
        ctk.CTkLabel(direita, text="Últimos Sorteios",
                     font=("Arial", 18, "bold")).pack(pady=(5, 0))

        frame_busca = ctk.CTkFrame(direita)
        frame_busca.pack(fill="x", padx=10, pady=5)
        
        self.entry_busca = ctk.CTkEntry(frame_busca, placeholder_text="Buscar número...")
        self.entry_busca.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        btn_busca = ctk.CTkButton(frame_busca, text="🔍", width=40, command=self.buscar_no_sorteio)
        btn_busca.pack(side="right")

        self.lista = ctk.CTkTextbox(direita, width=300)
        self.lista.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkLabel(direita, text="Ranking Cartelas", font=("Arial", 14, "bold")).pack(pady=(5, 0))

        self.ranking = ctk.CTkTextbox(direita, height=200)
        self.ranking.pack(fill="x", padx=10, pady=5)

    # ================= FUNÇÃO DE BUSCA =================
    def buscar_no_sorteio(self):
        termo = self.entry_busca.get().strip().upper()
        if not termo:
            return

        apenas_numero = "".join(c for c in termo if c.isdigit())
        
        if not apenas_numero:
            messagebox.showwarning("Busca", "Digite um número válido para buscar.")
            return
        
        num_int = int(apenas_numero)
        
        if num_int in self.sorteados:
            texto_formatado = formato_bingo(num_int)
            messagebox.showinfo("Encontrado!", f"O número {texto_formatado} JÁ foi sorteado!")
        else:
            messagebox.showinfo("Não encontrado", f"O número {termo} AINDA NÃO foi sorteado.")

    # ================= GERAR CARTELAS (CORRIGIDO PARA REGRAS REAIS) =================
    def gerar_lote(self):
        try:
            inicio = int(simpledialog.askstring("Início", "Cartela inicial"))
            fim = int(simpledialog.askstring("Fim", "Cartela final"))

            con = sqlite3.connect(DB)
            cur = con.cursor()

            rng = secrets.SystemRandom()

            for numero in range(inicio, fim + 1):
                # Gera números únicos e ordenados por coluna seguindo as faixas oficiais
                b = sorted(rng.sample(range(1, 16), 5))
                i = sorted(rng.sample(range(16, 31), 5))
                n = sorted(rng.sample(range(31, 46), 4)) # Apenas 4 na do meio por causa do FREE
                g = sorted(rng.sample(range(46, 60), 5))
                o = sorted(rng.sample(range(61, 76), 5))

                # Junta tudo em uma estrutura de dicionário mapeada por colunas
                cartela_dados = {
                    "0": b,
                    "1": i,
                    "2": n,
                    "3": g,
                    "4": o
                }

                cur.execute(
                    "INSERT OR REPLACE INTO cartelas VALUES (?,?)",
                    (numero, json.dumps(cartela_dados))
                )

            con.commit()
            con.close()

            messagebox.showinfo("OK", "Cartelas geradas seguindo o padrão oficial BINGO!")

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

        self.atualizar_ranking()

    # ================= RANKING (CORRIGIDO) =================
    def atualizar_ranking(self):

        con = sqlite3.connect(DB)
        cur = con.cursor()

        cur.execute("SELECT numero,numeros FROM cartelas")

        ranking = []
        sorteados = set(self.sorteados)

        for numero, numeros_json in cur.fetchall():
            cartela_dados = json.loads(numeros_json)
            
            # Se o banco possuir o formato antigo (lista simples), ignora ou trata como vazio
            if isinstance(cartela_dados, list):
                all_nums = set(cartela_dados)
            else:
                all_nums = set()
                for col in cartela_dados.values():
                    all_nums.update(col)

            acertos = len(all_nums & sorteados)
            faltam = len(all_nums - sorteados)

            if acertos == 24:
                faltam = 0

            ranking.append((numero, faltam, acertos))

        con.close()

        ranking.sort(key=lambda x: (x[1], -x[2]))
        self.ranking.delete("1.0", "end")

        for num, faltam, acertos in ranking[:10]:
            self.ranking.insert(
                "end",
                f"Cartela {num} → faltam {faltam} | acertos {acertos}\n"
            )

    # ================= NOVO JOGO =================
    def novo_sorteio(self):

        self.sorteados.clear()
        self.disponiveis = list(range(1, 76))

        self.numero_label.configure(text="-")
        self.lista.delete("1.0", "end")
        self.ranking.delete("1.0", "end")
        self.entry_busca.delete(0, "end")

        for lbl in self.labels.values():
            lbl.configure(fg_color=CARD_COLOR)

    # ================= VERIFICAR CARTELA =================
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

            cartela_dados = json.loads(row[0])
            
            # Sanitização caso seja uma cartela antiga antiga no banco
            if isinstance(cartela_dados, list):
                messagebox.showwarning("Aviso", "Esta cartela foi gerada no formato antigo. Recomenda-se gerar novas cartelas.")
                return

            all_nums = set()
            for col in cartela_dados.values():
                all_nums.update(col)

            sorteados = set(self.sorteados)
            acertos = len(all_nums & sorteados)

            if acertos == 24:
                messagebox.showinfo("BINGO!", f"Cartela {numero} VENCEU!")
            else:
                messagebox.showwarning(
                    "Ainda não",
                    f"Cartela {numero} não venceu ainda.\nAcertos: {acertos}/24"
                )

            self.abrir_cartela_visual(numero, cartela_dados)

        except Exception as e:
            pass

    # ================= VISUAL CARTELA (ALINHADO COM CABEÇALHO B I N G O) =================
    def abrir_cartela_visual(self, numero, cartela_dados):

        janela = ctk.CTkToplevel(self.root)
        janela.title(f"BINGO - Cartela {numero}")
        janela.geometry("500x550")
        janela.lift()

        ctk.CTkLabel(
            janela,
            text=f"Cartela {numero}",
            font=("Arial", 20, "bold")
        ).pack(pady=(15, 5))

        frame = ctk.CTkFrame(janela)
        frame.pack(pady=10, padx=20)

        # Cabeçalho B I N G O idêntico à tela da esquerda
        for i, letra in enumerate(["B", "I", "N", "G", "O"]):
            ctk.CTkLabel(
                frame,
                text=letra,
                width=75,
                font=("Arial", 22, "bold"),
                text_color=TEXT_COLOR
            ).grid(row=0, column=i, padx=5, pady=(5, 15))

        sorteados = set(self.sorteados)

        # Monta o grid tradicional 5x5
        for r in range(5):
            for c in range(5):
                # Posição central (Linha 3, Coluna 3 -> índice 2, 2) fica em BRANCO / FREE
                if r == 2 and c == 2:
                    ctk.CTkLabel(
                        frame,
                        text="FREE",
                        width=75,
                        height=50,
                        font=("Arial", 12, "bold"),
                        fg_color="#333333",
                        corner_radius=6
                    ).grid(row=r + 1, column=c, padx=5, pady=5)
                    continue

                # Ajusta os índices da coluna N que só possui 4 números salvos
                col_key = str(c)
                if c == 2:
                    idx_num = r if r < 2 else r - 1
                    val = cartela_dados[col_key][idx_num]
                else:
                    val = cartela_dados[col_key][r]

                marcado = val in sorteados

                ctk.CTkLabel(
                    frame,
                    text=str(val),
                    width=75,
                    height=50,
                    font=("Arial", 14, "bold"),
                    text_color=TEXT_COLOR,
                    fg_color=SUCCESS_COLOR if marcado else CARD_COLOR,
                    corner_radius=6
                ).grid(row=r + 1, column=c, padx=5, pady=5)


if __name__ == "__main__":
    root = ctk.CTk()
    app = BingoProfissional(root)
    root.mainloop()