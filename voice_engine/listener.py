import speech_recognition as sr
from typing import Optional


class VoiceListener:
    """
    Voice Input Handler for LIAO AI Assistant

    Responsibilities:
    - Capture microphone audio
    - Convert speech to text
    - Return clean string output
    """

    def __init__(self, timeout: int = 5, phrase_time_limit: int = 8, language: str = "en-IN"):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit
        self.language = language

        # Optional tuning (noise handling)
        self.recognizer.dynamic_energy_threshold = True

    # --------------------------------------
    # LISTEN FROM MICROPHONE
    # --------------------------------------
    def listen(self) -> Optional[str]:
        """
        Listen from mic and convert speech to text
        Returns:
            str | None
        """

        try:
            with self.microphone as source:
                print("🎤 Listening...")

                # adjust for background noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

                audio = self.recognizer.listen(
                    source,
                    timeout=self.timeout,
                    phrase_time_limit=self.phrase_time_limit
                )

            # Speech to text (Google API)
            text = self.recognizer.recognize_google(
                audio,
                language=self.language
            )

            text = text.strip()

            if text:
                print("🗣️ Recognized:", text)
                return text

            return None

        # --------------------------------------
        # ERROR HANDLING
        # --------------------------------------
        except sr.WaitTimeoutError:
            print("⏳ No speech detected (timeout)")
            return None

        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None

        except sr.RequestError as e:
            print("🌐 Speech API error:", str(e))
            return None

        except Exception as e:
            print("🔥 Listener crash:", str(e))
            return None