import customtkinter as ctk
import logging
import os

class CustomTextHandler(logging.Handler):
    def __init__(self, textbox):
        super().__init__()
        self.textbox = textbox
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        msg = self.format(record)
        self.textbox.insert(ctk.END, msg + "\n")
        self.textbox.see(ctk.END) # Rola para o final

class LogsTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text="Logs & Monitoramento", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.log_textbox = ctk.CTkTextbox(self, width=700, height=400, state="disabled")
        self.log_textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.clear_logs_button = ctk.CTkButton(self, text="Limpar Logs", command=self.clear_logs)
        self.clear_logs_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.export_logs_button = ctk.CTkButton(self, text="Exportar Logs", command=self.export_logs)
        self.export_logs_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.setup_logging()

    def setup_logging(self):
        # Configura o logger para redirecionar para o textbox
        logger = logging.getLogger('InstagramBot')
        logger.setLevel(logging.INFO)

        # Remove handlers existentes para evitar duplicação
        for handler in list(logger.handlers):
            if isinstance(handler, CustomTextHandler):
                logger.removeHandler(handler)
        
        # Adiciona o novo handler para o textbox
        text_handler = CustomTextHandler(self.log_textbox)
        logger.addHandler(text_handler)

        # Carregar logs existentes do arquivo bot.log
        self.load_existing_logs()

    def load_existing_logs(self):
        log_file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'bot.log')
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r', encoding='utf-8') as f:
                logs = f.read()
                self.log_textbox.configure(state="normal")
                self.log_textbox.insert(ctk.END, logs)
                self.log_textbox.see(ctk.END)
                self.log_textbox.configure(state="disabled")

    def clear_logs(self):
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", ctk.END)
        self.log_textbox.configure(state="disabled")
        # Também limpar o arquivo de log
        log_file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'bot.log')
        if os.path.exists(log_file_path):
            with open(log_file_path, 'w', encoding='utf-8') as f:
                f.truncate(0)

    def export_logs(self):
        # Implementar funcionalidade de exportar logs para um arquivo
        # Por enquanto, apenas um placeholder
        print("Exportar logs...")
