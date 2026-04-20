import customtkinter as ctk
from datetime import datetime


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class DashboardWindow(ctk.CTkFrame):
    """
    Dashboard panel for LIAO AI Assistant.
    Shows quick system info and assistant status.
    """

    def __init__(self, master):
        super().__init__(master, corner_radius=18)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self._build_header()
        self._build_cards()
        self._build_footer()

    def _build_header(self):
        self.header = ctk.CTkLabel(
            self,
            text="System Dashboard",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.header.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=20,
            pady=(20, 10),
            sticky="w"
        )

    def _build_cards(self):
        self.status_card = self._create_card(
            row=1,
            column=0,
            title="Assistant Status",
            value="Online",
            subtitle="Ready for commands"
        )

        self.memory_card = self._create_card(
            row=1,
            column=1,
            title="Memory Engine",
            value="Active",
            subtitle="Local database connected"
        )

        self.voice_card = self._create_card(
            row=2,
            column=0,
            title="Voice Listener",
            value="Standby",
            subtitle="Wake word detection ready"
        )

        self.security_card = self._create_card(
            row=2,
            column=1,
            title="Security Layer",
            value="Protected",
            subtitle="Safe mode enabled"
        )

    def _build_footer(self):
        current_time = datetime.now().strftime("%d %b %Y  |  %I:%M %p")

        self.footer = ctk.CTkLabel(
            self,
            text=f"Updated: {current_time}",
            font=ctk.CTkFont(size=12)
        )
        self.footer.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=20,
            pady=(10, 20),
            sticky="e"
        )

    def _create_card(self, row, column, title, value, subtitle):
        card = ctk.CTkFrame(
            self,
            corner_radius=16,
            height=150
        )
        card.grid(
            row=row,
            column=column,
            padx=15,
            pady=12,
            sticky="nsew"
        )

        card.grid_rowconfigure(0, weight=1)
        card.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14)
        )
        title_label.pack(anchor="w", padx=18, pady=(18, 6))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        value_label.pack(anchor="w", padx=18, pady=4)

        sub_label = ctk.CTkLabel(
            card,
            text=subtitle,
            font=ctk.CTkFont(size=12)
        )
        sub_label.pack(anchor="w", padx=18, pady=(4, 18))

        return card


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("LIAO Dashboard")
    root.geometry("900x600")

    dashboard = DashboardWindow(root)
    dashboard.pack(fill="both", expand=True, padx=20, pady=20)

    root.mainloop()