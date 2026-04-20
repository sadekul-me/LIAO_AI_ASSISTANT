import customtkinter as ctk
from tkinter import END


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ChatWindow(ctk.CTk):
    """
    Main desktop chat interface for LIAO AI Assistant.
    """

    def __init__(self):
        super().__init__()

        self.title("LIAO AI Assistant")
        self.geometry("980x680")
        self.minsize(860, 600)

        self._configure_layout()
        self._build_sidebar()
        self._build_main_panel()
        self._load_welcome()

    def _configure_layout(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.sidebar.grid_rowconfigure(6, weight=1)

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="LIAO AI",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo.grid(row=0, column=0, padx=24, pady=(28, 16))

        self.status_card = ctk.CTkFrame(self.sidebar)
        self.status_card.grid(row=1, column=0, padx=18, pady=10, sticky="ew")

        self.status_label = ctk.CTkLabel(
            self.status_card,
            text="● Online",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(pady=10)

        self.memory_card = ctk.CTkFrame(self.sidebar)
        self.memory_card.grid(row=2, column=0, padx=18, pady=10, sticky="ew")

        self.memory_label = ctk.CTkLabel(
            self.memory_card,
            text="Memory Ready",
            font=ctk.CTkFont(size=14)
        )
        self.memory_label.pack(pady=10)

        self.clear_button = ctk.CTkButton(
            self.sidebar,
            text="Clear Chat",
            height=42,
            command=self.clear_chat
        )
        self.clear_button.grid(row=3, column=0, padx=18, pady=(16, 8), sticky="ew")

        self.settings_button = ctk.CTkButton(
            self.sidebar,
            text="Settings",
            height=42
        )
        self.settings_button.grid(row=4, column=0, padx=18, pady=8, sticky="ew")

        self.exit_button = ctk.CTkButton(
            self.sidebar,
            text="Exit",
            height=42,
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=self.destroy
        )
        self.exit_button.grid(row=5, column=0, padx=18, pady=8, sticky="ew")

        self.footer = ctk.CTkLabel(
            self.sidebar,
            text="v1.0 Local Build",
            font=ctk.CTkFont(size=12)
        )
        self.footer.grid(row=7, column=0, padx=20, pady=(0, 18))

    def _build_main_panel(self):
        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=0
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.topbar = ctk.CTkFrame(
            self.main_frame,
            height=70
        )
        self.topbar.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 10))

        self.topbar.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.topbar,
            text="Nilima Assistant",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=18, sticky="w")

        self.chat_box = ctk.CTkTextbox(
            self.main_frame,
            wrap="word",
            font=ctk.CTkFont(size=15),
            corner_radius=16
        )
        self.chat_box.grid(row=1, column=0, sticky="nsew", padx=18, pady=8)
        self.chat_box.configure(state="disabled")

        self.bottom_bar = ctk.CTkFrame(
            self.main_frame,
            height=80
        )
        self.bottom_bar.grid(row=2, column=0, sticky="ew", padx=18, pady=(10, 18))

        self.bottom_bar.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(
            self.bottom_bar,
            height=46,
            placeholder_text="Write a message..."
        )
        self.entry.grid(row=0, column=0, padx=(16, 10), pady=16, sticky="ew")
        self.entry.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(
            self.bottom_bar,
            text="Send",
            width=90,
            height=46,
            command=self.send_message
        )
        self.send_button.grid(row=0, column=1, padx=(0, 10), pady=16)

        self.mic_button = ctk.CTkButton(
            self.bottom_bar,
            text="🎤",
            width=60,
            height=46
        )
        self.mic_button.grid(row=0, column=2, padx=(0, 16), pady=16)

    def _load_welcome(self):
        self._append_message(
            "Nilima",
            "হ্যালো, আমি প্রস্তুত আছি। আজ কীভাবে সাহায্য করতে পারি?"
        )

    def _append_message(self, sender, message):
        self.chat_box.configure(state="normal")
        self.chat_box.insert(END, f"{sender}: {message}\n\n")
        self.chat_box.see(END)
        self.chat_box.configure(state="disabled")

    def send_message(self, event=None):
        message = self.entry.get().strip()

        if not message:
            return

        self._append_message("You", message)
        self.entry.delete(0, END)

        self._append_message(
            "Nilima",
            "তোমার বার্তাটি পেয়েছি। Backend connection প্রস্তুত হলে উত্তর দেখাবে।"
        )

    def clear_chat(self):
        self.chat_box.configure(state="normal")
        self.chat_box.delete("1.0", END)
        self.chat_box.configure(state="disabled")
        self._load_welcome()


if __name__ == "__main__":
    app = ChatWindow()
    app.mainloop()