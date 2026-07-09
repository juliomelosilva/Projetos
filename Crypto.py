import os
import hashlib
from tkinter import filedialog, messagebox
import customtkinter as ctk
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Configurações de tema da interface
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class CriptografadorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Joker Crypt - Criptografia em Massa")
        self.geometry("600x450")
        self.resizable(False, False)

        # Definição da senha padrão e geração da chave AES-256 (32 bytes)
        self.SENHA_PADRAO = "joker@1090"
        self.key = hashlib.sha256(self.SENHA_PADRAO.encode()).digest()
        
        self.arquivos_selecionados = []
        self.criar_interface()

    def criar_interface(self):
        # Título principal
        self.lbl_titulo = ctk.CTkLabel(self, text="🔑 JOKER CRYPT", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_titulo.pack(pady=20)

        # Frame de seleção de arquivos
        self.btn_selecionar = ctk.CTkButton(self, text="Selecionar Arquivos em Massa", command=self.selecionar_arquivos)
        self.btn_selecionar.pack(pady=10)

        self.lbl_status = ctk.CTkLabel(self, text="Nenhum arquivo selecionado.", font=ctk.CTkFont(size=12))
        self.lbl_status.pack(pady=5)

        # Campo de Senha para validação
        self.lbl_senha = ctk.CTkLabel(self, text="Digite a senha para prosseguir:")
        self.lbl_senha.pack(pady=(20, 5))
        
        self.txt_senha = ctk.CTkEntry(self, show="*", width=300, placeholder_text="Senha de segurança")
        self.txt_senha.pack(pady=5)

        # Barra de progresso (oculta inicialmente)
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=15)
        self.progress_bar.pack_forget()

        # Frame para os botões de ação
        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.pack(pady=20, fill="x", padx=50)

        self.btn_criptografar = ctk.CTkButton(self.frame_botoes, text="Criptografar", fg_color="#2baf2b", hover_color="#218c21", command=lambda: self.processar_arquivos(acao="criptografar"))
        self.btn_criptografar.pack(side="left", expand=True, padx=10)

        self.btn_descriptografar = ctk.CTkButton(self.frame_botoes, text="Descriptografar", fg_color="#d32f2f", hover_color="#9a1f1f", command=lambda: self.processar_arquivos(acao="descriptografar"))
        self.btn_descriptografar.pack(side="right", expand=True, padx=10)

    def selecionar_arquivos(self):
        arquivos = filedialog.askopenfilenames(title="Selecione os arquivos")
        if arquivos:
            self.arquivos_selecionados = list(arquivos)
            self.lbl_status.configure(text=f"{len(self.arquivos_selecionados)} arquivo(s) selecionado(s).")
            self.progress_bar.set(0)
            self.progress_bar.pack_forget()

    def validar_senha(self):
        return self.txt_senha.get() == self.SENHA_PADRAO

    def pad(self, data):
        # Preenchimento PKCS7 para alinhar aos blocos do AES (16 bytes)
        block_size = 16
        padding_len = block_size - (len(data) % block_size)
        return data + bytes([padding_len] * padding_len)

    def unpad(self, data):
        padding_len = data[-1]
        return data[:-padding_len]

    def criptografar_arquivo(self, caminho_arquivo):
        try:
            if caminho_arquivo.endswith(".joker"):
                return True # Já está criptografado

            with open(caminho_arquivo, "rb") as f:
                dados_originais = f.read()

            # Gera um Vetor de Inicialização (IV) aleatório para segurança
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            
            dados_criptografados = encryptor.update(self.pad(dados_originais)) + encryptor.finalize()

            # Salva o arquivo final: IV (16 bytes) + Conteúdo Criptografado
            with open(caminho_arquivo + ".joker", "wb") as f:
                f.write(iv + dados_criptografados)

            os.remove(caminho_arquivo)
            return True
        except Exception as e:
            print(f"Erro ao criptografar {caminho_arquivo}: {e}")
            return False

    def descriptografar_arquivo(self, caminho_arquivo):
        try:
            if not caminho_arquivo.endswith(".joker"):
                return True # Não é um arquivo criptografado pelo app

            with open(caminho_arquivo, "rb") as f:
                dados_arquivo = f.read()

            # Separa o IV dos dados criptografados
            iv = dados_arquivo[:16]
            dados_criptografados = dados_arquivo[16:]

            cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            
            dados_finais = decryptor.update(dados_criptografados) + decryptor.finalize()
            dados_originais = self.unpad(dados_finais)

            caminho_original = caminho_arquivo.replace(".joker", "")
            with open(caminho_original, "wb") as f:
                f.write(dados_originais)

            os.remove(caminho_arquivo)
            return True
        except Exception as e:
            print(f"Erro ao descriptografar {caminho_arquivo}: {e}")
            return False

    def processar_arquivos(self, acao):
        if not self.arquivos_selecionados:
            messagebox.showwarning("Aviso", "Por favor, selecione pelo menos um arquivo.")
            return

        if not self.validar_senha():
            messagebox.showerror("Erro de Autenticação", "Senha incorreta! Acesso negado.")
            return

        self.progress_bar.pack(pady=15)
        sucessos = 0
        total = len(self.arquivos_selecionados)

        # Cria uma lista cópia para manipular caminhos que vão mudar de nome
        novos_caminhos = []

        for i, caminho in enumerate(self.arquivos_selecionados):
            if acao == "criptografar":
                if self.criptografar_arquivo(caminho):
                    sucessos += 1
                    novos_caminhos.append(caminho + ".joker")
            elif acao == "descriptografar":
                if self.descriptografar_arquivo(caminho):
                    sucessos += 1
                    novos_caminhos.append(caminho.replace(".joker", ""))
            
            # Atualiza a barra de progresso visualmente
            self.progress_bar.set((i + 1) / total)
            self.update_idletasks()

        # Atualiza a lista interna para refletir o novo estado dos arquivos
        self.arquivos_selecionados = novos_caminhos
        self.lbl_status.configure(text="Operação concluída com sucesso!")
        
        messagebox.showinfo("Sucesso", f"Processo concluído!\n{sucessos} de {total} arquivos foram processados.")

if __name__ == "__main__":
    app = CriptografadorApp()
    app.mainloop()