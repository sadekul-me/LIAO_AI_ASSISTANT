from __future__ import annotations

import sqlite3
from pathlib import Path
from datetime import datetime
from threading import RLock
from typing import List, Dict, Optional


class MemoryEngine:
    """
    LIAO AI Memory Engine (Production Grade)

    Features:
    - Persistent storage (SQLite, WAL mode)
    - Thread-safe (RLock)
    - Conversation history
    - Key-value memory system
    - Optimized read/write
    - Future-proof hooks
    """

    def __init__(self, db_path: str = "data/memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.lock = RLock()
        self.connection = self._connect()

        self._setup()

    # =========================================================
    # 🔌 CONNECTION
    # =========================================================
    def _connect(self):
        conn = sqlite3.connect(
            self.db_path,
            check_same_thread=False,
            timeout=30,
        )
        conn.row_factory = sqlite3.Row

        # 🔥 Performance boost
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")

        return conn

    def _setup(self):
        queries = [
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                key_name TEXT NOT NULL,
                value TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(category, key_name)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """,
            "CREATE INDEX IF NOT EXISTS idx_mem_cat_key ON memories(category, key_name)",
            "CREATE INDEX IF NOT EXISTS idx_conv_time ON conversations(created_at)"
        ]

        with self.lock:
            cursor = self.connection.cursor()
            for q in queries:
                cursor.execute(q)
            self.connection.commit()

    # =========================================================
    # 🕒 TIME
    # =========================================================
    def _now(self) -> str:
        return datetime.utcnow().isoformat()

    # =========================================================
    # 🧠 MEMORY (KEY-VALUE)
    # =========================================================
    def save_memory(self, category: str, key_name: str, value: str) -> bool:
        try:
            with self.lock:
                self.connection.execute(
                    """
                    INSERT INTO memories (category, key_name, value, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(category, key_name)
                    DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at
                    """,
                    (category, key_name, value, self._now(), self._now())
                )
                self.connection.commit()
            return True
        except sqlite3.Error as e:
            print("Memory save error:", e)
            return False

    def get_memory(self, category: str, key_name: str) -> Optional[str]:
        try:
            with self.lock:
                cur = self.connection.execute(
                    "SELECT value FROM memories WHERE category=? AND key_name=? LIMIT 1",
                    (category, key_name)
                )
                row = cur.fetchone()
                return row["value"] if row else None
        except sqlite3.Error as e:
            print("Memory fetch error:", e)
            return None

    def delete_memory(self, category: str, key_name: str) -> bool:
        try:
            with self.lock:
                self.connection.execute(
                    "DELETE FROM memories WHERE category=? AND key_name=?",
                    (category, key_name)
                )
                self.connection.commit()
            return True
        except sqlite3.Error as e:
            print("Memory delete error:", e)
            return False

    def get_all_memories(self, category: Optional[str] = None) -> List[Dict]:
        try:
            with self.lock:
                if category:
                    cur = self.connection.execute(
                        "SELECT * FROM memories WHERE category=? ORDER BY updated_at DESC",
                        (category,)
                    )
                else:
                    cur = self.connection.execute(
                        "SELECT * FROM memories ORDER BY updated_at DESC"
                    )

                return [dict(r) for r in cur.fetchall()]
        except sqlite3.Error as e:
            print("Memory list error:", e)
            return []

    # =========================================================
    # 💬 CONVERSATIONS
    # =========================================================
    def save_conversation(self, role: str, message: str) -> bool:
        try:
            with self.lock:
                self.connection.execute(
                    "INSERT INTO conversations (role, message, created_at) VALUES (?, ?, ?)",
                    (role, message, self._now())
                )
                self.connection.commit()
            return True
        except sqlite3.Error as e:
            print("Conversation save error:", e)
            return False

    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        try:
            with self.lock:
                cur = self.connection.execute(
                    """
                    SELECT role, message, created_at
                    FROM conversations
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (limit,)
                )
                rows = [dict(r) for r in cur.fetchall()]
                return list(reversed(rows))
        except sqlite3.Error as e:
            print("Conversation fetch error:", e)
            return []

    def clear_conversations(self) -> bool:
        try:
            with self.lock:
                self.connection.execute("DELETE FROM conversations")
                self.connection.commit()
            return True
        except sqlite3.Error as e:
            print("Conversation clear error:", e)
            return False

    # =========================================================
    # 🧠 ADVANCED (FUTURE READY)
    # =========================================================
    def prune_old_conversations(self, keep_last: int = 100):
        """Keep last N messages, delete older ones"""
        try:
            with self.lock:
                self.connection.execute(
                    """
                    DELETE FROM conversations
                    WHERE id NOT IN (
                        SELECT id FROM conversations
                        ORDER BY id DESC LIMIT ?
                    )
                    """,
                    (keep_last,)
                )
                self.connection.commit()
        except sqlite3.Error as e:
            print("Prune error:", e)

    def summarize_old_conversations(self):
        """Hook for future LLM summarization"""
        pass

    # =========================================================
    # 🔒 CLOSE
    # =========================================================
    def close(self):
        try:
            with self.lock:
                if self.connection:
                    self.connection.close()
        except sqlite3.Error as e:
            print("DB close error:", e)


# =========================================================
# 🧪 TEST
# =========================================================
if __name__ == "__main__":
    mem = MemoryEngine()

    mem.save_memory("user", "name", "Sadekul")
    print(mem.get_memory("user", "name"))

    mem.save_conversation("user", "Hello")
    mem.save_conversation("assistant", "Hi!")

    print(mem.get_recent_conversations())

    mem.prune_old_conversations(50)

    mem.close()