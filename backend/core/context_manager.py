from __future__ import annotations

from collections import deque
from datetime import datetime
from threading import RLock
from typing import Any, Deque, Dict, List, Optional
import re


class ContextManager:
    """
    LIAO AI Context Manager (Ultra Jarvis Layer)

    Responsibilities:
    - Manage chat sessions
    - Build intelligent context
    - Detect emotion + intent hints
    - Optimize LLM context quality
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
        self._lock = RLock()

    # ==================================================
    # SESSION MANAGEMENT
    # ==================================================
    def create_session(self, session_id: str) -> None:
        if not session_id:
            return

        with self._lock:
            if session_id not in self._sessions:
                self._cleanup()
                self._sessions[session_id] = deque(
                    maxlen=self.max_messages_per_session
                )

    def clear_session(self, session_id: str) -> bool:
        with self._lock:
            return self._sessions.pop(session_id, None) is not None

    # ==================================================
    # MESSAGE ADD
    # ==================================================
    def add_user_message(self, session_id: str, message: str):
        self._add(session_id, "user", message)

    def add_assistant_message(self, session_id: str, message: str):
        self._add(session_id, "assistant", message)

    # ==================================================
    # 🧠 CONTEXT BUILDER (SMART)
    # ==================================================
    def get_context_text(self, session_id: str, limit: int = 12) -> str:
        messages = self._sessions.get(session_id, [])

        if not messages:
            return ""

        recent = list(messages)[-limit:]

        optimized = []

        for m in recent:
            role = m["role"].upper()
            content = self._clean_text(m["content"])

            if not content:
                continue

            optimized.append(f"{role}: {content}")

        return "\n".join(optimized)

    # ==================================================
    # 🔥 ADVANCED CONTEXT (WITH EMOTION TAG)
    # ==================================================
    def get_enriched_context(self, session_id: str, limit: int = 10) -> str:
        messages = self._sessions.get(session_id, [])

        if not messages:
            return ""

        recent = list(messages)[-limit:]

        enriched = []

        for m in recent:
            emotion = self._detect_emotion(m["content"])
            role = m["role"].upper()

            enriched.append(
                f"{role} ({emotion}): {self._clean_text(m['content'])}"
            )

        return "\n".join(enriched)

    # ==================================================
    # EMOTION DETECTION (LIGHTWEIGHT)
    # ==================================================
    def _detect_emotion(self, text: str) -> str:
        text = text.lower()

        if any(w in text for w in ["sad", "depressed", "unhappy", "খারাপ"]):
            return "sad"

        if any(w in text for w in ["angry", "mad", "রাগ"]):
            return "angry"

        if any(w in text for w in ["confused", "don't understand", "বুঝি না"]):
            return "confused"

        if any(w in text for w in ["happy", "great", "good", "ভালো"]):
            return "happy"

        return "neutral"

    # ==================================================
    # TEXT CLEANING (IMPORTANT)
    # ==================================================
    def _clean_text(self, text: str) -> str:
        text = text.strip()

        # remove extra spaces
        text = re.sub(r"\s+", " ", text)

        # remove repeated messages
        if len(text) < 2:
            return ""

        return text

    # ==================================================
    # MEMORY HOOK (CLEAN)
    # ==================================================
    def save_fact(self, category: str, key: str, value: str) -> bool:
        if not self.memory_engine:
            return False

        try:
            return self.memory_engine.save_memory(category, key, value)
        except:
            return False

    def load_fact(self, category: str, key: str) -> Optional[str]:
        if not self.memory_engine:
            return None

        try:
            return self.memory_engine.get_memory(category, key)
        except:
            return None

    # ==================================================
    # INTERNAL ADD
    # ==================================================
    def _add(self, session_id: str, role: str, content: str):
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

    def _cleanup(self):
        while len(self._sessions) >= self.max_sessions:
            self._sessions.pop(next(iter(self._sessions)))