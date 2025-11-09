import customtkinter as ctk
import os
import json


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

        self.bot_config_title = ctk.CTkLabel(
            self.config_frame,
            text="Configurações dos Bots",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.bot_config_title.grid(
            row=0, column=1, columnspan=2, pady=(10, 10), sticky="n"
        )

        self.max_followers_label = ctk.CTkLabel(
            self.config_frame,
            text="Quantidade máxima de seguidores a extrair:",
            font=ctk.CTkFont(size=20),
        )
        self.max_followers_label.grid(row=1, column=1, pady=(5, 5), sticky="ew")

        self.max_followers_entry = ctk.CTkEntry(
            self.config_frame, placeholder_text="0 = extrair todos", width=250
        )
        self.max_followers_entry.grid(
            row=1, column=2, padx=15, pady=(0, 10), sticky="ew"
        )

        self.max_reels_label = ctk.CTkLabel(
            self.config_frame,
            text="Máximo de reels a serem curtidos por perfil:",
            font=ctk.CTkFont(size=20),
        )
        self.max_reels_label.grid(row=2, column=1, pady=(5, 5), sticky="ew")

        self.max_reels_entry = ctk.CTkEntry(
            self.config_frame,
            placeholder_text="Digite o número máximo (0 = todos)",
            width=250,
        )
        self.max_reels_entry.grid(row=2, column=2, padx=15, pady=(0, 10), sticky="ew")

        self.save_bot_config_button = ctk.CTkButton(
            self.config_frame,
            text="Salvar Configurações",
            command=self.save_bot_configs_action,
            fg_color="orange",
        )
        self.save_bot_config_button.grid(
            row=3, column=1, columnspan=2, padx=15, pady=(10, 10), sticky="ew"
        )

        # Status das configurações
        self.status_label = ctk.CTkLabel(self, text="", text_color="green")
        self.status_label.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Carregar configurações salvas
        self.load_bot_configs()

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

    def save_bot_configs(self):
        """Salva as configurações dos bots em um arquivo JSON."""
        config_file = os.path.join(os.path.dirname(__file__), "..", "bot_configs.json")

        configs = {
            "max_followers": self.max_followers_entry.get(),
            "max_reels_per_profile": self.max_reels_entry.get(),
        }

        try:
            with open(config_file, "w") as f:
                json.dump(configs, f, indent=4)
            return True
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
            return False

    def load_bot_configs(self):
        """Carrega as configurações dos bots do arquivo JSON."""
        config_file = os.path.join(os.path.dirname(__file__), "..", "bot_configs.json")

        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    configs = json.load(f)

                # Carregar limite de seguidores
                if "max_followers" in configs:
                    self.max_followers_entry.delete(0, "end")
                    self.max_followers_entry.insert(0, str(configs["max_followers"]))

                # Carregar limite de reels por perfil
                if "max_reels_per_profile" in configs:
                    self.max_reels_entry.delete(0, "end")
                    self.max_reels_entry.insert(
                        0, str(configs["max_reels_per_profile"])
                    )

            except Exception as e:
                print(f"Erro ao carregar configurações: {e}")

    def save_bot_configs_action(self):
        """Ação do botão salvar configurações dos bots."""
        if self.save_bot_configs():
            self.status_label.configure(
                text="Configurações dos bots salvas!", text_color="green"
            )
        else:
            self.status_label.configure(
                text="Erro ao salvar configurações!", text_color="red"
            )

    def get_max_followers_config(self):
        """Retorna o limite máximo de seguidores configurado."""
        try:
            value = self.max_followers_entry.get().strip()
            return int(value) if value else 0
        except ValueError:
            return 0

    def get_max_reels_config(self):
        """Retorna o limite máximo de reels por perfil configurado."""
        try:
            value = self.max_reels_entry.get().strip()
            return int(value) if value else 0
        except ValueError:
            return 0
