import customtkinter as ctk
import os


class DashboardTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Configurar grid com 1 coluna
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        # Título principal
        self.label = ctk.CTkLabel(
            self, text="Dashboard", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # Status da conta
        self.account_frame = ctk.CTkFrame(self)
        self.account_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.account_frame.grid_columnconfigure(0, weight=1)

        self.account_title = ctk.CTkLabel(
            self.account_frame, text="Status da Conta", font=ctk.CTkFont(weight="bold")
        )
        self.account_title.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="w")

        self.account_status_label = ctk.CTkLabel(
            self.account_frame, text="Nenhuma conta logada", text_color="orange"
        )
        self.account_status_label.grid(
            row=1, column=0, padx=15, pady=(0, 10), sticky="w"
        )

        # Configurações dos Bots
        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Configurar três colunas para centralizar o conteúdo
        self.config_frame.grid_columnconfigure(0, weight=1)  # margem esquerda
        self.config_frame.grid_columnconfigure(1, weight=0)  # conteúdo principal
        self.config_frame.grid_columnconfigure(2, weight=0)
        self.config_frame.grid_columnconfigure(3, weight=1)  # margem direita

        # Status das configurações
        self.status_label = ctk.CTkLabel(self, text="", text_color="green")
        self.status_label.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Atualizar status da conta quando o username mudar
        if hasattr(master, "logged_username"):
            master.logged_username.trace_add("write", self.update_account_status)

    def update_account_status(self, *args):
        """Atualiza o status da conta quando o username muda."""
        username = self.master.logged_username.get()
        if username:
            self.account_status_label.configure(
                text=f"Status da Conta: Logado como @{username}", text_color="green"
            )
        else:
            self.account_status_label.configure(
                text="Status da Conta: Nenhuma conta logada", text_color="orange"
            )
