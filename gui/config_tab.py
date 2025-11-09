import customtkinter as ctk
from dotenv import load_dotenv, set_key
import os

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
        self.save_button.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        self.status_label = ctk.CTkLabel(self, text="", text_color="green")
        self.status_label.grid(row=5, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="n")

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
