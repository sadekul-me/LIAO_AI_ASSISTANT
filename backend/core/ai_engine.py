import os
import json
import re
from datetime import datetime
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from google import genai
from groq import Groq


load_dotenv()


class AIEngine:
    """
    Core AI Engine for LIAO Assistant

    Provider Priority:
    1. Gemini
    2. Groq
    3. Offline Rules Engine
    """

    def __init__(self):
        # -------------------------
        # API Keys
        # -------------------------
        self.gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.groq_key = os.getenv("GROQ_API_KEY", "").strip()

        # -------------------------
        # Clients
        # -------------------------
        self.gemini_client = None
        self.groq_client = None

        if self.gemini_key:
            try:
                self.gemini_client = genai.Client(
                    api_key=self.gemini_key
                )
            except Exception as e:
                print("Gemini Init Failed:", str(e))

        if self.groq_key:
            try:
                self.groq_client = Groq(
                    api_key=self.groq_key
                )
            except Exception as e:
                print("Groq Init Failed:", str(e))

        # -------------------------
        # Models
        # -------------------------
        self.gemini_model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.0-flash"
        )

        self.groq_model = os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile"
        )

        # -------------------------
        # System Prompt
        # -------------------------
        self.system_prompt = self._load_system_prompt()

        # -------------------------
        # Runtime State
        # -------------------------
        self.last_provider = "offline"

    # =================================================
    # SYSTEM PROMPT
    # =================================================
    def _load_system_prompt(self) -> str:
        return """
তুমি LIAO AI Assistant এর স্মার্ট সহকারী "Nilima"।

নিয়ম:
- সবসময় পরিষ্কার বাংলায় উত্তর দেবে
- সংক্ষিপ্ত কিন্তু কার্যকর হবে
- friendly এবং professional tone রাখবে
- technical প্রশ্নে smart help করবে
- অপ্রয়োজনীয় বড় উত্তর দেবে না
"""

    # =================================================
    # PROMPT BUILDER
    # =================================================
    def _build_prompt(
        self,
        user_input: str,
        context: str = ""
    ) -> str:
        return f"""
System:
{self.system_prompt}

Context:
{context}

User:
{user_input}

Assistant:
"""

    # =================================================
    # MAIN RESPONSE
    # =================================================
    def generate_response(
        self,
        user_input: str,
        context: str = ""
    ) -> str:

        prompt = self._build_prompt(
            user_input=user_input,
            context=context
        )

        # 1. Gemini
        response = self._ask_gemini(prompt)
        if response:
            self.last_provider = "gemini"
            return response

        # 2. Groq
        response = self._ask_groq(prompt)
        if response:
            self.last_provider = "groq"
            return response

        # 3. Offline
        self.last_provider = "offline"
        return self._offline_response(user_input)

    # =================================================
    # GEMINI
    # =================================================
    def _ask_gemini(
        self,
        prompt: str
    ) -> Optional[str]:

        if not self.gemini_client:
            return None

        try:
            result = self.gemini_client.models.generate_content(
                model=self.gemini_model,
                contents=prompt
            )

            if result and hasattr(result, "text"):
                text = result.text.strip()

                if text:
                    print("🟢 Provider: Gemini")
                    return text

        except Exception as e:
            print("🔴 Gemini Failed:", str(e))

        return None

    # =================================================
    # GROQ
    # =================================================
    def _ask_groq(
        self,
        prompt: str
    ) -> Optional[str]:

        if not self.groq_client:
            return None

        try:
            result = self.groq_client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.6
            )

            text = (
                result.choices[0]
                .message
                .content
                .strip()
            )

            if text:
                print("🟡 Provider: Groq")
                return text

        except Exception as e:
            print("🔴 Groq Failed:", str(e))

        return None

    # =================================================
    # INTENT DETECTION
    # =================================================
    def detect_intent(
        self,
        user_input: str
    ) -> Dict[str, Any]:

        text = user_input.lower().strip()

        # Open App
        if "open" in text or "খুলো" in text:
            if "chrome" in text:
                return {
                    "intent": "open_app",
                    "target": "chrome",
                    "message": "Chrome খুলছি।"
                }

            if "vscode" in text or "vs code" in text:
                return {
                    "intent": "open_app",
                    "target": "vscode",
                    "message": "VS Code খুলছি।"
                }

            if "notepad" in text:
                return {
                    "intent": "open_app",
                    "target": "notepad",
                    "message": "Notepad খুলছি।"
                }

        # Search
        if "search" in text or "google" in text:
            return {
                "intent": "search_web",
                "target": user_input,
                "message": "ওয়েবে খুঁজছি।"
            }

        # Time
        if "time" in text or "সময়" in text:
            return {
                "intent": "system_action",
                "target": "time",
                "message": "সময় দেখাচ্ছি।"
            }

        # File
        if "create file" in text or "file" in text:
            return {
                "intent": "create_file",
                "target": "",
                "message": "ফাইল তৈরি করছি।"
            }

        return self._default_intent()

    # =================================================
    # SAFE JSON PARSER
    # =================================================
    def safe_json(
        self,
        text: str
    ) -> Dict[str, Any]:

        try:
            match = re.search(
                r"\{.*\}",
                text,
                re.DOTALL
            )

            if match:
                return json.loads(match.group())

        except Exception:
            pass

        return self._default_intent()

    # =================================================
    # OFFLINE RULES ENGINE
    # =================================================
    def _offline_response(
        self,
        user_input: str
    ) -> str:

        text = user_input.lower().strip()

        greetings = [
            "hi",
            "hello",
            "hey",
            "helo"
        ]

        if text in greetings:
            return "হ্যালো, আমি আছি। কীভাবে সাহায্য করতে পারি?"

        if "who are you" in text:
            return "আমি LIAO AI Assistant, তোমার স্মার্ট সহকারী।"

        if "time" in text or "সময়" in text:
            now = datetime.now().strftime("%I:%M %p")
            return f"এখন সময় {now}"

        if "thank" in text:
            return "সবসময় পাশে আছি।"

        if "bye" in text:
            return "আবার কথা হবে। ভালো থাকো।"

        return "এই মুহূর্তে online AI unavailable. আমি basic mode এ আছি।"

    # =================================================
    # DEFAULT INTENT
    # =================================================
    def _default_intent(self) -> Dict[str, Any]:
        return {
            "intent": "chat",
            "target": "",
            "message": ""
        }

    # =================================================
    # PROVIDER STATUS
    # =================================================
    def get_provider(self) -> str:
        return self.last_provider


# =====================================================
# LOCAL TEST
# =====================================================
if __name__ == "__main__":
    ai = AIEngine()

    while True:
        msg = input("You: ").strip()

        if msg.lower() == "exit":
            break

        reply = ai.generate_response(msg)

        print("AI:", reply)
        print("Provider:", ai.get_provider())
        print("-" * 50)