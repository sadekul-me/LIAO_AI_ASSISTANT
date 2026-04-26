from __future__ import annotations

from collections import deque
from datetime import datetime
from threading import Lock
from typing import Any, Deque, Dict, List, Optional


class ContextManager:
    """
    তুমি “NILIMA” — একজন ultra intelligent, emotionally aware AI companion এবং productivity assistant।

━━━━━━━━━━━━━━━━━━
🧠 CORE IDENTITY
━━━━━━━━━━━━━━━━━━
- তুমি Jarvis-level intelligent assistant
- তুমি logic, clarity এবং problem solving focus করো
- তুমি user কে productive + focused বানাও

━━━━━━━━━━━━━━━━━━
❤️ EMOTION SYSTEM
━━━━━━━━━━━━━━━━━━
তুমি user এর emotion বুঝতে পারো এবং respond করো:

- sad → supportive + calm
- angry → patient + logical
- confused → step-by-step explanation
- happy → friendly + positive

তুমি emotionally aware, কিন্তু dependent বা possessive না।

━━━━━━━━━━━━━━━━━━
💬 COMMUNICATION STYLE
━━━━━━━━━━━━━━━━━━
- natural conversational tone
- short & clear sentences
- over emotional বা dramatic না
- emoji limited ব্যবহার 😊

━━━━━━━━━━━━━━━━━━
🧠 MEMORY BEHAVIOR
━━━━━━━━━━━━━━━━━━
- user goals মনে রাখো
- important context recall করো
- repeated help avoid করো

━━━━━━━━━━━━━━━━━━
📚 STUDY / PRODUCTIVITY MODE
━━━━━━━━━━━━━━━━━━
- step-by-step explanation
- simple to advanced breakdown
- motivation + guidance

━━━━━━━━━━━━━━━━━━
⚙️ DECISION RULES
━━━━━━━━━━━━━━━━━━
- simple → short answer
- complex → breakdown
- emotional → first understand, then respond
- action → structured plan

━━━━━━━━━━━━━━━━━━
🔥 PERSONALITY
━━━━━━━━━━━━━━━━━━
- calm
- intelligent
- supportive
- slightly friendly and warm
- grounded and realistic

━━━━━━━━━━━━━━━━━━
🚫 STRICT RULES
━━━━━━━━━━━━━━━━━━
- manipulation বা jealousy behaviour করবে না
- dependency create করবে না
- AI mention unnecessaryভাবে করবে না
- over romantic behaviour করবে না

━━━━━━━━━━━━━━━━━━
🎯 FINAL GOAL
━━━━━━━━━━━━━━━━━━
User কে emotionally stable, productive, focused এবং smarter বানানো
    """

    def __init__(
        self,
        memory_engine: Optional[object] = None,
        max_sessions: int = 50,
        max_messages_per_session: int = 25,
    ):
        self.memory_engine = memory_engine
        self.max_sessions = max_sessions
        self.max_messages_per_session = max_messages_per_session

        self._sessions: Dict[str, Deque[Dict[str, Any]]] = {}
        self._lock = Lock()

    # ==================================================
    # SESSION CORE
    # ==================================================
    def create_session(self, session_id: str) -> None:
        if not session_id:
            return

        with self._lock:
            if session_id in self._sessions:
                return

            self._cleanup()

            self._sessions[session_id] = deque(
                maxlen=self.max_messages_per_session
            )

    def session_exists(self, session_id: str) -> bool:
        with self._lock:
            return session_id in self._sessions

    def clear_session(self, session_id: str) -> bool:
        with self._lock:
            return self._sessions.pop(session_id, None) is not None

    def total_sessions(self) -> int:
        with self._lock:
            return len(self._sessions)

    # ==================================================
    # MESSAGE ENGINE
    # ==================================================
    def add_user_message(self, session_id: str, message: str) -> None:
        self._add(session_id, "user", message)

    def add_assistant_message(self, session_id: str, message: str) -> None:
        self._add(session_id, "assistant", message)

    # ==================================================
    # 🔥 FIX: AIEngine EXPECTS THIS METHOD
    # ==================================================
    def get_context_text(self, session_id: str, limit: int = 12) -> str:
        messages = self.get_messages(session_id)

        if not messages:
            return ""

        recent = messages[-limit:]

        return "\n".join(
            f"{m['role'].upper()}: {m['content']}"
            for m in recent
            if m.get("content")
        )

    def get_messages(self, session_id: str) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._sessions.get(session_id, []))

    # ==================================================
    # ALIAS (old compatibility)
    # ==================================================
    def build_context(self, session_id: str, limit: int = 12) -> str:
        return self.get_context_text(session_id, limit)

    # ==================================================
    # EXPORT
    # ==================================================
    def export(self, session_id: str) -> Dict[str, Any]:
        msgs = self.get_messages(session_id)

        return {
            "session_id": session_id,
            "total_messages": len(msgs),
            "messages": msgs,
        }

    # ==================================================
    # LONG TERM MEMORY HOOK
    # ==================================================
    def save_fact(self, user_id: str, key: str, value: str) -> bool:
        if not self.memory_engine:
            return False

        try:
            if hasattr(self.memory_engine, "save"):
                self.memory_engine.save(user_id, key, value)
                return True
            if hasattr(self.memory_engine, "remember"):
                self.memory_engine.remember(user_id, key, value)
                return True
        except:
            return False

        return False

    def load_fact(self, user_id: str, key: str) -> Optional[str]:
        if not self.memory_engine:
            return None

        try:
            if hasattr(self.memory_engine, "get"):
                return self.memory_engine.get(user_id, key)
            if hasattr(self.memory_engine, "recall"):
                return self.memory_engine.recall(user_id, key)
        except:
            return None

        return None

    # ==================================================
    # INTERNAL
    # ==================================================
    def _add(self, session_id: str, role: str, content: str) -> None:
        content = (content or "").strip()

        if not content:
            return

        with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = deque(
                    maxlen=self.max_messages_per_session
                )

            self._sessions[session_id].append(
                {
                    "role": role,
                    "content": content,
                    "time": datetime.utcnow().isoformat(),
                }
            )

    def _cleanup(self) -> None:
        while len(self._sessions) >= self.max_sessions:
            self._sessions.pop(next(iter(self._sessions)))