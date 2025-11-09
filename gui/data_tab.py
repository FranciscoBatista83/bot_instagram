import customtkinter as ctk
import os
from core.file_manager import ler_urls_arquivo

class DataTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.logged_username_var = master.logged_username  # Referência ao username logado

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) # 3 linhas para labels, textbox e botão

        self.label = ctk.CTkLabel(self, text="Dados dos Perfis", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.account_file_label = ctk.CTkLabel(self, text="Arquivo: Nenhum", text_color="orange")
        self.account_file_label.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.data_textbox = ctk.CTkTextbox(self, width=700, height=400, state="disabled")
        self.data_textbox.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.load_data_button = ctk.CTkButton(self, text="Recarregar Dados", command=self.load_data)
        self.load_data_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # Atualizar label do arquivo quando o username mudar
        self.logged_username_var.trace_add("write", self.update_file_label)

        self.load_data()

    def update_file_label(self, *args):
        """Atualiza o label do arquivo quando o username muda."""
        username = self.logged_username_var.get()
        if username:
            self.account_file_label.configure(text=f"Arquivo: seguidores_{username}.txt", text_color="green")
        else:
            self.account_file_label.configure(text="Arquivo: Nenhum", text_color="orange")

    def load_data(self):
        self.data_textbox.configure(state="normal")
        self.data_textbox.delete("1.0", ctk.END)

        username = self.logged_username_var.get()
        if username:
            file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), f'seguidores_{username}.txt')
            file_name = f'seguidores_{username}.txt'
        else:
            # Quando não há conta logada, mostrar mensagem explicativa
            self.data_textbox.insert(ctk.END, "📁 Sistema de Arquivos por Conta\n\n")
            self.data_textbox.insert(ctk.END, "Cada conta do Instagram possui seu próprio arquivo de seguidores:\n")
            self.data_textbox.insert(ctk.END, "• seguidores_{nome_da_conta}.txt\n\n")
            self.data_textbox.insert(ctk.END, "Para visualizar os dados:\n")
            self.data_textbox.insert(ctk.END, "1. Vá para a aba 'Credenciais & Config'\n")
            self.data_textbox.insert(ctk.END, "2. Preencha usuário e senha\n")
            self.data_textbox.insert(ctk.END, "3. Clique em 'Fazer Login'\n")
            self.data_textbox.insert(ctk.END, "4. Vá para 'Ações do Bot' e clique em 'Extrair Seguidores'\n\n")
            self.data_textbox.insert(ctk.END, "O arquivo será criado automaticamente! 🎯")
            return

        if os.path.exists(file_path):
            urls = ler_urls_arquivo(file_path)
            if urls:
                self.data_textbox.insert(ctk.END, f"📄 Arquivo: {file_name}\n")
                self.data_textbox.insert(ctk.END, f"👥 Total de perfis: {len(urls)}\n\n")
                for url in urls:
                    self.data_textbox.insert(ctk.END, url + "\n")
            else:
                self.data_textbox.insert(ctk.END, f"📄 Arquivo: {file_name}\n")
                self.data_textbox.insert(ctk.END, "📭 Nenhum perfil encontrado.\n")
                self.data_textbox.insert(ctk.END, "Use 'Extrair Seguidores' para popular este arquivo.\n")
        else:
            self.data_textbox.insert(ctk.END, f"📄 Arquivo: {file_name}\n")
            self.data_textbox.insert(ctk.END, "📭 Arquivo ainda não foi criado.\n")
            self.data_textbox.insert(ctk.END, "Será criado automaticamente quando você extrair seguidores desta conta.\n")

        self.data_textbox.configure(state="disabled")
