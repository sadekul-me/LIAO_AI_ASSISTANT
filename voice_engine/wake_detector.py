import os
import re
import time
import threading
import requests
import speech_recognition as sr
from pygame import mixer


class JarvisAssistant:
    """
    🔥 LIAO / JARVIS ULTRA PRO v5
    --------------------------------
    ✅ Fixed Backend Detection
    ✅ Correct JSON Payload Support
    ✅ Auto Route Scanner
    ✅ No Fake Offline Error
    ✅ Bangla + English Hybrid STT
    ✅ Better Wake Word Detection
    ✅ Smart Retry System
    ✅ Cleaner Logs
    ✅ Thread Safe
    """

    # ==================================================
    # INIT
    # ==================================================
    def __init__(self):

        # Speech Recognition
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 280
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.7
        self.recognizer.non_speaking_duration = 0.4

        # Wake Words
        self.wake_words = [
            "liao",
            "leo",
            "hey liao",
            "hello liao",
            "লিয়াও",
            "হে লিয়াও",
            "লি আও"
        ]

        # Backend Routes
        self.api_routes = [
            "http://127.0.0.1:8000/chat",
            "http://127.0.0.1:8000/api/chat"
        ]

        self.api_url = None

        # States
        self.running = False
        self.is_thinking = False

        # Memory
        self.last_command = ""
        self.last_reply = ""

        # Lock
        self.lock = threading.Lock()

        # Audio
        try:
            mixer.init()
            self.audio_ready = True
        except:
            self.audio_ready = False

    # ==================================================
    # SOUND
    # ==================================================
    def _play_sound(self, state):

        if not self.audio_ready:
            return

        try:
            sounds = {
                "wake": "static/sounds/wake.mp3",
                "thinking": "static/sounds/thinking.mp3",
                "done": "static/sounds/done.mp3",
                "error": "static/sounds/error.mp3"
            }

            path = sounds.get(state)

            if path and os.path.exists(path):
                mixer.music.load(path)
                mixer.music.play()

        except:
            pass

    # ==================================================
    # BACKEND DETECTOR
    # ==================================================
    def _detect_backend(self):

        print("🔍 Scanning backend routes...")

        for url in self.api_routes:

            try:
                # GET health check first
                r = requests.get(url, timeout=3)

                if r.status_code == 200:
                    self.api_url = url
                    print(f"✅ Backend Connected: {url}")
                    return True

            except:
                pass

        print("❌ No backend route found.")
        self.api_url = None
        return False

    # ==================================================
    # HYBRID SPEECH TO TEXT
    # ==================================================
    def _recognize(self, audio):

        # Bangla first
        try:
            text = self.recognizer.recognize_google(
                audio,
                language="bn-BD"
            )

            if text:
                return text.lower().strip()

        except:
            pass

        # English fallback
        try:
            text = self.recognizer.recognize_google(
                audio,
                language="en-US"
            )

            if text:
                return text.lower().strip()

        except:
            pass

        return ""

    # ==================================================
    # WAKE WORD CHECK
    # ==================================================
    def _contains_wake_word(self, text):

        text = text.lower()

        for word in self.wake_words:
            if text.startswith(word) or word in text:
                return True

        return False

    # ==================================================
    # REMOVE WAKE WORD
    # ==================================================
    def _extract_command(self, text):

        cmd = text.lower()

        for word in self.wake_words:
            cmd = cmd.replace(word, "")

        cmd = re.sub(r"\s+", " ", cmd).strip()

        return cmd

    # ==================================================
    # ASK AI
    # ==================================================
    def _ask_ai(self, text):

        with self.lock:
            self.is_thinking = True

        self.last_command = text

        print("\n🤖 Thinking...")
        print(f"🧠 Command: {text}")

        self._play_sound("thinking")

        try:

            # Detect backend if missing
            if not self.api_url:
                if not self._detect_backend():
                    print("❌ Backend server not running.")
                    return

            # Correct payload for your backend
            payload = {
                "message": text,
                "session_id": "voice_user"
            }

            res = requests.post(
                self.api_url,
                json=payload,
                timeout=20
            )

            if res.status_code == 200:

                data = res.json()

                reply = data.get("reply", "I'm here.")
                provider = data.get("provider", "unknown")

                self.last_reply = reply

                print(f"🎙️ Jarvis: {reply}")
                print(f"⚡ Provider: {provider}")

                self._play_sound("done")

            else:
                print(f"⚠️ Backend Error: {res.status_code}")
                print(res.text)
                self._play_sound("error")

        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to backend.")
            self.api_url = None
            self._play_sound("error")

        except requests.exceptions.Timeout:
            print("⌛ Backend timeout.")
            self._play_sound("error")

        except Exception as e:
            print(f"❌ AI Error: {e}")
            self._play_sound("error")

        finally:
            with self.lock:
                self.is_thinking = False

    # ==================================================
    # FOLLOWUP MODE
    # ==================================================
    def _followup_listen(self, source):

        print("👂 Listening for command...")

        try:
            audio = self.recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=7
            )

            text = self._recognize(audio)

            if text:
                threading.Thread(
                    target=self._ask_ai,
                    args=(text,),
                    daemon=True
                ).start()
            else:
                print("⌛ No command heard.")

        except:
            print("⌛ Timeout.")

    # ==================================================
    # MAIN LOOP
    # ==================================================
    def _listen_loop(self):

        with sr.Microphone() as source:

            print("🎤 Calibrating microphone...")

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            print("🌐 Jarvis ONLINE")
            print("👂 Waiting for wake word...\n")

            while self.running:

                if self.is_thinking:
                    time.sleep(0.2)
                    continue

                try:
                    audio = self.recognizer.listen(
                        source,
                        timeout=2,
                        phrase_time_limit=5
                    )

                    text = self._recognize(audio)

                    if not text:
                        continue

                    print(f"📝 Heard: {text}")

                    if self._contains_wake_word(text):

                        print("⚡ Activated")
                        self._play_sound("wake")

                        command = self._extract_command(text)

                        if command:
                            threading.Thread(
                                target=self._ask_ai,
                                args=(command,),
                                daemon=True
                            ).start()
                        else:
                            self._followup_listen(source)

                except sr.WaitTimeoutError:
                    continue

                except Exception as e:
                    print(f"⚠️ Sensor Error: {e}")

    # ==================================================
    # START
    # ==================================================
    def start(self):

        if self.running:
            return

        self.running = True

        self._detect_backend()

        self.thread = threading.Thread(
            target=self._listen_loop,
            daemon=True
        )

        self.thread.start()

        print("🚀 Jarvis Boot Complete.")

    # ==================================================
    # STOP
    # ==================================================
    def stop(self):

        self.running = False

        try:
            mixer.music.stop()
        except:
            pass

        print("🛑 Jarvis Shutdown Complete.")

    # ==================================================
    # STATUS
    # ==================================================
    def status(self):

        return {
            "running": self.running,
            "thinking": self.is_thinking,
            "backend": self.api_url,
            "last_command": self.last_command,
            "last_reply": self.last_reply
        }


# ==================================================
# MAIN
# ==================================================
if __name__ == "__main__":

    jarvis = JarvisAssistant()
    jarvis.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        jarvis.stop()