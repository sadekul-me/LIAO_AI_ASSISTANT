import os
import time
from datetime import datetime
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from google import genai
from groq import Groq
from openai import OpenAI

from backend.core.prompt_engine import PromptEngine
from backend.core.context_manager import ContextManager
from backend.core.memory_engine import MemoryEngine
from backend.core.decision_engine import DecisionEngine

load_dotenv()


class AIEngine:
    """
    🔥 NILIMA / JARVIS CORE v4.1 (ULTRA STABLE)

    Features:
    - Context + Memory fusion brain
    - Safe failover AI pipeline
    - Decision engine protected
    - Production safe response system
    """

    def __init__(self) -> None:

        # =========================
        # ENV
        # =========================
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "").strip()

        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        self.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.openrouter_model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

        # =========================
        # CORE MODULES
        # =========================
        self.prompt_engine = PromptEngine()
        self.memory_engine = MemoryEngine()
        self.context_manager = ContextManager(self.memory_engine)
        self.decision_engine = DecisionEngine(self)

        # =========================
        # CLIENTS
        # =========================
        self.gemini_client = self._create_gemini_client()
        self.groq_client = self._create_groq_client()
        self.openrouter_client = self._create_openrouter_client()

        # =========================
        # STATE
        # =========================
        self.last_provider = "offline"
        self.last_latency = 0.0

    # ==================================================
    # CLIENT INIT
    # ==================================================
    def _create_gemini_client(self):
        if not self.gemini_api_key:
            return None
        try:
            return genai.Client(api_key=self.gemini_api_key)
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
                base_url="https://openrouter.ai/api/v1",
                api_key=self.openrouter_api_key
            )
        except:
            return None

    # ==================================================
    # MAIN BRAIN
    # ==================================================
    def generate_response(
        self,
        user_input: str,
        session_id: str = "default_user"
    ) -> str:

        if not user_input:
            return "⚠️ Empty input received"

        # 🧠 CONTEXT
        context = self.context_manager.get_context_text(session_id)

        # 🧠 MEMORY
        memory = self._load_memory_snippet()

        # ⚙️ DECISION ENGINE (SAFE)
        try:
            decision = self.decision_engine.analyze(user_input)
        except:
            decision = {"intent": "chat"}

        # =========================
        # ACTION MODE
        # =========================
        if decision.get("intent") != "chat":
            response = self._handle_action(decision)

            self._save_chat(session_id, user_input, response)
            return response

        # =========================
        # CHAT MODE
        # =========================
        prompt = self.prompt_engine.build_chat_prompt(
            user_input=user_input,
            context=f"{context}\n{memory}".strip()
        )

        response = self._run_ai_pipeline(prompt)

        self._save_chat(session_id, user_input, response)

        return response

    # ==================================================
    # SAFE CHAT SAVE
    # ==================================================
    def _save_chat(self, session_id: str, user: str, bot: str):
        try:
            self.context_manager.add_user_message(session_id, user)
            self.context_manager.add_assistant_message(session_id, bot)
        except:
            pass

    # ==================================================
    # ACTION HANDLER
    # ==================================================
    def _handle_action(self, decision: Dict[str, Any]) -> str:
        intent = decision.get("intent", "")

        if intent == "open_app":
            return f"🚀 Opening {decision.get('target', 'unknown')}..."

        if intent == "search_web":
            return f"🔎 Searching: {decision.get('target', '')}"

        if intent == "system_action":
            return f"⚙️ Executing: {decision.get('action', '')}"

        if intent == "create_file":
            return "📁 File system ready..."

        return "⚡ Action detected but not executed"

    # ==================================================
    # AI PIPELINE
    # ==================================================
    def _run_ai_pipeline(self, prompt: str) -> str:

        providers = [
            ("gemini", self._gemini_call),
            ("groq", self._groq_call),
            ("openrouter", self._openrouter_call),
        ]

        for name, func in providers:
            try:
                start = time.time()
                result = func(prompt)
                self.last_latency = round(time.time() - start, 3)

                if result:
                    self.last_provider = name
                    return result

            except:
                continue

        self.last_provider = "offline"
        return "আমি এখন offline mode এ আছি 🚀"

    # ==================================================
    # MEMORY SNIPPET
    # ==================================================
    def _load_memory_snippet(self) -> str:
        try:
            memories = self.memory_engine.get_all_memories()
            if not memories:
                return ""

            return "\n".join(
                f"{m.get('category','')}: {m.get('key_name','')} = {m.get('value','')}"
                for m in memories[:5]
            )
        except:
            return ""

    # ==================================================
    # PROVIDERS
    # ==================================================
    def _gemini_call(self, prompt: str) -> Optional[str]:
        if not self.gemini_client:
            return None

        res = self.gemini_client.models.generate_content(
            model=self.gemini_model,
            contents=prompt
        )

        return getattr(res, "text", "").strip() or None

    def _groq_call(self, prompt: str) -> Optional[str]:
        if not self.groq_client:
            return None

        res = self.groq_client.chat.completions.create(
            model=self.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return res.choices[0].message.content.strip() or None

    def _openrouter_call(self, prompt: str) -> Optional[str]:
        if not self.openrouter_client:
            return None

        res = self.openrouter_client.chat.completions.create(
            model=self.openrouter_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return res.choices[0].message.content.strip() or None

    # ==================================================
    # STATUS
    # ==================================================
    def get_status(self):
        return {
            "provider": self.last_provider,
            "latency": self.last_latency
        }