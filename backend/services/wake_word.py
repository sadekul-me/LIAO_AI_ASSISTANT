import time
import threading
from typing import Callable, Optional, List


class WakeWordDetector:
    """
    Wake word detector for LIAO Assistant.

    Default mode:
    - text simulation mode
    - keyword matching mode
    - callback trigger mode

    Later upgrade ready for:
    - microphone stream
    - speech recognition
    - Porcupine / Vosk / Whisper
    """

    def __init__(
        self,
        callback: Optional[Callable[[str], None]] = None,
        wake_words: Optional[List[str]] = None,
        cooldown_seconds: float = 2.0
    ) -> None:

        self.callback = callback
        self.wake_words = wake_words or [
            "hey liao",
            "hello liao",
            "liao",
            "nilima",
            "হে লিয়াও",
            "লিয়াও",
            "নিলিমা"
        ]

        self.cooldown_seconds = cooldown_seconds

        self._running = False
        self._thread = None
        self._last_trigger = 0.0

    # --------------------------------------------------
    # Public Controls
    # --------------------------------------------------
    def start(self) -> dict:
        """
        Start listening loop.
        """
        if self._running:
            return self._response(
                True,
                "Wake detector already running."
            )

        self._running = True

        self._thread = threading.Thread(
            target=self._listen_loop,
            daemon=True
        )
        self._thread.start()

        return self._response(
            True,
            "Wake detector started."
        )

    def stop(self) -> dict:
        """
        Stop listening loop.
        """
        self._running = False

        return self._response(
            True,
            "Wake detector stopped."
        )

    def is_running(self) -> bool:
        return self._running

    # --------------------------------------------------
    # Main Loop
    # --------------------------------------------------
    def _listen_loop(self) -> None:
        """
        Development mode:
        Reads text from terminal input.
        Replace later with microphone listener.
        """
        while self._running:
            try:
                text = input("🎤 Listening: ").strip()

                if not self._running:
                    break

                if text:
                    self.process_text(text)

            except KeyboardInterrupt:
                self._running = False

            except Exception:
                time.sleep(0.3)

    # --------------------------------------------------
    # Detection Logic
    # --------------------------------------------------
    def process_text(self, text: str) -> bool:
        """
        Check text for wake word.
        """
        normalized = text.lower().strip()

        if not normalized:
            return False

        if not self._cooldown_ready():
            return False

        for word in self.wake_words:
            if word in normalized:
                self._trigger(word)
                return True

        return False

    def add_wake_word(self, word: str) -> dict:
        value = word.strip().lower()

        if not value:
            return self._response(False, "Invalid wake word.")

        if value not in self.wake_words:
            self.wake_words.append(value)

        return self._response(
            True,
            "Wake word added."
        )

    def remove_wake_word(self, word: str) -> dict:
        value = word.strip().lower()

        if value in self.wake_words:
            self.wake_words.remove(value)

            return self._response(
                True,
                "Wake word removed."
            )

        return self._response(
            False,
            "Wake word not found."
        )

    def list_wake_words(self) -> List[str]:
        return list(self.wake_words)

    # --------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------
    def _trigger(self, word: str) -> None:
        self._last_trigger = time.time()

        print(f"🟢 Wake word detected: {word}")

        if self.callback:
            try:
                self.callback(word)
            except Exception:
                pass

    def _cooldown_ready(self) -> bool:
        return (
            time.time() - self._last_trigger
            >= self.cooldown_seconds
        )

    def _response(
        self,
        success: bool,
        message: str
    ) -> dict:
        return {
            "success": success,
            "message": message
        }


# --------------------------------------------------
# Local Test
# --------------------------------------------------
if __name__ == "__main__":

    def on_wake(word: str):
        print(f"🤖 Activated by: {word}")

    detector = WakeWordDetector(
        callback=on_wake
    )

    detector.start()

    while detector.is_running():
        time.sleep(1)