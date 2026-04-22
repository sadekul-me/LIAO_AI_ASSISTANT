import customtkinter as ctk

from frontend.ui.dashboard import DashboardWindow
from frontend.ui.chat_window import ChatWindow
from frontend.ui.settings import SettingsWindow
from frontend.ui.voice_ui import VoiceUI


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LIAODesktopApp(ctk.CTk):
    """
    Main desktop shell for LIAO AI Assistant.
    Handles navigation, layout and page rendering.
    """

    def __init__(self):
        super().__init__()

        self.current_frame = None

        self._configure_window()
        self._configure_grid()
        self._build_sidebar()
        self._build_topbar()

        self.show_dashboard()

    # -------------------------------------------------
    # WINDOW
    # -------------------------------------------------
    def _configure_window(self):
        self.title("LIAO AI Assistant")
        self.geometry("1280x760")
        self.minsize(1100, 680)

    # -------------------------------------------------
    # GRID SYSTEM
    # -------------------------------------------------
    def _configure_grid(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

    # -------------------------------------------------
    # SIDEBAR
    # -------------------------------------------------
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

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="LIAO AI",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        )
        self.logo_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=(30, 20)
        )

        self._create_nav_button(
            text="Dashboard",
            row=1,
            command=self.show_dashboard
        )

        self._create_nav_button(
            text="Chat",
            row=2,
            command=self.show_chat
        )

        self._create_nav_button(
            text="Voice",
            row=3,
            command=self.show_voice
        )

        self._create_nav_button(
            text="Settings",
            row=4,
            command=self.show_settings
        )

        self.exit_button = ctk.CTkButton(
            self.sidebar,
            text="Exit",
            height=42,
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=self.destroy
        )
        self.exit_button.grid(
            row=9,
            column=0,
            padx=18,
            pady=20,
            sticky="ew"
        )

    def _create_nav_button(
        self,
        text: str,
        row: int,
        command
    ):
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

    # -------------------------------------------------
    # TOPBAR
    # -------------------------------------------------
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

        self.page_title = ctk.CTkLabel(
            self.topbar,
            text="Dashboard",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        self.page_title.grid(
            row=0,
            column=0,
            padx=20,
            pady=18,
            sticky="w"
        )

    # -------------------------------------------------
    # PAGE CONTROL
    # -------------------------------------------------
    def _clear_current_page(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    def _set_page_title(self, text: str):
        self.page_title.configure(text=text)

    def _load_page(self, frame_class, title: str):
        self._clear_current_page()
        self._set_page_title(title)

        self.current_frame = frame_class(self)

        self.current_frame.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=18,
            pady=18
        )

    # -------------------------------------------------
    # NAVIGATION
    # -------------------------------------------------
    def show_dashboard(self):
        self._load_page(
            DashboardWindow,
            "Dashboard"
        )

    def show_chat(self):
        self._load_page(
            ChatWindow,
            "Chat"
        )

    def show_voice(self):
        self._load_page(
            VoiceUI,
            "Voice"
        )

    def show_settings(self):
        self._load_page(
            SettingsWindow,
            "Settings"
        )


# -------------------------------------------------
# ENTRY POINT
# -------------------------------------------------
if __name__ == "__main__":
    app = LIAODesktopApp()
    app.mainloop()