from __future__ import annotations

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
    🚀 LIAO / JARVIS CORE v9.0 (ULTRA EDITION)

    Features:
    - Smart provider routing
    - Retry + fallback
    - Optimized token usage
    - Action-safe execution
    - Memory-aware prompts
    - Thread-safe status tracking
    """

    def __init__(self) -> None:

        # =========================
        # ENV
        # =========================
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
        self.groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "").strip()

        self.deepseek_model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        self.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.openrouter_model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

        # =========================
        # CORE
        # =========================
        self.prompt_engine = PromptEngine()
        self.memory_engine = MemoryEngine()
        self.context_manager = ContextManager(self.memory_engine)
        self.decision_engine = DecisionEngine(self)

        # =========================
        # CLIENTS
        # =========================
        self.deepseek_client = self._safe_create(lambda: OpenAI(
            api_key=self.deepseek_api_key,
            base_url="https://api.deepseek.com"
        ))

        self.groq_client = self._safe_create(lambda: Groq(api_key=self.groq_api_key))

        self.openrouter_client = self._safe_create(lambda: OpenAI(
            api_key=self.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1"
        ))

        # =========================
        # STATE
        # =========================
        self.last_provider = "offline"
        self.last_latency = 0.0
        self.last_error = None

        self.lock = threading.RLock()

    # ==================================================
    # SAFE CREATOR
    # ==================================================
    def _safe_create(self, fn: Callable):
        try:
            return fn()
        except:
            return None

    # ==================================================
    # MAIN RESPONSE
    # ==================================================
    def generate_response(self, user_input: str, session_id: str = "default") -> str:

        if not user_input or not user_input.strip():
            return "⚠️ Empty input."

        user_input = user_input.strip()

        decision = self.detect_intent(user_input)

        # ACTION MODE
        if decision.get("intent") != "chat":
            reply = self._handle_action(decision)
            self._save_chat(session_id, user_input, reply)
            return reply

        # CHAT MODE
        context = self._safe_context(session_id)
        memory = self._safe_memory()

        prompt = self._build_prompt(user_input, context, memory)

        reply = self._run_pipeline(prompt)

        self._save_chat(session_id, user_input, reply)

        return reply

    # ==================================================
    # PROMPT BUILDER
    # ==================================================
    def _build_prompt(self, user_input: str, context: str, memory: str) -> str:

        context = context[-1000:] if context else ""
        memory = memory[:400] if memory else ""

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
            return self.decision_engine.analyze(user_input)
        except:
            return {"intent": "chat"}

    # ==================================================
    # ACTION HANDLER (SAFE)
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

                elif "code" in target:
                    subprocess.Popen(["code"], shell=True)

                return f"🚀 Opening {target}"

            elif intent == "search_web":
                webbrowser.open(f"https://www.google.com/search?q={target}")
                return f"🔎 Searching {target}"

            elif intent == "system_action":
                return "⚙️ Restricted system command."

        except Exception as e:
            return f"❌ Action error: {str(e)}"

        return "⚡ Done."

    # ==================================================
    # AI PIPELINE (SMART ROUTING)
    # ==================================================
    def _run_pipeline(self, prompt: str) -> str:

        providers = [
            ("groq", self._groq_call),
            ("deepseek", self._deepseek_call),
            ("openrouter", self._openrouter_call),
        ]

        for name, fn in providers:

            result = self._safe_call(name, fn, prompt)

            if result:
                return result

        return "আমি এখন offline mode এ আছি 🚀"

    def _safe_call(self, name: str, fn: Callable, prompt: str) -> Optional[str]:

        try:
            start = time.time()

            result = fn(prompt)

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

        return None

    # ==================================================
    # PROVIDERS
    # ==================================================
    def _groq_call(self, prompt: str) -> Optional[str]:

        if not self.groq_client:
            return None

        res = self.groq_client.chat.completions.create(
            model=self.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=220
        )

        return res.choices[0].message.content

    def _deepseek_call(self, prompt: str) -> Optional[str]:

        if not self.deepseek_client:
            return None

        res = self.deepseek_client.chat.completions.create(
            model=self.deepseek_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=220
        )

        return res.choices[0].message.content

    def _openrouter_call(self, prompt: str) -> Optional[str]:

        if not self.openrouter_client:
            return None

        res = self.openrouter_client.chat.completions.create(
            model=self.openrouter_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )

        return res.choices[0].message.content

    # ==================================================
    # CONTEXT + MEMORY
    # ==================================================
    def _safe_context(self, session_id: str) -> str:
        try:
            return self.context_manager.get_context_text(session_id)
        except:
            return ""

    def _safe_memory(self) -> str:
        try:
            data = self.memory_engine.get_all_memories()[:5]
            return "\n".join(f"{d['key_name']}: {d['value']}" for d in data)
        except:
            return ""

    def _save_chat(self, session_id: str, user: str, bot: str):
        try:
            self.context_manager.add_user_message(session_id, user)
            self.context_manager.add_assistant_message(session_id, bot)
        except:
            pass

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