import customtkinter as ctk
import os
from gui.dashboard_tab import DashboardTab
from gui.config_tab import ConfigTab
from gui.actions_tab import ActionsTab
from gui.logs_tab import LogsTab
from gui.data_tab import DataTab


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bot Instagram - Automação")
        self.geometry("1000x700")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        ctk.set_appearance_mode("System")

        # Variáveis para armazenar credenciais e conta logada
        self.instagram_user = ctk.StringVar(value="")
        self.instagram_password = ctk.StringVar(value="")
        self.logged_username = ctk.StringVar(
            value=""
        )  # Username da conta atualmente logada

        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(7, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(
            self.navigation_frame,
            text="Bot Instagram",
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.dashboard_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Dashboard",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            anchor="w",
            command=self.dashboard_button_event,
        )
        self.dashboard_button.grid(row=1, column=0, sticky="ew")

        self.config_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Credenciais & Config",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            anchor="w",
            command=self.config_button_event,
        )
        self.config_button.grid(row=2, column=0, sticky="ew")

        self.actions_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Ações do Bot",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            anchor="w",
            command=self.actions_button_event,
        )
        self.actions_button.grid(row=3, column=0, sticky="ew")

        self.logs_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Logs & Monitoramento",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            anchor="w",
            command=self.logs_button_event,
        )
        self.logs_button.grid(row=4, column=0, sticky="ew")

        self.data_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Dados",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            anchor="w",
            command=self.data_button_event,
        )
        self.data_button.grid(row=5, column=0, sticky="ew")

        self.appearance_mode_label = ctk.CTkLabel(
            self.navigation_frame, text="Tema:", anchor="w"
        )
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.navigation_frame,
            values=["System", "Dark", "Light"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(
            row=9, column=0, padx=20, pady=(10, 20), sticky="ew"
        )

        # Criar frames para cada aba
        self.dashboard_frame = DashboardTab(
            self, corner_radius=0, fg_color="transparent"
        )
        self.config_frame = ConfigTab(
            self,
            self.instagram_user,
            self.instagram_password,
            corner_radius=0,
            fg_color="transparent",
        )
        self.logs_frame = LogsTab(
            self, corner_radius=0, fg_color="transparent"
        )  # LogsTab deve ser criada antes
        self.actions_frame = ActionsTab(
            self,
            self.logs_frame,
            self.instagram_user,
            self.instagram_password,
            corner_radius=0,
            fg_color="transparent",
        )  # Passar logs_frame e credenciais
        self.data_frame = DataTab(self, corner_radius=0, fg_color="transparent")

        # Selecionar frame inicial
        self.select_frame_by_name("dashboard")

    def select_frame_by_name(self, name):
        # Definir cor de fundo para os botões de navegação
        self.dashboard_button.configure(
            fg_color=("gray75", "gray25") if name == "dashboard" else "transparent"
        )
        self.config_button.configure(
            fg_color=("gray75", "gray25") if name == "config" else "transparent"
        )
        self.actions_button.configure(
            fg_color=("gray75", "gray25") if name == "actions" else "transparent"
        )
        self.logs_button.configure(
            fg_color=("gray75", "gray25") if name == "logs" else "transparent"
        )
        self.data_button.configure(
            fg_color=("gray75", "gray25") if name == "data" else "transparent"
        )

        # Mostrar o frame selecionado
        if name == "dashboard":
            self.dashboard_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.dashboard_frame.grid_forget()
        if name == "config":
            self.config_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.config_frame.grid_forget()
        if name == "actions":
            self.actions_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.actions_frame.grid_forget()
        if name == "logs":
            self.logs_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.logs_frame.grid_forget()
        if name == "data":
            self.data_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.data_frame.grid_forget()

    def dashboard_button_event(self):
        self.select_frame_by_name("dashboard")

    def config_button_event(self):
        self.select_frame_by_name("config")

    def actions_button_event(self):
        self.select_frame_by_name("actions")

    def logs_button_event(self):
        self.select_frame_by_name("logs")

    def data_button_event(self):
        self.select_frame_by_name("data")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
