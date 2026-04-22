import time
import threading
import speech_recognition as sr
from typing import Callable, Optional, List


class WakeWordDetector:
    """
    Wake Word Detection System (Background Listener)

    Features:
    - Continuous background listening
    - Callback trigger system
    - Bangla + English wake words support
    - Noise calibration
    - Cooldown control
    - Safe threading lifecycle
    """

    def __init__(self):
        self.recognizer = sr.Recognizer()

        # Better tuned defaults
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.7

        self.wake_words: List[str] = [
            "hey liao",
            "hello liao",
            "liao",
            "লীআও",
            "লিয়াও",
            "হে লিয়াও"
        ]

        self.running = False
        self.thread: Optional[threading.Thread] = None

        self.cooldown_seconds = 2
        self._last_trigger_time = 0

    # --------------------------------------
    # START LISTENER
    # --------------------------------------
    def start(
        self,
        callback: Optional[Callable[[str], None]] = None,
        language: str = "bn-BD"
    ):
        """
        Start background wake word detection
        """

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._listen_loop,
            args=(callback, language),
            daemon=True
        )

        self.thread.start()

    # --------------------------------------
    # STOP LISTENER
    # --------------------------------------
    def stop(self):
        """
        Stop background listener safely
        """
        self.running = False

    # --------------------------------------
    # MAIN LOOP
    # --------------------------------------
    def _listen_loop(
        self,
        callback: Optional[Callable],
        language: str
    ):
        """
        Continuous microphone listening loop
        """

        try:
            with sr.Microphone() as source:
                print("🎤 Calibrating microphone...")

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=1
                )

                print("🟢 Wake detector is running...")

                while self.running:
                    try:
                        audio = self.recognizer.listen(
                            source,
                            timeout=3,
                            phrase_time_limit=4
                        )

                        text = self._recognize(audio, language)

                        if text:
                            print("🗣️ Heard:", text)

                        if self._is_wake_word(text):
                            now = time.time()

                            if now - self._last_trigger_time >= self.cooldown_seconds:
                                self._last_trigger_time = now

                                print("⚡ Wake word triggered")

                                if callback:
                                    callback(text)

                    except sr.WaitTimeoutError:
                        continue

                    except Exception as e:
                        print("⚠️ Listener error:", str(e))
                        time.sleep(0.3)

        except Exception as e:
            print("🔥 Microphone error:", str(e))
            self.running = False

    # --------------------------------------
    # SPEECH RECOGNITION
    # --------------------------------------
    def _recognize(self, audio, language: str) -> str:
        """
        Convert speech to text
        """

        try:
            text = self.recognizer.recognize_google(
                audio,
                language=language
            )

            return text.lower().strip()

        except sr.UnknownValueError:
            return ""

        except sr.RequestError:
            return ""

        except Exception:
            return ""

    # --------------------------------------
    # WAKE WORD CHECK
    # --------------------------------------
    def _is_wake_word(self, text: str) -> bool:
        """
        Check if wake word exists in text
        """

        if not text:
            return False

        for word in self.wake_words:
            if word in text:
                return True

        return False

    # --------------------------------------
    # ADD WAKE WORD
    # --------------------------------------
    def add_wake_word(self, word: str):
        cleaned = word.lower().strip()

        if cleaned and cleaned not in self.wake_words:
            self.wake_words.append(cleaned)

    # --------------------------------------
    # REMOVE WAKE WORD
    # --------------------------------------
    def remove_wake_word(self, word: str):
        cleaned = word.lower().strip()

        if cleaned in self.wake_words:
            self.wake_words.remove(cleaned)

    # --------------------------------------
    # GET WAKE WORDS
    # --------------------------------------
    def get_wake_words(self):
        return list(self.wake_words)


# --------------------------------------
# LOCAL TEST
# --------------------------------------
if __name__ == "__main__":

    def on_wake(text):
        print("🚀 Assistant Activated with:", text)

    detector = WakeWordDetector()
    detector.start(callback=on_wake)

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        detector.stop()
        print("🛑 Wake detector stopped")