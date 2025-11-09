import customtkinter as ctk
import os
from core.file_manager import ler_urls_arquivo

class DataTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # 2 linhas para label e textbox

        self.label = ctk.CTkLabel(self, text="Dados dos Perfis", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.data_textbox = ctk.CTkTextbox(self, width=700, height=400, state="disabled")
        self.data_textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.load_data_button = ctk.CTkButton(self, text="Recarregar Dados", command=self.load_data)
        self.load_data_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.load_data()

    def load_data(self):
        self.data_textbox.configure(state="normal")
        self.data_textbox.delete("1.0", ctk.END)

        # Caminho para o arquivo seguidores.txt
        file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'seguidores.txt')

        if os.path.exists(file_path):
            urls = ler_urls_arquivo(file_path)
            if urls:
                self.data_textbox.insert(ctk.END, f"Total de perfis: {len(urls)}\n\n")
                for url in urls:
                    self.data_textbox.insert(ctk.END, url + "\n")
            else:
                self.data_textbox.insert(ctk.END, "Nenhum perfil encontrado em seguidores.txt.\n")
        else:
            self.data_textbox.insert(ctk.END, "Arquivo 'seguidores.txt' não encontrado.\n")
        
        self.data_textbox.configure(state="disabled")
