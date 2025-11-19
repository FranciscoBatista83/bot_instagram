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
            self, text="Painel de Controle", font=ctk.CTkFont(size=20, weight="bold")
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

        # Configurações dos Bots - Usando abas para organização
        self.config_tabview = ctk.CTkTabview(self, width=600, height=300)
        self.config_tabview.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Criar abas
        self.config_tabview.add("Videos")
        self.config_tabview.add("Deixar de Seguir")
        self.config_tabview.add("Seguir")

        # Configurar abas para centralizar conteúdo
        for tab_name in ["Videos", "Deixar de Seguir", "Seguir"]:
            tab = self.config_tabview.tab(tab_name)
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_columnconfigure(1, weight=0)
            tab.grid_columnconfigure(2, weight=1)

        # ===== ABA REELS =====
        reels_tab = self.config_tabview.tab("Videos")

        # Reels por perfil
        self.reels_per_profile_label = ctk.CTkLabel(
            reels_tab,
            text="Reels por perfil:",
            font=ctk.CTkFont(size=14),
        )
        self.reels_per_profile_label.grid(row=0, column=1, pady=(15, 5), sticky="ew")

        self.reels_per_profile_entry = ctk.CTkEntry(
            reels_tab,
            placeholder_text="3",
            width=200,
        )
        self.reels_per_profile_entry.grid(row=1, column=1, padx=15, pady=(0, 10), sticky="ew")

        # Pausa mínima entre perfis
        self.pause_min_profiles_label = ctk.CTkLabel(
            reels_tab,
            text="Pausa min entre perfis (minutos):",
            font=ctk.CTkFont(size=14),
        )
        self.pause_min_profiles_label.grid(row=2, column=1, pady=(5, 5), sticky="ew")

        self.pause_min_profiles_entry = ctk.CTkEntry(
            reels_tab,
            width=200,
        )
        self.pause_min_profiles_entry.grid(row=3, column=1, padx=15, pady=(0, 15), sticky="ew")

        # Pausa máxima entre perfis
        self.pause_max_profiles_label = ctk.CTkLabel(
            reels_tab,
            text="Pausa max entre perfis (minutos):",
            font=ctk.CTkFont(size=14),
        )
        self.pause_max_profiles_label.grid(row=4, column=1, pady=(5, 5), sticky="ew")

        self.pause_max_profiles_entry = ctk.CTkEntry(
            reels_tab,
            width=200,
        )
        self.pause_max_profiles_entry.grid(row=5, column=1, padx=15, pady=(0, 20), sticky="ew")

        # Botão salvar configurações reels
        self.save_reels_config_button = ctk.CTkButton(
            reels_tab,
            text="Salvar Configuracoes",
            command=self.save_reels_configs_action,

            fg_color="green",
            height=35,
        )
        self.save_reels_config_button.grid(row=6, column=1, padx=15, pady=(5, 15), sticky="ew")

        # ===== ABA UNFOLLOW =====
        unfollow_tab = self.config_tabview.tab("Deixar de Seguir")

        # Lote unfollow
        self.unfollow_batch_size_label = ctk.CTkLabel(
            unfollow_tab,
            text="Lote de deixar de seguir:",
            font=ctk.CTkFont(size=14),
        )
        self.unfollow_batch_size_label.grid(row=0, column=1, pady=(15, 5), sticky="ew")

        self.unfollow_batch_size_entry = ctk.CTkEntry(
            unfollow_tab,
            placeholder_text="10",
            width=200,
        )
        self.unfollow_batch_size_entry.grid(row=1, column=1, padx=15, pady=(0, 10), sticky="ew")

        # Pausa mínima entre lotes
        self.unfollow_pause_min_label = ctk.CTkLabel(
            unfollow_tab,
            text="Pausa min entre lotes (minutos):",
            font=ctk.CTkFont(size=14),
        )
        self.unfollow_pause_min_label.grid(row=2, column=1, pady=(5, 5), sticky="ew")

        self.unfollow_pause_min_entry = ctk.CTkEntry(
            unfollow_tab,
            width=200,
        )
        self.unfollow_pause_min_entry.grid(row=3, column=1, padx=15, pady=(0, 10), sticky="ew")

        # Pausa máxima entre lotes
        self.unfollow_pause_max_label = ctk.CTkLabel(
            unfollow_tab,
            text="Pausa max entre lotes (minutos):",
            font=ctk.CTkFont(size=14),
        )
        self.unfollow_pause_max_label.grid(row=4, column=1, pady=(5, 5), sticky="ew")

        self.unfollow_pause_max_entry = ctk.CTkEntry(
            unfollow_tab,
            width=200,
        )
        self.unfollow_pause_max_entry.grid(row=5, column=1, padx=15, pady=(0, 20), sticky="ew")

        # Botão salvar configurações unfollow
        self.save_unfollow_config_button = ctk.CTkButton(
            unfollow_tab,
            text="Salvar Configuracoes",
            command=self.save_unfollow_configs_action,
            fg_color="green",
            height=35,
        )
        self.save_unfollow_config_button.grid(row=6, column=1, padx=15, pady=(5, 15), sticky="ew")

        # ===== ABA FOLLOW =====
        follow_tab = self.config_tabview.tab("Seguir")

        # Lote follow
        self.follow_batch_size_label = ctk.CTkLabel(
            follow_tab,
            text="Lote de seguir:",
            font=ctk.CTkFont(size=14),
        )
        self.follow_batch_size_label.grid(row=0, column=1, pady=(15, 5), sticky="ew")

        self.follow_batch_size_entry = ctk.CTkEntry(
            follow_tab,
            placeholder_text="5",
            width=200,
        )
        self.follow_batch_size_entry.grid(row=1, column=1, padx=15, pady=(0, 10), sticky="ew")

        # Pausa mínima entre lotes
        self.follow_pause_min_label = ctk.CTkLabel(
            follow_tab,
            text="Pausa min entre lotes (minutos):",
            font=ctk.CTkFont(size=14),
        )
        self.follow_pause_min_label.grid(row=2, column=1, pady=(5, 5), sticky="ew")

        self.follow_pause_min_entry = ctk.CTkEntry(
            follow_tab,
            width=200,
        )
        self.follow_pause_min_entry.grid(row=3, column=1, padx=15, pady=(0, 10), sticky="ew")

        # Pausa máxima entre lotes
        self.follow_pause_max_label = ctk.CTkLabel(
            follow_tab,
            text="Pausa max entre lotes (minutos):",
            font=ctk.CTkFont(size=14),
        )
        self.follow_pause_max_label.grid(row=4, column=1, pady=(5, 5), sticky="ew")

        self.follow_pause_max_entry = ctk.CTkEntry(
            follow_tab,
            width=200,
        )
        self.follow_pause_max_entry.grid(row=5, column=1, padx=15, pady=(0, 10), sticky="ew")

        # Número de ciclos
        self.follow_cycles_label = ctk.CTkLabel(
            follow_tab,
            text="Numero de ciclos:",
            font=ctk.CTkFont(size=14),
        )
        self.follow_cycles_label.grid(row=6, column=1, pady=(5, 5), sticky="ew")

        self.follow_cycles_entry = ctk.CTkEntry(
            follow_tab,
            placeholder_text="10",
            width=200,
        )
        self.follow_cycles_entry.grid(row=7, column=1, padx=15, pady=(0, 20), sticky="ew")

        # Botão salvar configurações follow
        self.save_follow_config_button = ctk.CTkButton(
            follow_tab,
            text="Salvar Configuracoes",
            command=self.save_follow_configs_action,
            fg_color="green",
            height=35,
        )
        self.save_follow_config_button.grid(row=8, column=1, padx=15, pady=(5, 15), sticky="ew")

        # Status das configurações
        self.status_label = ctk.CTkLabel(self, text="", text_color="green")
        self.status_label.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Carregar configurações dos reels, unfollow e follow
        self.load_reels_configs()
        self.load_unfollow_configs()
        self.load_follow_configs()

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
        """Carrega as configuracoes dos reels do arquivo JSON (converte segundos para minutos na interface)."""
        config_file = os.path.join(os.path.dirname(__file__), "..", "bot_configs.json")

        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    configs = json.load(f)

                # Carregar reels por perfil
                if "reels_per_profile" in configs:
                    self.reels_per_profile_entry.delete(0, "end")
                    self.reels_per_profile_entry.insert(0, str(configs["reels_per_profile"]))

                # Carregar pausa minima entre perfis (converter segundos para minutos)
                if "pause_min_profiles" in configs:
                    minutos_min = configs["pause_min_profiles"] / 60.0
                    self.pause_min_profiles_entry.delete(0, "end")
                    self.pause_min_profiles_entry.insert(0, f"{minutos_min:.2f}")

                # Carregar pausa maxima entre perfis (converter segundos para minutos)
                if "pause_max_profiles" in configs:
                    minutos_max = configs["pause_max_profiles"] / 60.0
                    self.pause_max_profiles_entry.delete(0, "end")
                    self.pause_max_profiles_entry.insert(0, f"{minutos_max:.2f}")

            except Exception as e:
                print(f"Erro ao carregar configuracoes dos reels: {e}")

    def save_reels_configs(self):
        """Salva as configuracoes dos reels em um arquivo JSON (converte minutos para segundos)."""
        config_file = os.path.join(os.path.dirname(__file__), "..", "bot_configs.json")

        try:
            # Carregar configuracoes existentes ou criar dicionario vazio
            if os.path.exists(config_file):
                with open(config_file, "r") as f:
                    configs = json.load(f)
            else:
                configs = {}

            # Atualizar configuracoes dos reels
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
            print(f"Erro ao salvar configuracoes dos reels: {e}")
            return False

    def save_reels_configs_action(self):
        """Acao do botao salvar configuracoes dos reels."""
        if self.save_reels_configs():
            self.status_label.configure(
                text="Configuracoes dos reels salvas com sucesso!", text_color="green"
            )
        else:
            self.status_label.configure(
                text="Erro ao salvar configuracoes dos reels!", text_color="red"
            )

    def load_unfollow_configs(self):
        """Carrega as configuracoes de unfollow do arquivo JSON (converte segundos para minutos na interface)."""
        config_file = os.path.join(os.path.dirname(__file__), "..", "bot_configs.json")

        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    configs = json.load(f)

                # Carregar lote unfollow
                if "unfollow_batch_size" in configs:
                    self.unfollow_batch_size_entry.delete(0, "end")
                    self.unfollow_batch_size_entry.insert(0, str(configs["unfollow_batch_size"]))

                # Carregar pausa minima entre lotes (converter segundos para minutos)
                if "unfollow_pause_min" in configs:
                    minutos_min = configs["unfollow_pause_min"] / 60.0
                    self.unfollow_pause_min_entry.delete(0, "end")
                    self.unfollow_pause_min_entry.insert(0, f"{minutos_min:.0f}")

                # Carregar pausa maxima entre lotes (converter segundos para minutos)
                if "unfollow_pause_max" in configs:
                    minutos_max = configs["unfollow_pause_max"] / 60.0
                    self.unfollow_pause_max_entry.delete(0, "end")
                    self.unfollow_pause_max_entry.insert(0, f"{minutos_max:.0f}")

            except Exception as e:
                print(f"Erro ao carregar configuracoes de unfollow: {e}")

    def save_unfollow_configs(self):
        """Salva as configuracoes de unfollow em um arquivo JSON (converte minutos para segundos)."""
        config_file = os.path.join(os.path.dirname(__file__), "..", "bot_configs.json")

        try:
            # Carregar configuracoes existentes ou criar dicionario vazio
            if os.path.exists(config_file):
                with open(config_file, "r") as f:
                    configs = json.load(f)
            else:
                configs = {}

            # Atualizar configuracoes de unfollow
            configs["unfollow_batch_size"] = int(self.unfollow_batch_size_entry.get() or 10)

            # Converter minutos para segundos (pausas)
            minutos_min = float(self.unfollow_pause_min_entry.get() or 15)
            configs["unfollow_pause_min"] = int(minutos_min * 60)

            minutos_max = float(self.unfollow_pause_max_entry.get() or 30)
            configs["unfollow_pause_max"] = int(minutos_max * 60)

            # Salvar no arquivo
            with open(config_file, "w") as f:
                json.dump(configs, f, indent=4)

            return True
        except Exception as e:
            print(f"Erro ao salvar configuracoes de unfollow: {e}")
            return False

    def save_unfollow_configs_action(self):
        """Acao do botao salvar configuracoes de unfollow."""
        if self.save_unfollow_configs():
            self.status_label.configure(
                text="Configuracoes de unfollow salvas com sucesso!", text_color="green"
            )
        else:
            self.status_label.configure(
                text="Erro ao salvar configuracoes de unfollow!", text_color="red"
            )

    def load_follow_configs(self):
        """Carrega as configuracoes de follow do arquivo JSON."""
        config_file = os.path.join(os.path.dirname(__file__), "..", "bot_configs.json")

        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    configs = json.load(f)

                # Carregar lote follow
                if "follow_batch_size" in configs:
                    self.follow_batch_size_entry.delete(0, "end")
                    self.follow_batch_size_entry.insert(0, str(configs["follow_batch_size"]))

                # Carregar pausa minima entre lotes (converter segundos para minutos)
                if "follow_pause_min" in configs:
                    minutos_min = configs["follow_pause_min"] / 60.0
                    self.follow_pause_min_entry.delete(0, "end")
                    self.follow_pause_min_entry.insert(0, f"{minutos_min:.0f}")

                # Carregar pausa maxima entre lotes (converter segundos para minutos)
                if "follow_pause_max" in configs:
                    minutos_max = configs["follow_pause_max"] / 60.0
                    self.follow_pause_max_entry.delete(0, "end")
                    self.follow_pause_max_entry.insert(0, f"{minutos_max:.0f}")

                # Carregar numero de ciclos
                if "follow_cycles" in configs:
                    self.follow_cycles_entry.delete(0, "end")
                    self.follow_cycles_entry.insert(0, str(configs["follow_cycles"]))

            except Exception as e:
                print(f"Erro ao carregar configuracoes de follow: {e}")

    def save_follow_configs(self):
        """Salva as configuracoes de follow em um arquivo JSON (converte minutos para segundos)."""
        config_file = os.path.join(os.path.dirname(__file__), "..", "bot_configs.json")

        try:
            # Carregar configuracoes existentes ou criar dicionario vazio
            if os.path.exists(config_file):
                with open(config_file, "r") as f:
                    configs = json.load(f)
            else:
                configs = {}

            # Atualizar configuracoes de follow
            configs["follow_batch_size"] = int(self.follow_batch_size_entry.get() or 5)

            # Converter minutos para segundos (pausas)
            minutos_min = float(self.follow_pause_min_entry.get() or 20)
            configs["follow_pause_min"] = int(minutos_min * 60)

            minutos_max = float(self.follow_pause_max_entry.get() or 30)
            configs["follow_pause_max"] = int(minutos_max * 60)

            # Numero de ciclos
            configs["follow_cycles"] = int(self.follow_cycles_entry.get() or 10)

            # Salvar no arquivo
            with open(config_file, "w") as f:
                json.dump(configs, f, indent=4)

            return True
        except Exception as e:
            print(f"Erro ao salvar configuracoes de follow: {e}")
            return False

    def save_follow_configs_action(self):
        """Acao do botao salvar configuracoes de follow."""
        if self.save_follow_configs():
            self.status_label.configure(
                text="Configuracoes de follow salvas com sucesso!", text_color="green"
            )
        else:
            self.status_label.configure(
                text="Erro ao salvar configuracoes de follow!", text_color="red"
            )
