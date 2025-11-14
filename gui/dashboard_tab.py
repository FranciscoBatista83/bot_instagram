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

        # 🎬 Configurações de Reels
        self.reels_config_title = ctk.CTkLabel(
            self.config_frame,
            text="🎬 Configurações de Reels",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.reels_config_title.grid(
            row=0, column=1, columnspan=2, pady=(15, 10), sticky="n"
        )

        # Reels por perfil
        self.reels_per_profile_label = ctk.CTkLabel(
            self.config_frame,
            text="Reels por perfil:",
            font=ctk.CTkFont(size=14),
        )
        self.reels_per_profile_label.grid(row=1, column=1, pady=(5, 5), sticky="ew")

        self.reels_per_profile_entry = ctk.CTkEntry(
            self.config_frame,
            placeholder_text="3",
            width=200,
        )
        self.reels_per_profile_entry.grid(
            row=1, column=2, padx=15, pady=(0, 10), sticky="ew"
        )

        # Pausa mínima entre perfis
        self.pause_min_profiles_label = ctk.CTkLabel(
            self.config_frame,
            text="Pausa min entre perfis (minutos):",
            font=ctk.CTkFont(size=14),
        )
        self.pause_min_profiles_label.grid(row=2, column=1, pady=(5, 5), sticky="ew")

        self.pause_min_profiles_entry = ctk.CTkEntry(
            self.config_frame,
            width=200,
        )
        self.pause_min_profiles_entry.grid(
            row=2, column=2, padx=15, pady=(0, 10), sticky="ew"
        )

        # Pausa máxima entre perfis
        self.pause_max_profiles_label = ctk.CTkLabel(
            self.config_frame,
            text="Pausa max entre perfis (minutos):",
            font=ctk.CTkFont(size=14),
        )
        self.pause_max_profiles_label.grid(row=3, column=1, pady=(5, 5), sticky="ew")

        self.pause_max_profiles_entry = ctk.CTkEntry(
            self.config_frame,
            width=200,
        )
        self.pause_max_profiles_entry.grid(
            row=3, column=2, padx=15, pady=(0, 15), sticky="ew"
        )

        # Botão salvar configurações
        self.save_reels_config_button = ctk.CTkButton(
            self.config_frame,
            text="💾 Salvar Configurações",
            command=self.save_reels_configs_action,
            fg_color="orange",
            height=35,
        )
        self.save_reels_config_button.grid(
            row=4, column=1, columnspan=2, padx=15, pady=(5, 15), sticky="ew"
        )

        # Status das configurações
        self.status_label = ctk.CTkLabel(self, text="", text_color="green")
        self.status_label.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Carregar configurações dos reels
        self.load_reels_configs()

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

    def load_reels_configs(self):
        """Carrega as configurações dos reels do arquivo JSON (converte segundos para minutos na interface)."""
        config_file = os.path.join(os.path.dirname(__file__), "..", "bot_configs.json")

        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    configs = json.load(f)

                # Carregar reels por perfil
                if "reels_per_profile" in configs:
                    self.reels_per_profile_entry.delete(0, "end")
                    self.reels_per_profile_entry.insert(0, str(configs["reels_per_profile"]))

                # Carregar pausa mínima entre perfis (converter segundos para minutos)
                if "pause_min_profiles" in configs:
                    minutos_min = configs["pause_min_profiles"] / 60.0
                    self.pause_min_profiles_entry.delete(0, "end")
                    self.pause_min_profiles_entry.insert(0, f"{minutos_min:.2f}")

                # Carregar pausa máxima entre perfis (converter segundos para minutos)
                if "pause_max_profiles" in configs:
                    minutos_max = configs["pause_max_profiles"] / 60.0
                    self.pause_max_profiles_entry.delete(0, "end")
                    self.pause_max_profiles_entry.insert(0, f"{minutos_max:.2f}")

            except Exception as e:
                print(f"Erro ao carregar configurações dos reels: {e}")

    def save_reels_configs(self):
        """Salva as configurações dos reels em um arquivo JSON (converte minutos para segundos)."""
        config_file = os.path.join(os.path.dirname(__file__), "..", "bot_configs.json")

        try:
            # Carregar configurações existentes ou criar dicionário vazio
            if os.path.exists(config_file):
                with open(config_file, "r") as f:
                    configs = json.load(f)
            else:
                configs = {}

            # Atualizar configurações dos reels
            configs["reels_per_profile"] = int(self.reels_per_profile_entry.get() or 3)

            # Converter minutos para segundos (pausas)
            minutos_min = float(self.pause_min_profiles_entry.get() or 0.17)
            configs["pause_min_profiles"] = int(minutos_min * 60)

            minutos_max = float(self.pause_max_profiles_entry.get() or 0.5)
            configs["pause_max_profiles"] = int(minutos_max * 60)

            # Salvar no arquivo
            with open(config_file, "w") as f:
                json.dump(configs, f, indent=4)

            return True
        except Exception as e:
            print(f"Erro ao salvar configurações dos reels: {e}")
            return False

    def save_reels_configs_action(self):
        """Ação do botão salvar configurações dos reels."""
        if self.save_reels_configs():
            self.status_label.configure(
                text="✅ Configurações dos reels salvas com sucesso!", text_color="green"
            )
        else:
            self.status_label.configure(
                text="❌ Erro ao salvar configurações dos reels!", text_color="red"
            )
