import threading
import requests
import customtkinter as ctk
from tkinter import END


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ChatWindow(ctk.CTkFrame):
    """
    Embedded Chat Interface for LIAO Desktop Application

    Responsibilities:
    - UI rendering
    - backend communication
    - response handling
    """

    def __init__(self, master):
        super().__init__(master, corner_radius=0)

        self.api_url = "http://127.0.0.1:8000/chat/"
        self.master = master

        self._build_ui()
        self._load_welcome()

    # ==================================================
    # UI SETUP
    # ==================================================
    def _build_ui(self):

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ---------------- Sidebar ----------------
        self.sidebar = ctk.CTkFrame(self, width=230, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)

        ctk.CTkLabel(
            self.sidebar,
            text="LIAO AI",
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(25, 15))

        self.status_label = ctk.CTkLabel(
            self.sidebar,
            text="● Backend Ready"
        )
        self.status_label.grid(row=1, column=0, padx=10, pady=10)

        self.clear_btn = ctk.CTkButton(
            self.sidebar,
            text="Clear Chat",
            command=self.clear_chat
        )
        self.clear_btn.grid(row=2, column=0, padx=15, pady=10, sticky="ew")

        # ---------------- Topbar ----------------
        self.topbar = ctk.CTkFrame(self, height=70)
        self.topbar.grid(row=0, column=1, sticky="ew", padx=15, pady=(15, 10))

        ctk.CTkLabel(
            self.topbar,
            text="Chat Assistant",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left", padx=20)

        # ---------------- Chat Box ----------------
        self.chat_box = ctk.CTkTextbox(
            self,
            wrap="word",
            font=ctk.CTkFont(size=14),
            corner_radius=12
        )
        self.chat_box.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=15,
            pady=10
        )
        self.chat_box.configure(state="disabled")

        # ---------------- Bottom Bar ----------------
        self.bottom_bar = ctk.CTkFrame(self, height=80)
        self.bottom_bar.grid(row=2, column=1, sticky="ew", padx=15, pady=15)
        self.bottom_bar.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(
            self.bottom_bar,
            placeholder_text="Type your message..."
        )
        self.entry.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="ew")
        self.entry.bind("<Return>", self.send_message)

        self.send_btn = ctk.CTkButton(
            self.bottom_bar,
            text="Send",
            command=self.send_message
        )
        self.send_btn.grid(row=0, column=1, padx=(0, 15), pady=15)

    # ==================================================
    # CHAT LOGIC
    # ==================================================
    def _load_welcome(self):
        self._append("System", "Assistant ready to respond.")

    def _append(self, sender, text):
        self.chat_box.configure(state="normal")
        self.chat_box.insert(END, f"{sender}: {text}\n\n")
        self.chat_box.see(END)
        self.chat_box.configure(state="disabled")

    def send_message(self, event=None):
        message = self.entry.get().strip()

        if not message:
            return

        self._append("You", message)
        self.entry.delete(0, END)

        self.send_btn.configure(state="disabled", text="...")

        threading.Thread(
            target=self._call_backend,
            args=(message,),
            daemon=True
        ).start()

    # ==================================================
    # BACKEND CALL
    # ==================================================
    def _call_backend(self, message):
        try:
            response = requests.post(
                self.api_url,
                json={"message": message, "context": ""},
                timeout=30
            )

            if response.status_code != 200:
                reply = "Server error occurred."
            else:
                data = response.json()
                reply = data.get("reply") or "No response received."

        except Exception as e:
            reply = "Backend disconnected. Please start server."

        self.after(0, lambda: self._update_ui(reply))

    def _update_ui(self, reply):
        self._append("Nilima", reply)

        self.send_btn.configure(state="normal", text="Send")

    # ==================================================
    # CLEAR CHAT
    # ==================================================
    def clear_chat(self):
        self.chat_box.configure(state="normal")
        self.chat_box.delete("1.0", END)
        self.chat_box.configure(state="disabled")
        self._load_welcome()