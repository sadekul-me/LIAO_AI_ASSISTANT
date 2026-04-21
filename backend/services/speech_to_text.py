import os
import tempfile
import speech_recognition as sr


class SpeechToTextService:
    """
    LIAO AI Assistant Speech To Text Service

    Responsibilities:
    - microphone listening
    - voice recognition
    - ambient noise adjustment
    - language support
    - safe fallback handling
    """

    def __init__(self):
        self.recognizer = sr.Recognizer()

        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 0.8
        self.recognizer.dynamic_energy_threshold = True

    def listen_once(
        self,
        language: str = "bn-BD",
        timeout: int = 5,
        phrase_time_limit: int = 10
    ) -> dict:
        """
        Listen once from microphone
        """
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=1
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

            text = self.recognize_audio(
                audio=audio,
                language=language
            )

            return {
                "success": True,
                "text": text,
                "message": "Voice captured successfully."
            }

        except sr.WaitTimeoutError:
            return {
                "success": False,
                "text": "",
                "message": "No voice detected."
            }

        except Exception as error:
            return {
                "success": False,
                "text": "",
                "message": f"Microphone error: {error}"
            }

    def recognize_audio(
        self,
        audio,
        language: str = "bn-BD"
    ) -> str:
        """
        Convert audio to text using Google Speech Recognition
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

    def transcribe_wav_file(
        self,
        file_path: str,
        language: str = "bn-BD"
    ) -> dict:
        """
        Convert local WAV audio file to text
        """
        try:
            with sr.AudioFile(file_path) as source:
                audio = self.recognizer.record(source)

            text = self.recognize_audio(
                audio=audio,
                language=language
            )

            return {
                "success": True,
                "text": text,
                "message": "File transcribed successfully."
            }

        except Exception as error:
            return {
                "success": False,
                "text": "",
                "message": f"Transcription failed: {error}"
            }

    def save_temp_audio(
        self,
        audio_data
    ) -> str:
        """
        Save temporary wav file if needed
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
            return ""

    def delete_temp_file(
        self,
        file_path: str
    ):
        """
        Remove temp file safely
        """
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)

        except Exception:
            pass


if __name__ == "__main__":
    stt = SpeechToTextService()

    print("Speak now...")

    result = stt.listen_once()

    print(result)