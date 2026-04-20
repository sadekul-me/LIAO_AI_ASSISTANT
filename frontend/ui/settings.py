import customtkinter as ctk


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SettingsWindow(ctk.CTkFrame):
    """
    Settings panel for LIAO AI Assistant.
    """

    def __init__(self, master):
        super().__init__(master, corner_radius=18)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._build_header()
        self._build_general_section()
        self._build_voice_section()
        self._build_system_section()
        self._build_actions()

    def _build_header(self):
        title = ctk.CTkLabel(
            self,
            text="Settings",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=20,
            pady=(20, 15),
            sticky="w"
        )

    def _build_general_section(self):
        frame = ctk.CTkFrame(self, corner_radius=16)
        frame.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=10,
            sticky="nsew"
        )

        title = ctk.CTkLabel(
            frame,
            text="General",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(anchor="w", padx=18, pady=(18, 12))

        self.theme_label = ctk.CTkLabel(frame, text="Theme")
        self.theme_label.pack(anchor="w", padx=18)

        self.theme_menu = ctk.CTkOptionMenu(
            frame,
            values=["Dark", "Light", "System"],
            command=self.change_theme
        )
        self.theme_menu.set("Dark")
        self.theme_menu.pack(fill="x", padx=18, pady=(6, 14))

        self.language_label = ctk.CTkLabel(frame, text="Language")
        self.language_label.pack(anchor="w", padx=18)

        self.language_menu = ctk.CTkOptionMenu(
            frame,
            values=["Bangla", "English"]
        )
        self.language_menu.set("Bangla")
        self.language_menu.pack(fill="x", padx=18, pady=(6, 18))

    def _build_voice_section(self):
        frame = ctk.CTkFrame(self, corner_radius=16)
        frame.grid(
            row=1,
            column=1,
            padx=(10, 20),
            pady=10,
            sticky="nsew"
        )

        title = ctk.CTkLabel(
            frame,
            text="Voice",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(anchor="w", padx=18, pady=(18, 12))

        self.voice_switch = ctk.CTkSwitch(
            frame,
            text="Enable Voice Assistant"
        )
        self.voice_switch.select()
        self.voice_switch.pack(anchor="w", padx=18, pady=8)

        self.wake_switch = ctk.CTkSwitch(
            frame,
            text="Wake Word Detection"
        )
        self.wake_switch.select()
        self.wake_switch.pack(anchor="w", padx=18, pady=8)

        self.voice_name_label = ctk.CTkLabel(
            frame,
            text="Wake Word"
        )
        self.voice_name_label.pack(anchor="w", padx=18, pady=(12, 0))

        self.voice_name_entry = ctk.CTkEntry(
            frame,
            placeholder_text="Hey LIAO"
        )
        self.voice_name_entry.pack(fill="x", padx=18, pady=(6, 18))

    def _build_system_section(self):
        frame = ctk.CTkFrame(self, corner_radius=16)
        frame.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=20,
            pady=10,
            sticky="nsew"
        )

        title = ctk.CTkLabel(
            frame,
            text="System Controls",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(anchor="w", padx=18, pady=(18, 12))

        self.startup_switch = ctk.CTkSwitch(
            frame,
            text="Run on Windows Startup"
        )
        self.startup_switch.pack(anchor="w", padx=18, pady=8)

        self.notify_switch = ctk.CTkSwitch(
            frame,
            text="Desktop Notifications"
        )
        self.notify_switch.select()
        self.notify_switch.pack(anchor="w", padx=18, pady=8)

        self.safe_mode_switch = ctk.CTkSwitch(
            frame,
            text="Safe Mode Protection"
        )
        self.safe_mode_switch.select()
        self.safe_mode_switch.pack(anchor="w", padx=18, pady=(8, 18))

    def _build_actions(self):
        self.save_button = ctk.CTkButton(
            self,
            text="Save Settings",
            height=42,
            command=self.save_settings
        )
        self.save_button.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=20,
            pady=(12, 20),
            sticky="ew"
        )

    def change_theme(self, value):
        if value == "Dark":
            ctk.set_appearance_mode("dark")
        elif value == "Light":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("system")

    def save_settings(self):
        self.save_button.configure(text="Saved")

    def get_settings(self):
        return {
            "theme": self.theme_menu.get(),
            "language": self.language_menu.get(),
            "voice_enabled": self.voice_switch.get(),
            "wake_word_enabled": self.wake_switch.get(),
            "wake_word": self.voice_name_entry.get(),
            "startup": self.startup_switch.get(),
            "notifications": self.notify_switch.get(),
            "safe_mode": self.safe_mode_switch.get()
        }


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("LIAO Settings")
    root.geometry("900x650")

    settings = SettingsWindow(root)
    settings.pack(fill="both", expand=True, padx=20, pady=20)

    root.mainloop()