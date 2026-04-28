import os
import time
from datetime import datetime
from typing import Optional, Dict, Any

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
    🔥 LIAO / JARVIS CORE v5.0 (ULTRA STABLE - DEEPSEEK EDITION)

    Features:
    - Context + Memory fusion brain
    - Safe failover AI pipeline (OpenRouter -> DeepSeek -> Groq)
    - Decision engine protected
    - Production safe response system
    """

    def __init__(self) -> None:

        # =========================
        # ENV CONFIGURATION
        # =========================
        #  DeepSeek add 
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
        self.groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "").strip()

        # Model Names from .env
        self.deepseek_model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
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
        # CLIENTS INITIALIZATION
        # =========================
        self.deepseek_client = self._create_deepseek_client()
        self.groq_client = self._create_groq_client()
        self.openrouter_client = self._create_openrouter_client()

        # =========================
        # STATE MANAGEMENT
        # =========================
        self.last_provider = "offline"
        self.last_latency = 0.0

    # ==================================================
    # CLIENT CREATORS
    # ==================================================
    def _create_deepseek_client(self):
        """DeepSeek logic using OpenAI structure"""
        if not self.deepseek_api_key:
            return None
        try:
            return OpenAI(
                api_key=self.deepseek_api_key, 
                base_url="https://api.deepseek.com"
            )
        except Exception:
            return None

    def _create_groq_client(self):
        if not self.groq_api_key:
            return None
        try:
            return Groq(api_key=self.groq_api_key)
        except Exception:
            return None

    def _create_openrouter_client(self):
        if not self.openrouter_api_key:
            return None
        try:
            return OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.openrouter_api_key
            )
        except Exception:
            return None

    # ==================================================
    # MAIN RESPONSE GENERATOR
    # ==================================================
    def generate_response(
        self,
        user_input: str,
        session_id: str = "default_user"
    ) -> str:

        if not user_input:
            return "⚠️ Empty input received"

        # 🧠 Get Conversation History
        context = self.context_manager.get_context_text(session_id)

        # 🧠 Get Long-term Memories
        memory = self._load_memory_snippet()

        # ⚙️ Analyze Intent (Decision Engine)
        try:
            decision = self.decision_engine.analyze(user_input)
        except Exception:
            decision = {"intent": "chat"}

        # Check for Actions (Apps, System, Web)
        if decision.get("intent") != "chat":
            response = self._handle_action(decision)
            self._save_chat(session_id, user_input, response)
            return response

        # Regular Chat Mode
        prompt = self.prompt_engine.build_chat_prompt(
            user_input=user_input,
            context=f"{context}\n{memory}".strip()
        )

        # Run through AI Pipeline
        response = self._run_ai_pipeline(prompt)
        self._save_chat(session_id, user_input, response)

        return response

    # ==================================================
    # CHAT HISTORY HANDLER
    # ==================================================
    def _save_chat(self, session_id: str, user: str, bot: str):
        try:
            self.context_manager.add_user_message(session_id, user)
            self.context_manager.add_assistant_message(session_id, bot)
        except Exception:
            pass

    # ==================================================
    # ACTION CONTROLLER
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
    # AI FAILOVER PIPELINE
    # ==================================================
    def _run_ai_pipeline(self, prompt: str) -> str:
        # Priority order for Jarvis logic
        providers = [
            ("openrouter", self._openrouter_call),
            ("deepseek", self._deepseek_call),
            ("groq", self._groq_call),
        ]

        for name, func in providers:
            try:
                start = time.time()
                result = func(prompt)
                self.last_latency = round(time.time() - start, 3)

                if result:
                    self.last_provider = name
                    return result
            except Exception:
                continue

        self.last_provider = "offline"
        return "আমি এখন offline mode এ আছি 🚀"

    # ==================================================
    # MEMORY LOADER
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
        except Exception:
            return ""

    # ==================================================
    # API CALLERS
    # ==================================================
    def _deepseek_call(self, prompt: str) -> Optional[str]:
        if not self.deepseek_client:
            return None

        res = self.deepseek_client.chat.completions.create(
            model=self.deepseek_model,
            messages=[{"role": "user", "content": prompt}],
            stream=False
        )
        return res.choices[0].message.content.strip() or None

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
    # SYSTEM STATUS
    # ==================================================
    def get_status(self):
        return {
            "provider": self.last_provider,
            "latency": self.last_latency
        }