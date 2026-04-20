import math
import customtkinter as ctk


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class VoiceUI(ctk.CTkFrame):
    """
    Voice interaction panel for LIAO AI Assistant.
    """

    def __init__(self, master):
        super().__init__(master, corner_radius=18)

        self.is_listening = False
        self.wave_step = 0

        self.grid_columnconfigure(0, weight=1)

        self._build_layout()

    def _build_layout(self):
        self.title_label = ctk.CTkLabel(
            self,
            text="Voice Assistant",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        self.title_label.grid(
            row=0,
            column=0,
            pady=(24, 8),
            padx=20
        )

        self.status_label = ctk.CTkLabel(
            self,
            text="Standby",
            font=ctk.CTkFont(size=15)
        )
        self.status_label.grid(
            row=1,
            column=0,
            pady=(0, 20)
        )

        self.wave_canvas = ctk.CTkCanvas(
            self,
            width=520,
            height=170,
            bg="#1a1a1a",
            highlightthickness=0
        )
        self.wave_canvas.grid(
            row=2,
            column=0,
            padx=20,
            pady=10
        )

        self.mic_button = ctk.CTkButton(
            self,
            text="🎤 Start Listening",
            width=220,
            height=50,
            command=self.toggle_listening
        )
        self.mic_button.grid(
            row=3,
            column=0,
            pady=(18, 10)
        )

        self.command_label = ctk.CTkLabel(
            self,
            text="Wake Word: Hey LIAO",
            font=ctk.CTkFont(size=13)
        )
        self.command_label.grid(
            row=4,
            column=0,
            pady=(4, 24)
        )

        self._draw_idle_wave()

    def _draw_idle_wave(self):
        self.wave_canvas.delete("all")

        center_y = 85
        points = []

        for x in range(0, 520, 8):
            y = center_y + math.sin((x / 45) + self.wave_step) * 8
            points.extend([x, y])

        self.wave_canvas.create_line(
            points,
            width=3,
            smooth=True,
            fill="#3B82F6"
        )

    def _animate_wave(self):
        if not self.is_listening:
            self._draw_idle_wave()
            return

        self.wave_canvas.delete("all")

        center_y = 85
        points = []

        for x in range(0, 520, 8):
            amplitude = 18 + (math.sin(self.wave_step) * 6)
            y = center_y + math.sin((x / 22) + self.wave_step) * amplitude
            points.extend([x, y])

        self.wave_canvas.create_line(
            points,
            width=4,
            smooth=True,
            fill="#22C55E"
        )

        self.wave_step += 0.25
        self.after(40, self._animate_wave)

    def toggle_listening(self):
        self.is_listening = not self.is_listening

        if self.is_listening:
            self.status_label.configure(text="Listening...")
            self.mic_button.configure(
                text="⏹ Stop Listening"
            )
            self._animate_wave()
        else:
            self.status_label.configure(text="Standby")
            self.mic_button.configure(
                text="🎤 Start Listening"
            )
            self._draw_idle_wave()

    def set_transcript(self, text: str):
        self.command_label.configure(text=f"Heard: {text}")

    def set_status(self, text: str):
        self.status_label.configure(text=text)


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("LIAO Voice UI")
    root.geometry("760x520")

    app = VoiceUI(root)
    app.pack(fill="both", expand=True, padx=20, pady=20)

    root.mainloop()