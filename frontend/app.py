import customtkinter as ctk

from frontend.ui.chat_window import ChatWindow
from frontend.ui.dashboard import DashboardWindow
from frontend.ui.settings import SettingsWindow
from frontend.ui.voice_ui import VoiceUI


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LIAODesktopApp(ctk.CTk):
    """
    Main desktop launcher for LIAO AI Assistant.
    """

    def __init__(self):
        super().__init__()

        self.title("LIAO AI Assistant")
        self.geometry("1280x760")
        self.minsize(1100, 680)

        self.current_frame = None

        self._configure_layout()
        self._build_sidebar()
        self._build_topbar()

        self.show_dashboard()

    def _configure_layout(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0
        )
        self.sidebar.grid(
            row=0,
            column=0,
            rowspan=2,
            sticky="nsew"
        )

        self.sidebar.grid_rowconfigure(10, weight=1)

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="LIAO AI",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        self.logo.grid(
            row=0,
            column=0,
            padx=24,
            pady=(28, 24)
        )

        self.dashboard_btn = self._menu_button(
            row=1,
            text="Dashboard",
            command=self.show_dashboard
        )

        self.chat_btn = self._menu_button(
            row=2,
            text="Chat",
            command=self.show_chat
        )

        self.voice_btn = self._menu_button(
            row=3,
            text="Voice",
            command=self.show_voice
        )

        self.settings_btn = self._menu_button(
            row=4,
            text="Settings",
            command=self.show_settings
        )

        self.exit_btn = ctk.CTkButton(
            self.sidebar,
            text="Exit",
            height=42,
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=self.destroy
        )
        self.exit_btn.grid(
            row=9,
            column=0,
            padx=18,
            pady=18,
            sticky="ew"
        )

    def _build_topbar(self):
        self.topbar = ctk.CTkFrame(
            self,
            height=70,
            corner_radius=0
        )
        self.topbar.grid(
            row=0,
            column=1,
            sticky="ew"
        )

        self.topbar.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.topbar,
            text="Dashboard",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.grid(
            row=0,
            column=0,
            padx=24,
            pady=18,
            sticky="w"
        )

        self.status_label = ctk.CTkLabel(
            self.topbar,
            text="● Online",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.grid(
            row=0,
            column=1,
            padx=24,
            pady=18,
            sticky="e"
        )

    def _menu_button(self, row, text, command):
        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=42,
            command=command
        )
        button.grid(
            row=row,
            column=0,
            padx=18,
            pady=8,
            sticky="ew"
        )
        return button

    def _clear_content(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

    def _set_title(self, title):
        self.title_label.configure(text=title)

    def show_dashboard(self):
        self._clear_content()
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
        self._clear_content()
        self._set_title("Chat")

        self.current_frame = ChatWindow()
        self.current_frame.withdraw()

        frame = ctk.CTkFrame(self, corner_radius=18)
        frame.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=18,
            pady=18
        )

        label = ctk.CTkLabel(
            frame,
            text="Chat Window runs separately.\nRun chat_window.py for full chat mode.",
            font=ctk.CTkFont(size=18)
        )
        label.pack(expand=True)

        self.current_frame = frame

    def show_voice(self):
        self._clear_content()
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
        self._clear_content()
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