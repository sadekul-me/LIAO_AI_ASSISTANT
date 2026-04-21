import customtkinter as ctk

from frontend.ui.dashboard import DashboardWindow
from frontend.ui.chat_window import ChatWindow
from frontend.ui.settings import SettingsWindow
from frontend.ui.voice_ui import VoiceUI


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LIAODesktopApp(ctk.CTk):
    """
    Main Application Shell for LIAO AI Assistant
    """

    def __init__(self):
        super().__init__()

        self.title("LIAO AI Assistant")
        self.geometry("1280x760")
        self.minsize(1100, 680)

        self.current_frame = None

        self._setup_layout()
        self._build_sidebar()
        self._build_topbar()

        self.show_dashboard()

    # ---------------- Layout ----------------
    def _setup_layout(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

    # ---------------- Sidebar ----------------
    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=230, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.sidebar.grid_rowconfigure(10, weight=1)

        logo = ctk.CTkLabel(
            self.sidebar,
            text="LIAO AI",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        logo.grid(row=0, column=0, padx=20, pady=(30, 20))

        self._menu_button("Dashboard", self.show_dashboard, 1)
        self._menu_button("Chat", self.show_chat, 2)
        self._menu_button("Voice", self.show_voice, 3)
        self._menu_button("Settings", self.show_settings, 4)

        exit_btn = ctk.CTkButton(
            self.sidebar,
            text="Exit",
            height=42,
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=self.destroy
        )
        exit_btn.grid(row=9, column=0, padx=18, pady=20, sticky="ew")

    def _menu_button(self, text, command, row):
        btn = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=42,
            command=command
        )
        btn.grid(row=row, column=0, padx=18, pady=8, sticky="ew")

    # ---------------- Topbar ----------------
    def _build_topbar(self):
        self.topbar = ctk.CTkFrame(self, height=70, corner_radius=0)
        self.topbar.grid(row=0, column=1, sticky="ew")

        self.topbar.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.topbar,
            text="Dashboard",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=18, sticky="w")

    # ---------------- Navigation ----------------
    def _clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def _set_title(self, title):
        self.title_label.configure(text=title)

    def show_dashboard(self):
        self._clear_frame()
        self._set_title("Dashboard")

        self.current_frame = DashboardWindow(self)
        self.current_frame.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=18,
            pady=18
        )

    def show_chat(self):
        self._clear_frame()
        self._set_title("Chat")

        self.current_frame = ChatWindow(self)
        self.current_frame.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=18,
            pady=18
        )

    def show_voice(self):
        self._clear_frame()
        self._set_title("Voice")

        self.current_frame = VoiceUI(self)
        self.current_frame.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=18,
            pady=18
        )

    def show_settings(self):
        self._clear_frame()
        self._set_title("Settings")

        self.current_frame = SettingsWindow(self)
        self.current_frame.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=18,
            pady=18
        )


if __name__ == "__main__":
    app = LIAODesktopApp()
    app.mainloop()