import os
import time
import subprocess
import webbrowser
import threading
from typing import Optional, Dict, Any, Callable, List

from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI

from backend.core.prompt_engine import PromptEngine
from backend.core.context_manager import ContextManager
from backend.core.memory_engine import MemoryEngine
from backend.core.decision_engine import DecisionEngine

load_dotenv()


class AIEngine:
    """
    🔥 LIAO / JARVIS CORE v7.0 (HIGH PERFORMANCE EDITION)

    Upgrades:
    - Faster provider priority
    - Lower API traffic
    - Thread-safe status
    - Smart fallback
    - Prompt token optimization
    - Better timeout protection
    - Cleaner action engine
    """

    def __init__(self) -> None:

        # ==================================================
        # ENV
        # ==================================================
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
        self.groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "").strip()

        self.deepseek_model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        self.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.openrouter_model = os.getenv(
            "OPENROUTER_MODEL",
            "openai/gpt-4o-mini"
        )

        # ==================================================
        # CORE
        # ==================================================
        self.prompt_engine = PromptEngine()
        self.memory_engine = MemoryEngine()
        self.context_manager = ContextManager(self.memory_engine)
        self.decision_engine = DecisionEngine(self)

        # ==================================================
        # CLIENTS
        # ==================================================
        self.deepseek_client = self._create_deepseek_client()
        self.groq_client = self._create_groq_client()
        self.openrouter_client = self._create_openrouter_client()

        # ==================================================
        # STATE
        # ==================================================
        self.last_provider = "offline"
        self.last_latency = 0.0
        self.last_error = None

        self.lock = threading.Lock()

    # ==================================================
    # CLIENT BUILDERS
    # ==================================================
    def _create_deepseek_client(self):
        if not self.deepseek_api_key:
            return None
        try:
            return OpenAI(
                api_key=self.deepseek_api_key,
                base_url="https://api.deepseek.com"
            )
        except:
            return None

    def _create_groq_client(self):
        if not self.groq_api_key:
            return None
        try:
            return Groq(api_key=self.groq_api_key)
        except:
            return None

    def _create_openrouter_client(self):
        if not self.openrouter_api_key:
            return None
        try:
            return OpenAI(
                api_key=self.openrouter_api_key,
                base_url="https://openrouter.ai/api/v1"
            )
        except:
            return None

    # ==================================================
    # MAIN ENGINE
    # ==================================================
    def generate_response(
        self,
        user_input: str,
        session_id: str = "default_user"
    ) -> str:

        if not user_input or not user_input.strip():
            return "⚠️ Input missing."

        user_input = user_input.strip()

        # 1. Intent detection
        decision = self.detect_intent(user_input)

        # 2. Action Mode
        if decision.get("intent") != "chat":
            reply = self._handle_action(decision)
            self._save_chat(session_id, user_input, reply)
            return reply

        # 3. Chat Mode
        context = self._safe_get_context(session_id)
        memory = self._load_memory_snippet()

        prompt = self._build_prompt_safe(
            user_input=user_input,
            context=context,
            memory=memory
        )

        reply = self._run_ai_pipeline(prompt)

        self._save_chat(session_id, user_input, reply)

        return reply

    # ==================================================
    # PROMPT OPTIMIZER
    # ==================================================
    def _build_prompt_safe(
        self,
        user_input: str,
        context: str,
        memory: str
    ) -> str:

        # reduce token traffic
        context = context[-1200:] if context else ""
        memory = memory[:500] if memory else ""

        try:
            return self.prompt_engine.build_chat_prompt(
                user_input=user_input,
                context=f"{context}\n{memory}".strip()
            )
        except:
            return user_input

    # ==================================================
    # INTENT
    # ==================================================
    def detect_intent(self, user_input: str) -> Dict[str, Any]:
        try:
            result = self.decision_engine.analyze(user_input)

            if isinstance(result, dict):
                return result

            return {"intent": "chat"}

        except:
            return {"intent": "chat"}

    # ==================================================
    # ACTION ENGINE
    # ==================================================
    def _handle_action(self, decision: Dict[str, Any]) -> str:

        intent = decision.get("intent", "")
        target = decision.get("target", "").lower()

        try:
            if intent == "open_app":

                if "chrome" in target:
                    webbrowser.open("https://google.com")

                elif "youtube" in target:
                    webbrowser.open("https://youtube.com")

                elif "code" in target or "vs code" in target:
                    subprocess.Popen(["code"], shell=True)

                elif "notepad" in target:
                    subprocess.Popen(["notepad.exe"])

                return f"🚀 Opening {target}"

            elif intent == "search_web":

                webbrowser.open(
                    f"https://www.google.com/search?q={target}"
                )

                return f"🔎 Searching {target}"

            elif intent == "system_action":

                action = decision.get("action", "").lower()

                if "shutdown" in action:
                    return "⚙️ Shutdown blocked for safety."

                if "restart" in action:
                    return "⚙️ Restart blocked for safety."

                return f"⚙️ Task executed: {action}"

        except Exception as e:
            return f"❌ Action failed: {str(e)}"

        return "⚡ Command processed."

    # ==================================================
    # AI PIPELINE
    # ==================================================
    def _run_ai_pipeline(self, prompt: str) -> str:

        # fastest first = reduce wait
        providers = [
            ("groq", self._groq_call),
            ("deepseek", self._deepseek_call),
            ("openrouter", self._openrouter_call),
        ]

        for name, func in providers:

            try:
                start = time.time()

                result = func(prompt)

                if result and result.strip():

                    latency = round(time.time() - start, 3)

                    with self.lock:
                        self.last_provider = name
                        self.last_latency = latency
                        self.last_error = None

                    return result.strip()

            except Exception as e:

                with self.lock:
                    self.last_error = f"{name}: {str(e)}"

                continue

        with self.lock:
            self.last_provider = "offline"

        return "আমি এখন offline mode এ আছি 🚀"

    # ==================================================
    # PROVIDERS
    # ==================================================
    def _groq_call(self, prompt: str) -> Optional[str]:

        if not self.groq_client:
            return None

        res = self.groq_client.chat.completions.create(
            model=self.groq_model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=250
        )

        return res.choices[0].message.content

    def _deepseek_call(self, prompt: str) -> Optional[str]:

        if not self.deepseek_client:
            return None

        res = self.deepseek_client.chat.completions.create(
            model=self.deepseek_model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=250
        )

        return res.choices[0].message.content

    def _openrouter_call(self, prompt: str) -> Optional[str]:

        if not self.openrouter_client:
            return None

        res = self.openrouter_client.chat.completions.create(
            model=self.openrouter_model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=220
        )

        return res.choices[0].message.content

    # ==================================================
    # CONTEXT
    # ==================================================
    def _safe_get_context(self, session_id: str) -> str:
        try:
            return self.context_manager.get_context_text(session_id)
        except:
            return ""

    def _save_chat(
        self,
        session_id: str,
        user: str,
        bot: str
    ):
        try:
            self.context_manager.add_user_message(session_id, user)
            self.context_manager.add_assistant_message(session_id, bot)
        except:
            pass

    def _load_memory_snippet(self) -> str:
        try:
            memories = self.memory_engine.get_all_memories()

            if not memories:
                return ""

            rows = []

            for m in memories[:5]:
                key = m.get("key_name", "")
                val = m.get("value", "")
                rows.append(f"{key}: {val}")

            return "\n".join(rows)

        except:
            return ""

    # ==================================================
    # STATUS
    # ==================================================
    def get_status(self):

        with self.lock:
            return {
                "provider": self.last_provider,
                "latency": self.last_latency,
                "error": self.last_error
            }