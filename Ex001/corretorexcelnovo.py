import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import re
import os

class CorretorCaracteresEspeciais:
    def __init__(self, root):
        self.root = root
        self.root.title("Corretor de Caracteres Especiais")

        self.arquivo_selecionado = None
        self.caracteres_especiais = set()

        self.criar_interface()

    def criar_interface(self):
        # Botão para selecionar arquivo
        self.botao_selecionar_arquivo = tk.Button(self.root, text="Selecionar Arquivo", command=self.selecionar_arquivo)
        self.botao_selecionar_arquivo.pack(pady=10)

        # Label para exibir o caminho do arquivo selecionado
        self.label_caminho_arquivo = tk.Label(self.root, text="")
        self.label_caminho_arquivo.pack()

        # Botão para corrigir o arquivo
        self.botao_corrigir = tk.Button(self.root, text="Corrigir", command=self.corrigir_arquivo)
        self.botao_corrigir.pack(pady=10)

        # Área para exibir caracteres especiais encontrados
        self.label_caracteres_especiais = tk.Label(self.root, text="Caracteres Especiais Encontrados:")
        self.label_caracteres_especiais.pack()

        self.texto_caracteres_especiais = tk.Text(self.root, height=10, width=50)
        self.texto_caracteres_especiais.pack()

    def selecionar_arquivo(self):
        self.arquivo_selecionado = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.csv;*.xls;*.xlsx")])
        if self.arquivo_selecionado:
            self.label_caminho_arquivo.config(text=f"Arquivo Selecionado: {self.arquivo_selecionado}")
            self.botao_corrigir["state"] = "normal"

    def corrigir_arquivo(self):
        if not self.arquivo_selecionado:
            return

        # Ler o arquivo Excel
        try:
            df = pd.read_excel(self.arquivo_selecionado) if self.arquivo_selecionado.endswith(('.xls', '.xlsx')) else pd.read_csv(self.arquivo_selecionado)
        except pd.errors.EmptyDataError:
            self.mostrar_mensagem_erro("O arquivo está vazio.")
            return
        except Exception as e:
            self.mostrar_mensagem_erro(f"Erro ao ler o arquivo: {e}")
            return

        # Corrigir caracteres especiais
        for coluna in df.columns:
            df[coluna] = df[coluna].apply(lambda x: self.remover_caracteres_especiais(x) if isinstance(x, str) else x)

        # Exibir caracteres especiais encontrados
        self.caracteres_especiais = set(self.caracteres_especiais)
        texto_resultado = "\n".join(self.caracteres_especiais)
        self.texto_caracteres_especiais.delete(1.0, tk.END)
        self.texto_caracteres_especiais.insert(tk.END, texto_resultado)

        # Salvar o arquivo corrigido
        arquivo_saida = self.salvar_arquivo_corrigido(df)

        if arquivo_saida:
            messagebox.showinfo("Concluído", f"Correção concluída e arquivo salvo em:\n{arquivo_saida}")

    def remover_caracteres_especiais(self, texto):
        if isinstance(texto, str):
            caracteres_especiais = re.findall(r"[^a-zA-Z0-9\s,]", texto)
            self.caracteres_especiais.update(caracteres_especiais)
            # Preservar espaços, vírgulas em números e pontos em números decimais
            texto_corrigido = re.sub(r"[^a-zA-Z0-9\s,.]", "", texto)
            return texto_corrigido
        else:
            return texto

    def salvar_arquivo_corrigido(self, df):
        nome_arquivo, extensao = os.path.splitext(os.path.basename(self.arquivo_selecionado))
        arquivo_saida = filedialog.asksaveasfilename(defaultextension=extensao, filetypes=[("Arquivos Excel", "*.xls;*.xlsx"), ("Arquivos CSV", "*.csv")])

        if arquivo_saida:
            try:
                if arquivo_saida.endswith(('.xls', '.xlsx')):
                    df.to_excel(arquivo_saida, index=False)
                elif arquivo_saida.endswith('.csv'):
                    df.to_csv(arquivo_saida, index=False)
                return arquivo_saida
            except Exception as e:
                self.mostrar_mensagem_erro(f"Erro ao salvar o arquivo: {e}")
                return None
        else:
            return None

    def mostrar_mensagem_erro(self, mensagem):
        messagebox.showerror("Erro", mensagem)

if __name__ == "__main__":
    root = tk.Tk()
    app = CorretorCaracteresEspeciais(root)
    root.mainloop()