import customtkinter as ctk
import threading
import subprocess
import sys
import os
import psutil # Para matar processos filhos

# Adicionar o diretório raiz do projeto ao sys.path para importar os bots
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ActionsTab(ctk.CTkFrame):
    def __init__(self, master, logs_tab_instance, instagram_user_var, instagram_password_var, **kwargs):
        super().__init__(master, **kwargs)

        self.logs_tab = logs_tab_instance
        self.instagram_user_var = instagram_user_var
        self.instagram_password_var = instagram_password_var
        self.logged_username_var = master.logged_username  # Referência ao username logado

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        self.current_process = None
        self.process_thread = None

        self.label = ctk.CTkLabel(self, text="Ações do Bot", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.account_label = ctk.CTkLabel(self, text="Conta: Nenhuma", text_color="orange")
        self.account_label.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.status_label = ctk.CTkLabel(self, text="Status: Parado", text_color="gray")
        self.status_label.grid(row=8, column=0, padx=20, pady=(10, 20), sticky="ew")

        # Atualizar label da conta quando o username mudar
        self.logged_username_var.trace_add("write", self.update_account_label)

        # Botões para cada ação
        self.extract_followers_button = ctk.CTkButton(self, text="🔍 Extrair Seguidores", command=lambda: self.run_bot("acessar_seguidores.py"))
        self.extract_followers_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.follow_profiles_button = ctk.CTkButton(self, text="👥 Seguir Perfis", command=lambda: self.run_bot("seguir.py"))
        self.follow_profiles_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.like_reels_button = ctk.CTkButton(self, text="🎬 Curtir Reels", command=lambda: self.run_bot("curtir_reels.py"))
        self.like_reels_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.unfollow_profiles_button = ctk.CTkButton(self, text="🚫 Deixar de Seguir", command=lambda: self.run_bot("deixar_de_seguir.py"))
        self.unfollow_profiles_button.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.stop_button = ctk.CTkButton(self, text="🛑 Parar Execução", command=self.stop_bot, fg_color="red", state="disabled")
        self.stop_button.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

    def update_account_label(self, *args):
        """Atualiza o label da conta quando o username muda."""
        username = self.logged_username_var.get()
        if username:
            self.account_label.configure(text=f"Conta: @{username}", text_color="green")
        else:
            self.account_label.configure(text="Conta: Nenhuma", text_color="orange")

    def run_bot(self, script_name):
        if self.current_process and self.current_process.poll() is None:
            self.status_label.configure(text="Status: Já existe um bot em execução!", text_color="orange")
            return

        username = self.instagram_user_var.get()
        password = self.instagram_password_var.get()
        logged_username = self.logged_username_var.get()

        if not username or not password:
            self.status_label.configure(text="Erro: Credenciais não fornecidas!", text_color="red")
            return

        if not logged_username:
            self.status_label.configure(text="Erro: Nenhuma conta logada!", text_color="red")
            return

        self.status_label.configure(text=f"Status: Executando {script_name}...", text_color="blue")
        self.toggle_buttons_state("disabled")
        self.stop_button.configure(state="normal")

        # Obter configurações dos bots
        max_followers = 0
        max_reels = 3  # padrão
        if hasattr(self.master, 'dashboard_frame'):
            if hasattr(self.master.dashboard_frame, 'get_max_followers_config'):
                max_followers = self.master.dashboard_frame.get_max_followers_config()
            if hasattr(self.master.dashboard_frame, 'get_max_reels_config'):
                max_reels = self.master.dashboard_frame.get_max_reels_config()

        # Validação obrigatória para curtir reels
        if script_name == "curtir_reels.py" and max_reels == 0:
            self.status_label.configure(text="Erro: Configure o máximo de reels por perfil no Dashboard!", text_color="red")
            self.toggle_buttons_state("normal")
            self.stop_button.configure(state="disabled")
            return

        thread = threading.Thread(target=self._execute_bot_script, args=(script_name, username, password, logged_username, max_followers, max_reels))
        thread.start()

    def _execute_bot_script(self, script_name, username, password, logged_username, max_followers=0, max_reels=3):
        try:
            script_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bots')), script_name)

            # Passar credenciais e username da conta logada como argumentos de linha de comando
            command = [sys.executable, script_path, "--user", username, "--password", password, "--username", logged_username]

            # Adicionar parâmetro específico para o bot de acessar seguidores
            if script_name == "acessar_seguidores.py" and max_followers > 0:
                command.extend(["--max_followers", str(max_followers)])

            # Adicionar parâmetro específico para o bot de curtir reels
            if script_name == "curtir_reels.py":
                command.extend(["--max_reels", str(max_reels)])

            self.current_process = subprocess.Popen(command,
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE,
                                                    text=True,
                                                    bufsize=1,
                                                    universal_newlines=True)
            
            def read_output(pipe, is_stderr=False):
                for line in iter(pipe.readline, ''):
                    self.after(0, lambda l=line: self.logs_tab.log_textbox.configure(state="normal"))
                    self.after(0, lambda l=line: self.logs_tab.log_textbox.insert(ctk.END, l))
                    self.after(0, lambda: self.logs_tab.log_textbox.see(ctk.END))
                    self.after(0, lambda: self.logs_tab.log_textbox.configure(state="disabled"))
                    if is_stderr:
                        print(f"ERRO SUBPROCESSO: {line}", end='')
                    else:
                        print(f"SUBPROCESSO: {line}", end='')

            stdout_thread = threading.Thread(target=read_output, args=(self.current_process.stdout,))
            stderr_thread = threading.Thread(target=read_output, args=(self.current_process.stderr, True))
            stdout_thread.start()
            stderr_thread.start()

            self.current_process.wait()
            stdout_thread.join()
            stderr_thread.join()

            # Verificar se o processo foi interrompido manualmente
            if self.current_process:
                if self.current_process.returncode is not None:
                    if self.current_process.returncode == 0:
                        self.after(0, lambda: self.status_label.configure(text=f"Status: {script_name} concluído com sucesso!", text_color="green"))
                    else:
                        self.after(0, lambda: self.status_label.configure(text=f"Status: {script_name} falhou com código {self.current_process.returncode}!", text_color="red"))
                else:
                    self.after(0, lambda: self.status_label.configure(text=f"Status: {script_name} interrompido!", text_color="orange"))
            else:
                self.after(0, lambda: self.status_label.configure(text=f"Status: {script_name} interrompido!", text_color="orange"))


        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Status: Erro inesperado ao executar {script_name}!", text_color="red"))
            print(f"Erro inesperado: {e}")
        finally:
            self.after(0, lambda: self.toggle_buttons_state("normal"))
            self.after(0, lambda: self.stop_button.configure(state="disabled"))
            self.after(0, lambda: self.status_label.configure(text="Status: Parado", text_color="gray") if "Executando" in self.status_label.cget("text") else None)
            self.current_process = None
            self.process_thread = None

    def stop_bot(self):
        if self.current_process and self.current_process.poll() is None:
            self.status_label.configure(text="Status: Interrompendo execução...", text_color="orange")
            try:
                # Tenta terminar o processo e seus filhos
                parent = psutil.Process(self.current_process.pid)
                for child in parent.children(recursive=True):
                    child.terminate()
                parent.terminate()
                parent.wait(timeout=5) # Espera um pouco para terminar
                self.after(0, lambda: self.status_label.configure(text="Status: Execução interrompida!", text_color="red"))
            except psutil.NoSuchProcess:
                self.after(0, lambda: self.status_label.configure(text="Status: Processo já encerrado.", text_color="red"))
            except Exception as e:
                self.after(0, lambda: self.status_label.configure(text=f"Status: Erro ao interromper: {e}", text_color="red"))
            finally:
                self.current_process = None
                self.toggle_buttons_state("normal")
                self.stop_button.configure(state="disabled")
        else:
            self.status_label.configure(text="Status: Nenhum bot em execução para parar.", text_color="gray")
            self.toggle_buttons_state("normal")
            self.stop_button.configure(state="disabled")

    def toggle_buttons_state(self, state):
        self.extract_followers_button.configure(state=state)
        self.follow_profiles_button.configure(state=state)
        self.like_reels_button.configure(state=state)
        self.unfollow_profiles_button.configure(state=state)
