import os
import time
import asyncio
import tempfile
import threading
import edge_tts
import pygame


class TextToSpeechService:
    """
    LIAO AI Assistant Text To Speech Service

    Features:
    - background speech playback
    - no popup media player
    - Bangla / English voices
    - thread-safe speaking lock
    - temp file cleanup
    """

    def __init__(self):
        self.default_voice = "bn-BD-NabanitaNeural"
        self.default_rate = "+0%"
        self.default_volume = "+0%"

        self._play_lock = threading.Lock()

        self._init_audio_engine()

    def _init_audio_engine(self):
        """
        Initialize pygame mixer once
        """
        try:
            pygame.mixer.init()
        except Exception:
            pass

    async def _generate_audio(
        self,
        text: str,
        output_file: str,
        voice: str = None,
        rate: str = None,
        volume: str = None
    ):
        """
        Generate speech mp3 file
        """
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice or self.default_voice,
            rate=rate or self.default_rate,
            volume=volume or self.default_volume
        )

        await communicate.save(output_file)

    def speak(
        self,
        text: str,
        voice: str = None,
        rate: str = None,
        volume: str = None
    ) -> dict:
        """
        Generate and play speech
        """
        if not text.strip():
            return {
                "success": False,
                "message": "Empty text provided."
            }

        temp_path = ""

        try:
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".mp3"
            )

            temp_path = temp_file.name
            temp_file.close()

            asyncio.run(
                self._generate_audio(
                    text=text,
                    output_file=temp_path,
                    voice=voice,
                    rate=rate,
                    volume=volume
                )
            )

            self._play_audio(temp_path)

            self._safe_delete(temp_path)

            return {
                "success": True,
                "message": "Speech played successfully."
            }

        except Exception as error:
            self._safe_delete(temp_path)

            return {
                "success": False,
                "message": f"TTS error: {error}"
            }

    def speak_async(
        self,
        text: str,
        voice: str = None
    ):
        """
        Non-blocking speech
        """
        thread = threading.Thread(
            target=self.speak,
            args=(text, voice),
            daemon=True
        )

        thread.start()

    def save_to_file(
        self,
        text: str,
        file_path: str,
        voice: str = None
    ) -> dict:
        """
        Save speech file
        """
        try:
            asyncio.run(
                self._generate_audio(
                    text=text,
                    output_file=file_path,
                    voice=voice
                )
            )

            return {
                "success": True,
                "message": "Audio saved successfully."
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Save failed: {error}"
            }

    def _play_audio(
        self,
        file_path: str
    ):
        """
        Background playback without popup
        """
        try:
            with self._play_lock:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()

                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)

        except Exception:
            pass

    def stop(self):
        """
        Stop current speech
        """
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

    def set_voice(
        self,
        voice_name: str
    ):
        """
        Change default voice
        """
        self.default_voice = voice_name

    def _safe_delete(
        self,
        file_path: str
    ):
        """
        Delete temp file safely
        """
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass


if __name__ == "__main__":
    tts = TextToSpeechService()

    tts.speak(
        "হ্যালো সাদিক, আমি লিয়াও অ্যাসিস্ট্যান্ট। আজকে কী কাজ করবো?"
    )