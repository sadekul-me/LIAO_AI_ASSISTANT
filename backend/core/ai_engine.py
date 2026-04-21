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

    Provider Order:
    1. Gemini
    2. Groq
    3. Offline Rules Engine
    """

    def __init__(self) -> None:
        # -----------------------------------
        # Environment
        # -----------------------------------
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.groq_api_key = os.getenv("GROQ_API_KEY", "").strip()

        self.gemini_model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.0-flash"
        ).strip()

        self.groq_model = os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile"
        ).strip()

        # -----------------------------------
        # Clients
        # -----------------------------------
        self.gemini_client = self._create_gemini_client()
        self.groq_client = self._create_groq_client()

        # -----------------------------------
        # Runtime State
        # -----------------------------------
        self.last_provider = "offline"

        # -----------------------------------
        # Prompt Cache
        # -----------------------------------
        self.system_prompt = self._system_prompt()

    # ==================================================
    # CLIENT INITIALIZATION
    # ==================================================
    def _create_gemini_client(self):
        if not self.gemini_api_key:
            return None

        try:
            return genai.Client(api_key=self.gemini_api_key)
        except Exception as error:
            print("Gemini initialization failed:", error)
            return None

    def _create_groq_client(self):
        if not self.groq_api_key:
            return None

        try:
            return Groq(api_key=self.groq_api_key)
        except Exception as error:
            print("Groq initialization failed:", error)
            return None

    # ==================================================
    # SYSTEM PROMPT
    # ==================================================
    def _system_prompt(self) -> str:
        return """
তুমি LIAO AI Assistant এর সহকারী "Nilima"।

নির্দেশনা:
- সবসময় স্বাভাবিক ও পরিষ্কার বাংলায় উত্তর দেবে
- সংক্ষিপ্ত কিন্তু কার্যকর হবে
- friendly এবং professional থাকবে
- technical বিষয়ে সহায়ক হবে
- অপ্রয়োজনীয় বড় উত্তর দেবে না
"""

    # ==================================================
    # PROMPT BUILDER
    # ==================================================
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

    # ==================================================
    # PUBLIC RESPONSE METHOD
    # ==================================================
    def generate_response(
        self,
        user_input: str,
        context: str = ""
    ) -> str:

        prompt = self._build_prompt(
            user_input=user_input,
            context=context
        )

        response = self._generate_with_gemini(prompt)

        if response:
            self.last_provider = "gemini"
            return response

        response = self._generate_with_groq(prompt)

        if response:
            self.last_provider = "groq"
            return response

        self.last_provider = "offline"

        return self._offline_response(user_input)

    # ==================================================
    # GEMINI PROVIDER
    # ==================================================
    def _generate_with_gemini(
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

            text = getattr(result, "text", "")

            if text:
                print("🟢 Provider: Gemini")
                return text.strip()

        except Exception as error:
            print("🔴 Gemini Failed:", error)

        return None

    # ==================================================
    # GROQ PROVIDER
    # ==================================================
    def _generate_with_groq(
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
            )

            if text:
                print("🟡 Provider: Groq")
                return text.strip()

        except Exception as error:
            print("🔴 Groq Failed:", error)

        return None

    # ==================================================
    # INTENT DETECTION
    # ==================================================
    def detect_intent(
        self,
        user_input: str
    ) -> Dict[str, Any]:

        text = user_input.lower().strip()

        if self._contains_any(text, ["open", "খুলো", "launch"]):
            app = self._extract_app(text)

            if app:
                return {
                    "intent": "open_app",
                    "target": app,
                    "message": f"{app} খুলছি।"
                }

        if self._contains_any(text, ["search", "google", "find"]):
            return {
                "intent": "search_web",
                "target": user_input,
                "message": "ওয়েবে খুঁজছি।"
            }

        if self._contains_any(text, ["time", "সময়"]):
            return {
                "intent": "system_action",
                "target": "time",
                "message": "সময় দেখাচ্ছি।"
            }

        if self._contains_any(text, ["file", "create file"]):
            return {
                "intent": "create_file",
                "target": "",
                "message": "ফাইল তৈরি করছি।"
            }

        return self._default_intent()

    # ==================================================
    # APP EXTRACTION
    # ==================================================
    def _extract_app(self, text: str) -> str:
        apps = {
            "chrome": ["chrome", "google chrome"],
            "vscode": ["vscode", "vs code"],
            "notepad": ["notepad"],
            "calculator": ["calculator", "calc"]
        }

        for app_name, aliases in apps.items():
            if self._contains_any(text, aliases):
                return app_name

        return ""

    # ==================================================
    # HELPERS
    # ==================================================
    def _contains_any(
        self,
        text: str,
        keywords: list
    ) -> bool:
        return any(word in text for word in keywords)

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

    # ==================================================
    # OFFLINE ENGINE
    # ==================================================
    def _offline_response(
        self,
        user_input: str
    ) -> str:

        text = user_input.lower().strip()

        if text in ["hi", "hello", "hey", "helo"]:
            return "হ্যালো, আমি আছি। কীভাবে সাহায্য করতে পারি?"

        if "কেমন আছো" in text:
            return "ভালো আছি। আপনি কেমন আছেন?"

        if "who are you" in text:
            return "আমি LIAO AI Assistant।"

        if "time" in text or "সময়" in text:
            now = datetime.now().strftime("%I:%M %p")
            return f"এখন সময় {now}"

        if "thank" in text:
            return "সবসময় পাশে আছি।"

        if "bye" in text:
            return "আবার কথা হবে। ভালো থাকুন।"

        return "এই মুহূর্তে online AI unavailable. আমি basic mode এ আছি।"

    # ==================================================
    # DEFAULTS
    # ==================================================
    def _default_intent(self) -> Dict[str, Any]:
        return {
            "intent": "chat",
            "target": "",
            "message": ""
        }

    def get_provider(self) -> str:
        return self.last_provider


# ==================================================
# LOCAL TEST
# ==================================================
if __name__ == "__main__":
    engine = AIEngine()

    while True:
        message = input("You: ").strip()

        if message.lower() == "exit":
            break

        reply = engine.generate_response(message)

        print("AI:", reply)
        print("Provider:", engine.get_provider())
        print("-" * 50)