from __future__ import annotations

from collections import deque
from datetime import datetime
from threading import Lock
from typing import Any, Deque, Dict, List, Optional


class ContextManager:
    """
    Conversation context manager.

    Responsibilities:
    - maintain short-term chat history
    - provide formatted context for AI providers
    - optional long-term memory integration
    - thread-safe session handling
    """

    def __init__(
        self,
        memory_engine: Optional[object] = None,
        max_sessions: int = 100,
        max_messages_per_session: int = 20,
    ) -> None:
        self.memory_engine = memory_engine
        self.max_sessions = max_sessions
        self.max_messages_per_session = max_messages_per_session

        self._sessions: Dict[str, Deque[Dict[str, Any]]] = {}
        self._lock = Lock()

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------
    def create_session(self, session_id: str) -> None:
        """
        Create a new session if not exists.
        """
        with self._lock:
            if session_id not in self._sessions:
                self._cleanup_if_needed()

                self._sessions[session_id] = deque(
                    maxlen=self.max_messages_per_session
                )

    def add_user_message(
        self,
        session_id: str,
        message: str,
    ) -> None:
        self._add_message(
            session_id=session_id,
            role="user",
            content=message,
        )

    def add_assistant_message(
        self,
        session_id: str,
        message: str,
    ) -> None:
        self._add_message(
            session_id=session_id,
            role="assistant",
            content=message,
        )

    def get_messages(
        self,
        session_id: str,
    ) -> List[Dict[str, Any]]:
        """
        Return raw message list.
        """
        with self._lock:
            if session_id not in self._sessions:
                return []

            return list(self._sessions[session_id])

    def get_context_text(
        self,
        session_id: str,
        limit: int = 10,
    ) -> str:
        """
        Return formatted plain-text context for AI prompt.
        """
        messages = self.get_messages(session_id)

        if not messages:
            return ""

        selected = messages[-limit:]
        lines: List[str] = []

        for item in selected:
            role = item["role"].capitalize()
            content = item["content"].strip()
            lines.append(f"{role}: {content}")

        return "\n".join(lines)

    def clear_session(
        self,
        session_id: str,
    ) -> bool:
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                return True

        return False

    def session_exists(
        self,
        session_id: str,
    ) -> bool:
        with self._lock:
            return session_id in self._sessions

    def total_sessions(self) -> int:
        with self._lock:
            return len(self._sessions)

    def export_session(
        self,
        session_id: str,
    ) -> Dict[str, Any]:
        """
        Export full session data.
        """
        return {
            "session_id": session_id,
            "messages": self.get_messages(session_id),
            "count": len(self.get_messages(session_id)),
        }

    # --------------------------------------------------
    # Long-term memory helpers
    # --------------------------------------------------
    def save_fact(
        self,
        user_id: str,
        key: str,
        value: str,
    ) -> bool:
        """
        Save memory if memory engine exists.
        """
        if not self.memory_engine:
            return False

        try:
            if hasattr(self.memory_engine, "save"):
                self.memory_engine.save(user_id, key, value)
                return True

            if hasattr(self.memory_engine, "remember"):
                self.memory_engine.remember(user_id, key, value)
                return True

        except Exception:
            return False

        return False

    def load_fact(
        self,
        user_id: str,
        key: str,
    ) -> Optional[str]:
        """
        Load memory if memory engine exists.
        """
        if not self.memory_engine:
            return None

        try:
            if hasattr(self.memory_engine, "get"):
                return self.memory_engine.get(user_id, key)

            if hasattr(self.memory_engine, "recall"):
                return self.memory_engine.recall(user_id, key)

        except Exception:
            return None

        return None

    # --------------------------------------------------
    # Internal Methods
    # --------------------------------------------------
    def _add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:
        content = content.strip()

        if not content:
            return

        with self._lock:
            if session_id not in self._sessions:
                self.create_session(session_id)

            self._sessions[session_id].append(
                {
                    "role": role,
                    "content": content,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )

    def _cleanup_if_needed(self) -> None:
        """
        Remove oldest sessions when limit reached.
        """
        while len(self._sessions) >= self.max_sessions:
            oldest_key = next(iter(self._sessions))
            del self._sessions[oldest_key]


# ------------------------------------------------------
# Local Test
# ------------------------------------------------------
if __name__ == "__main__":
    manager = ContextManager()

    manager.create_session("user_1")

    manager.add_user_message("user_1", "Hello")
    manager.add_assistant_message("user_1", "Hi, how can I help?")
    manager.add_user_message("user_1", "What is Python?")

    print(manager.get_context_text("user_1"))