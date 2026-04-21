import time
import threading
import speech_recognition as sr


class WakeWordDetector:
    """
    LIAO AI Assistant Wake Word Detector

    Features:
    - continuous background listening
    - one-time microphone calibration
    - Bangla + English wake words
    - callback trigger system
    - low CPU usage
    - cooldown after activation
    """

    def __init__(self):
        self.recognizer = sr.Recognizer()

        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 0.6
        self.recognizer.dynamic_energy_threshold = True

        self.wake_words = [
            "hey liao",
            "hello liao",
            "liao",
            "লীআও",
            "লিয়াও",
            "হে লিয়াও"
        ]

        self.running = False
        self.listener_thread = None

        self.cooldown_seconds = 2
        self.last_trigger_time = 0

    def start(
        self,
        callback=None,
        language: str = "bn-BD"
    ):
        """
        Start background wake detector
        """
        if self.running:
            return

        self.running = True

        self.listener_thread = threading.Thread(
            target=self._listen_loop,
            args=(callback, language),
            daemon=True
        )

        self.listener_thread.start()

    def stop(self):
        """
        Stop detector
        """
        self.running = False

    def _listen_loop(
        self,
        callback,
        language: str
    ):
        """
        Continuous listening loop
        """
        try:
            with sr.Microphone() as source:
                print("Calibrating microphone...")

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=1
                )

                print("Wake detector ready.")

                while self.running:
                    try:
                        audio = self.recognizer.listen(
                            source,
                            timeout=3,
                            phrase_time_limit=4
                        )

                        text = self._recognize(
                            audio,
                            language
                        )

                        if text:
                            print("Heard:", text)

                        if self._is_wake_word(text):
                            current_time = time.time()

                            if (
                                current_time
                                - self.last_trigger_time
                                >= self.cooldown_seconds
                            ):
                                self.last_trigger_time = current_time

                                print("Wake word detected.")

                                if callback:
                                    callback(text)

                    except sr.WaitTimeoutError:
                        continue

                    except Exception:
                        time.sleep(0.5)

        except Exception:
            self.running = False

    def _recognize(
        self,
        audio,
        language: str = "bn-BD"
    ) -> str:
        """
        Speech to text
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

    def _is_wake_word(
        self,
        text: str
    ) -> bool:
        """
        Check wake word match
        """
        if not text:
            return False

        for wake in self.wake_words:
            if wake in text:
                return True

        return False

    def add_wake_word(
        self,
        word: str
    ):
        """
        Add custom wake word
        """
        cleaned = word.lower().strip()

        if cleaned and cleaned not in self.wake_words:
            self.wake_words.append(cleaned)

    def remove_wake_word(
        self,
        word: str
    ):
        """
        Remove custom wake word
        """
        cleaned = word.lower().strip()

        if cleaned in self.wake_words:
            self.wake_words.remove(cleaned)

    def get_wake_words(self):
        """
        Return wake words list
        """
        return self.wake_words.copy()


if __name__ == "__main__":
    def activated(text):
        print("Assistant Activated:", text)

    detector = WakeWordDetector()

    detector.start(callback=activated)

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        detector.stop()
        print("Stopped.")