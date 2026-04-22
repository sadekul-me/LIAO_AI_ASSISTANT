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
    Fixed & production stable version
    """

    def __init__(self):
        self.default_voice = "bn-BD-NabanitaNeural"
        self.default_rate = "+0%"
        self.default_volume = "+0%"

        self._play_lock = threading.Lock()
        self._init_audio_engine()

    def _init_audio_engine(self):
        try:
            pygame.mixer.init()
        except Exception as e:
            print("TTS Init Warning:", e)

    # --------------------------------------------------
    # CORE AUDIO GENERATION
    # --------------------------------------------------
    async def _generate_audio(
        self,
        text: str,
        output_file: str,
        voice: str = None,
        rate: str = None,
        volume: str = None
    ):
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice or self.default_voice,
            rate=rate or self.default_rate,
            volume=volume or self.default_volume
        )

        await communicate.save(output_file)

    # --------------------------------------------------
    # MAIN SPEAK FUNCTION
    # --------------------------------------------------
    def speak(
        self,
        text: str,
        voice: str = None,
        rate: str = None,
        volume: str = None
    ) -> str:
        """
        Returns audio file path (API friendly)
        """

        if not text or not text.strip():
            return ""

        temp_path = None

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

            return temp_path

        except Exception as e:
            print("TTS ERROR:", e)

            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

            return ""

    # --------------------------------------------------
    # ASYNC SPEAK (NON-BLOCKING)
    # --------------------------------------------------
    def speak_async(self, text: str, voice: str = None):
        thread = threading.Thread(
            target=self.speak,
            args=(text, voice),
            daemon=True
        )
        thread.start()

    # --------------------------------------------------
    # SAVE FILE ONLY
    # --------------------------------------------------
    def save_to_file(self, text: str, file_path: str, voice: str = None) -> bool:
        try:
            asyncio.run(
                self._generate_audio(
                    text=text,
                    output_file=file_path,
                    voice=voice
                )
            )
            return True
        except Exception as e:
            print("TTS SAVE ERROR:", e)
            return False

    # --------------------------------------------------
    # AUDIO PLAYBACK
    # --------------------------------------------------
    def _play_audio(self, file_path: str):
        try:
            with self._play_lock:
                if not pygame.mixer.get_init():
                    pygame.mixer.init()

                pygame.mixer.music.stop()
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)

        except Exception as e:
            print("PLAY ERROR:", e)

    # --------------------------------------------------
    # STOP AUDIO
    # --------------------------------------------------
    def stop(self):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

    # --------------------------------------------------
    # VOICE CONTROL
    # --------------------------------------------------
    def set_voice(self, voice_name: str):
        self.default_voice = voice_name

    # --------------------------------------------------
    # SAFE CLEANUP
    # --------------------------------------------------
    def cleanup(self, file_path: str):
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass