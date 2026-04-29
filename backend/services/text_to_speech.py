import os
import re
import time
import uuid
import asyncio
import threading
from pathlib import Path
from typing import Optional, Dict, Any

import edge_tts
import pygame


class TextToSpeechService:
    """
    🔥 LIAO AI Assistant - ULTRA PRO TTS v2

    Features
    -----------------------------------
    ✅ FastAPI Safe
    ✅ No asyncio.run conflict
    ✅ Auto Bangla / English voice detect
    ✅ Stable Windows support
    ✅ Static file output support
    ✅ Temp file support
    ✅ Clean playback system
    ✅ Production ready
    """

    # ==========================================
    # INIT
    # ==========================================
    def __init__(self):

        # Voice Profiles
        self.bn_voice = "bn-BD-NabanitaNeural"
        self.bn_male = "bn-BD-PradeepNeural"

        self.en_voice = "en-US-AriaNeural"
        self.en_male = "en-US-GuyNeural"

        # Default style
        self.default_rate = "+0%"
        self.default_volume = "+0%"
        self.default_pitch = "+0Hz"

        # File system
        self.static_dir = Path("static")
        self.static_dir.mkdir(parents=True, exist_ok=True)

        # Audio lock
        self._play_lock = threading.Lock()

        # Init pygame mixer
        self._init_audio()

    # ==========================================
    # AUDIO ENGINE
    # ==========================================
    def _init_audio(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except Exception as e:
            print("🔇 Audio Init Warning:", e)

    # ==========================================
    # LANGUAGE DETECT
    # ==========================================
    def _contains_bangla(self, text: str) -> bool:
        return bool(re.search(r'[\u0980-\u09FF]', text))

    def _select_voice(self, text: str, voice: Optional[str]) -> str:

        if voice:
            return voice

        if self._contains_bangla(text):
            return self.bn_voice

        return self.en_voice

    # ==========================================
    # GENERATE AUDIO
    # ==========================================
    async def _generate(
        self,
        text: str,
        output_path: str,
        voice: str,
        rate: str,
        volume: str,
        pitch: str
    ):

        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate,
            volume=volume,
            pitch=pitch
        )

        await communicate.save(output_path)

    # ==========================================
    # SAFE ASYNC RUNNER
    # ==========================================
    def _run_async_safe(self, coro):

        try:
            loop = asyncio.get_event_loop()

            if loop.is_running():

                result = {}

                def runner():
                    new_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(new_loop)

                    try:
                        new_loop.run_until_complete(coro)
                    finally:
                        new_loop.close()

                t = threading.Thread(target=runner)
                t.start()
                t.join()

            else:
                loop.run_until_complete(coro)

        except RuntimeError:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)

            try:
                new_loop.run_until_complete(coro)
            finally:
                new_loop.close()

    # ==========================================
    # MAIN SPEAK
    # ==========================================
    def speak(
        self,
        text: str,
        output_path: Optional[str] = None,
        voice: Optional[str] = None,
        rate: Optional[str] = None,
        volume: Optional[str] = None,
        pitch: Optional[str] = None
    ) -> Dict[str, Any]:

        if not text or not text.strip():
            return {
                "success": False,
                "audio_path": None,
                "error": "Empty text"
            }

        text = text.strip()

        try:
            # Voice select
            selected_voice = self._select_voice(text, voice)

            # Output path
            if not output_path:
                file_name = f"liao_{uuid.uuid4().hex[:8]}.mp3"
                output_path = str(self.static_dir / file_name)

            # Generate
            self._run_async_safe(
                self._generate(
                    text=text,
                    output_path=output_path,
                    voice=selected_voice,
                    rate=rate or self.default_rate,
                    volume=volume or self.default_volume,
                    pitch=pitch or self.default_pitch
                )
            )

            return {
                "success": True,
                "audio_path": output_path,
                "voice": selected_voice,
                "error": None
            }

        except Exception as e:
            print("🔥 TTS ERROR:", e)

            return {
                "success": False,
                "audio_path": None,
                "error": str(e)
            }

    # ==========================================
    # PLAY AUDIO
    # ==========================================
    def play(self, file_path: str) -> bool:

        try:
            with self._play_lock:

                if not pygame.mixer.get_init():
                    pygame.mixer.init()

                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()

            return True

        except Exception as e:
            print("🔊 Play Error:", e)
            return False

    # ==========================================
    # PLAY + WAIT
    # ==========================================
    def play_and_wait(self, file_path: str):

        try:
            with self._play_lock:

                if not pygame.mixer.get_init():
                    pygame.mixer.init()

                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)

                try:
                    pygame.mixer.music.unload()
                except:
                    pass

        except Exception as e:
            print("🔊 Play Wait Error:", e)

    # ==========================================
    # STOP
    # ==========================================
    def stop(self):

        try:
            pygame.mixer.music.stop()
        except:
            pass

    # ==========================================
    # CLEANUP
    # ==========================================
    def cleanup(self, file_path: str):

        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print("🧹 Cleanup Error:", e)

    # ==========================================
    # QUICK TEST
    # ==========================================
    def test(self):

        result = self.speak("হ্যালো সাদিক, আমি লিয়াও এআই এসিস্ট্যান্ট।")

        if result["success"]:
            print("✅ Generated:", result["audio_path"])
            self.play_and_wait(result["audio_path"])
        else:
            print("❌ Failed:", result["error"])


# ==========================================
# MAIN TEST
# ==========================================
if __name__ == "__main__":

    tts = TextToSpeechService()
    tts.test()