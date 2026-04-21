import sqlite3
from pathlib import Path
from datetime import datetime
from threading import Lock


class MemoryEngine:
    """
    LIAO AI Assistant Memory Engine

    Responsibilities:
    - persistent memory storage
    - recent conversation history
    - user preferences
    - safe SQLite operations
    """

    def __init__(self, db_path="data/memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.lock = Lock()

        self.connection = sqlite3.connect(
            self.db_path,
            check_same_thread=False,
            timeout=10
        )

        self.connection.row_factory = sqlite3.Row

        self._create_tables()

    def _create_tables(self):
        query_list = [
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                key_name TEXT NOT NULL,
                value TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
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
            """
            CREATE INDEX IF NOT EXISTS idx_memory_key
            ON memories (category, key_name)
            """
        ]

        try:
            with self.lock:
                cursor = self.connection.cursor()

                for query in query_list:
                    cursor.execute(query)

                self.connection.commit()

        except sqlite3.Error as error:
            print("Database setup error:", error)

    def _now(self):
        return datetime.utcnow().isoformat()

    def save_memory(self, category: str, key_name: str, value: str):
        try:
            with self.lock:
                cursor = self.connection.cursor()

                cursor.execute(
                    """
                    SELECT id FROM memories
                    WHERE category = ? AND key_name = ?
                    """,
                    (category, key_name)
                )

                row = cursor.fetchone()
                now = self._now()

                if row:
                    cursor.execute(
                        """
                        UPDATE memories
                        SET value = ?, updated_at = ?
                        WHERE id = ?
                        """,
                        (value, now, row["id"])
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO memories (
                            category,
                            key_name,
                            value,
                            created_at,
                            updated_at
                        )
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (category, key_name, value, now, now)
                    )

                self.connection.commit()

        except sqlite3.Error as error:
            print("Save memory error:", error)

    def get_memory(self, category: str, key_name: str):
        try:
            with self.lock:
                cursor = self.connection.cursor()

                cursor.execute(
                    """
                    SELECT value FROM memories
                    WHERE category = ? AND key_name = ?
                    LIMIT 1
                    """,
                    (category, key_name)
                )

                row = cursor.fetchone()

                return row["value"] if row else None

        except sqlite3.Error as error:
            print("Get memory error:", error)
            return None

    def get_all_memories(self, category=None):
        try:
            with self.lock:
                cursor = self.connection.cursor()

                if category:
                    cursor.execute(
                        """
                        SELECT category, key_name, value, updated_at
                        FROM memories
                        WHERE category = ?
                        ORDER BY updated_at DESC
                        """,
                        (category,)
                    )
                else:
                    cursor.execute(
                        """
                        SELECT category, key_name, value, updated_at
                        FROM memories
                        ORDER BY updated_at DESC
                        """
                    )

                rows = cursor.fetchall()

                return [dict(row) for row in rows]

        except sqlite3.Error as error:
            print("Fetch memories error:", error)
            return []

    def delete_memory(self, category: str, key_name: str):
        try:
            with self.lock:
                cursor = self.connection.cursor()

                cursor.execute(
                    """
                    DELETE FROM memories
                    WHERE category = ? AND key_name = ?
                    """,
                    (category, key_name)
                )

                self.connection.commit()

        except sqlite3.Error as error:
            print("Delete memory error:", error)

    def save_conversation(self, role: str, message: str):
        try:
            with self.lock:
                cursor = self.connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO conversations (
                        role,
                        message,
                        created_at
                    )
                    VALUES (?, ?, ?)
                    """,
                    (role, message, self._now())
                )

                self.connection.commit()

        except sqlite3.Error as error:
            print("Save conversation error:", error)

    def get_recent_conversations(self, limit=10):
        try:
            with self.lock:
                cursor = self.connection.cursor()

                cursor.execute(
                    """
                    SELECT role, message, created_at
                    FROM conversations
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (limit,)
                )

                rows = cursor.fetchall()

                data = [dict(row) for row in rows]
                data.reverse()

                return data

        except sqlite3.Error as error:
            print("Fetch conversations error:", error)
            return []

    def clear_conversations(self):
        try:
            with self.lock:
                cursor = self.connection.cursor()

                cursor.execute("DELETE FROM conversations")

                self.connection.commit()

        except sqlite3.Error as error:
            print("Clear conversations error:", error)

    def summarize_old_conversations(self):
        """
        Future feature placeholder:
        summarize old chat history and compress memory.
        """
        pass

    def close(self):
        try:
            with self.lock:
                if self.connection:
                    self.connection.close()

        except sqlite3.Error as error:
            print("Close database error:", error)


if __name__ == "__main__":
    memory = MemoryEngine()

    memory.save_memory("user", "name", "Sadik")
    memory.save_memory("user", "country", "Bangladesh")

    print(memory.get_memory("user", "name"))
    print(memory.get_all_memories())

    memory.save_conversation("user", "Hello")
    memory.save_conversation("assistant", "Hi Sadik")

    print(memory.get_recent_conversations())

    memory.close()