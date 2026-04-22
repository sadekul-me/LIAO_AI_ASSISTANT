import os
import tempfile
import speech_recognition as sr
from typing import Dict, Any, Optional


class SpeechToTextService:
    """
    Speech To Text Service

    Responsibilities:
    - Microphone input handling
    - Speech recognition (Google API)
    - File-based transcription
    - Safe error handling
    """

    def __init__(self):
        self.recognizer = sr.Recognizer()

        # tuned defaults for stability
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

    # --------------------------------------
    # MICROPHONE LISTEN
    # --------------------------------------
    def listen_once(
        self,
        language: str = "bn-BD",
        timeout: int = 5,
        phrase_time_limit: int = 10
    ) -> Dict[str, Any]:
        """
        Capture voice from microphone once
        """

        try:
            with sr.Microphone() as source:
                print("🎤 Calibrating microphone...")

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=1
                )

                print("🟢 Listening...")

                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

            text = self._recognize(audio, language)

            return {
                "success": True,
                "text": text,
                "message": "Voice captured successfully"
            }

        except sr.WaitTimeoutError:
            return {
                "success": False,
                "text": "",
                "message": "No voice detected"
            }

        except Exception as e:
            return {
                "success": False,
                "text": "",
                "message": f"Microphone error: {str(e)}"
            }

    # --------------------------------------
    # SPEECH RECOGNITION CORE
    # --------------------------------------
    def _recognize(
        self,
        audio,
        language: str = "bn-BD"
    ) -> str:
        """
        Convert speech to text
        """

        try:
            text = self.recognizer.recognize_google(
                audio,
                language=language
            )

            return text.strip()

        except sr.UnknownValueError:
            return ""

        except sr.RequestError:
            return ""

        except Exception:
            return ""

    # --------------------------------------
    # FILE TRANSCRIPTION
    # --------------------------------------
    def transcribe_wav_file(
        self,
        file_path: str,
        language: str = "bn-BD"
    ) -> Dict[str, Any]:
        """
        Transcribe audio file
        """

        try:
            with sr.AudioFile(file_path) as source:
                audio = self.recognizer.record(source)

            text = self._recognize(audio, language)

            return {
                "success": True,
                "text": text,
                "message": "File transcribed successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "text": "",
                "message": f"Transcription failed: {str(e)}"
            }

    # --------------------------------------
    # TEMP FILE HANDLING
    # --------------------------------------
    def save_temp_audio(self, audio_data) -> Optional[str]:
        """
        Save temporary wav file
        """

        try:
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".wav"
            )

            temp_file.write(audio_data.get_wav_data())
            temp_file.close()

            return temp_file.name

        except Exception:
            return None

    def delete_temp_file(self, file_path: str):
        """
        Safe file cleanup
        """

        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)

        except Exception:
            pass


# --------------------------------------
# LOCAL TEST
# --------------------------------------
if __name__ == "__main__":

    stt = SpeechToTextService()

    print("🎤 Speak now...")

    result = stt.listen_once()

    print("Result:", result)