
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3, random, json

DB="bingo_profissional.db"

class Bingo:
    def __init__(self, root):
        self.root=root
        self.root.title("Bingo Profissional")
        self.root.geometry("1300x800")

        self.sorteados=[]
        self.disponiveis=list(range(1,76))

        self.db()
        self.ui()

    def db(self):
        con=sqlite3.connect(DB)
        cur=con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS cartelas(
            numero INTEGER PRIMARY KEY,
            numeros TEXT NOT NULL
        )""")
        con.commit(); con.close()

    def ui(self):
        top=tk.Frame(self.root); top.pack(fill="x", pady=5)

        tk.Button(top,text="Gerar Lote",command=self.gerar_lote).pack(side="left",padx=3)
        tk.Button(top,text="Sortear",command=self.sortear,bg="green",fg="white").pack(side="left",padx=3)
        tk.Button(top,text="Novo Sorteio",command=self.novo_sorteio).pack(side="left",padx=3)
        tk.Button(top,text="Verificar Cartela",command=self.verificar).pack(side="left",padx=3)

        self.lbl=tk.Label(self.root,text="-",font=("Arial",70,"bold"))
        self.lbl.pack()

        self.info=tk.Label(self.root,text="Sorteados: 0 | Restantes: 75")
        self.info.pack()

        main=tk.Frame(self.root); main.pack(fill="both",expand=True)

        painel=tk.Frame(main)
        painel.pack(side="left",padx=10)

        self.labels={}
        n=1
        for r in range(15):
            for c in range(5):
                if n<=75:
                    lb=tk.Label(painel,text=f"{n:02}",width=5,height=2,relief="ridge")
                    lb.grid(row=r,column=c,padx=1,pady=1)
                    self.labels[n]=lb
                    n+=1

        right=tk.Frame(main)
        right.pack(side="right",fill="both",expand=True)

        tk.Label(right,text="Últimos sorteados").pack()

        self.lst=tk.Listbox(right,font=("Arial",12))
        self.lst.pack(fill="both",expand=True)

    def gerar_lote(self):
        try:
            inicio=int(simpledialog.askstring("Início","Número inicial da cartela"))
            fim=int(simpledialog.askstring("Fim","Número final da cartela"))

            con=sqlite3.connect(DB)
            cur=con.cursor()

            total=0
            for cartela in range(inicio,fim+1):
                nums=sorted(random.sample(range(1,76),24))
                cur.execute(
                    "INSERT OR REPLACE INTO cartelas(numero,numeros) VALUES (?,?)",
                    (cartela,json.dumps(nums))
                )
                total+=1

            con.commit(); con.close()

            messagebox.showinfo("Sucesso",f"{total} cartelas geradas.")
        except Exception as e:
            messagebox.showerror("Erro",str(e))

    def sortear(self):
        if not self.disponiveis:
            messagebox.showinfo("Fim","Todos os números foram sorteados.")
            return

        n=random.choice(self.disponiveis)
        self.disponiveis.remove(n)
        self.sorteados.append(n)

        self.lbl.config(text=str(n))
        self.labels[n].config(bg="green",fg="white")

        self.lst.insert(0,f"{n:02}")
        self.info.config(
            text=f"Sorteados: {len(self.sorteados)} | Restantes: {len(self.disponiveis)}"
        )

    def novo_sorteio(self):
        self.sorteados.clear()
        self.disponiveis=list(range(1,76))

        for lb in self.labels.values():
            lb.config(bg="SystemButtonFace",fg="black")

        self.lst.delete(0,tk.END)
        self.lbl.config(text="-")
        self.info.config(text="Sorteados: 0 | Restantes: 75")

    def verificar(self):
        try:
            numero=int(simpledialog.askstring("Verificar","Número da cartela"))

            con=sqlite3.connect(DB)
            cur=con.cursor()
            cur.execute(
                "SELECT numeros FROM cartelas WHERE numero=?",
                (numero,)
            )
            row=cur.fetchone()
            con.close()

            if not row:
                messagebox.showerror("Erro","Cartela não encontrada.")
                return

            cartela=set(json.loads(row[0]))
            faltantes=sorted(cartela-set(self.sorteados))

            if len(faltantes)==0:
                messagebox.showinfo(
                    "BINGO CONFIRMADO",
                    f"Cartela vencedora: {numero}"
                )
            else:
                messagebox.showwarning(
                    "Bingo inválido",
                    f"Faltam {len(faltantes)} números:\n\n{faltantes}"
                )
        except:
            pass

if __name__=="__main__":
    root=tk.Tk()
    Bingo(root)
    root.mainloop()
