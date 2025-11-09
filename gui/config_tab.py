import customtkinter as ctk
from dotenv import load_dotenv, set_key
import os
import json

class ConfigTab(ctk.CTkFrame):
    def __init__(self, master, instagram_user_var, instagram_password_var, **kwargs):
        super().__init__(master, **kwargs)

        self.instagram_user_var = instagram_user_var
        self.instagram_password_var = instagram_password_var

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.label = ctk.CTkLabel(self, text="Credenciais & Configurações", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # Campos de credenciais
        self.username_label = ctk.CTkLabel(self, text="Usuário do Instagram:")
        self.username_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Seu usuário", textvariable=self.instagram_user_var)
        self.username_entry.grid(row=1, column=1, padx=20, pady=(10, 0), sticky="ew")

        self.password_label = ctk.CTkLabel(self, text="Senha do Instagram:")
        self.password_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Sua senha", show="*", textvariable=self.instagram_password_var)
        self.password_entry.grid(row=2, column=1, padx=20, pady=(10, 0), sticky="ew")

        self.show_password_checkbox = ctk.CTkCheckBox(self, text="Mostrar Senha", command=self.toggle_password_visibility)
        self.show_password_checkbox.grid(row=3, column=1, padx=20, pady=(0, 10), sticky="w")

        self.save_button = ctk.CTkButton(self, text="Salvar Credenciais", command=self.save_credentials)
        self.save_button.grid(row=4, column=0, columnspan=2, padx=20, pady=(10, 5), sticky="ew")

        self.login_button = ctk.CTkButton(self, text="Fazer Login", command=self.perform_login, fg_color="green")
        self.login_button.grid(row=5, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")

        self.status_label = ctk.CTkLabel(self, text="", text_color="green")
        self.status_label.grid(row=6, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="n")



    def toggle_password_visibility(self):
        if self.show_password_checkbox.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def save_credentials(self):
        username = self.instagram_user_var.get()
        password = self.instagram_password_var.get()

        if not username or not password:
            self.status_label.configure(text="Usuário e senha não podem ser vazios!", text_color="red")
            return

        self.status_label.configure(text="Credenciais salvas na sessão!", text_color="green")
        # Não salva mais no .env, apenas atualiza as StringVar

    def perform_login(self):
        """Executa o login e atualiza o username da conta logada."""
        from core.browser import iniciar_driver, fazer_login, clicar_agora_nao
        import threading

        username = self.instagram_user_var.get()
        password = self.instagram_password_var.get()

        if not username or not password:
            self.status_label.configure(text="Preencha usuário e senha primeiro!", text_color="red")
            return

        self.status_label.configure(text="Fazendo login...", text_color="blue")
        self.login_button.configure(state="disabled", text="Logando...")

        def login_thread():
            driver = None
            try:
                driver = iniciar_driver()
                sucesso, username_logado = fazer_login(driver, username, password)

                if sucesso:
                    # Atualizar o username logado na interface
                    self.master.logged_username.set(username_logado)
                    self.after(0, lambda: self.status_label.configure(text=f"Login bem-sucedido! Conta: @{username_logado}", text_color="green"))
                else:
                    self.after(0, lambda: self.status_label.configure(text="Falha no login. Verifique as credenciais.", text_color="red"))

            except Exception as e:
                self.after(0, lambda: self.status_label.configure(text=f"Erro durante login: {str(e)}", text_color="red"))
            finally:
                if driver:
                    driver.quit()
                self.after(0, lambda: self.login_button.configure(state="normal", text="Fazer Login"))

        thread = threading.Thread(target=login_thread)
        thread.start()
