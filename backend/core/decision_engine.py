import re
import json
from difflib import get_close_matches
from typing import Dict, Any, Optional


class DecisionEngine:
    """
    LIAO AI Assistant Decision Engine

    Features:
    - Intent Detection
    - App Open Command
    - Web Search Command
    - System Command
    - File / Project Request
    - Fuzzy Matching
    - AI Fallback
    """

    def __init__(self, ai_engine: Optional[object] = None):
        self.ai_engine = ai_engine

        # --------------------------------------
        # APP KEYWORDS
        # --------------------------------------
        self.app_keywords = {
            "vscode": [
                "vscode",
                "vs code",
                "visual studio code",
                "code editor"
            ],
            "chrome": [
                "chrome",
                "google chrome",
                "browser"
            ],
            "notepad": [
                "notepad"
            ],
            "calculator": [
                "calculator",
                "calc"
            ],
            "spotify": [
                "spotify"
            ],
            "telegram": [
                "telegram"
            ],
            "discord": [
                "discord"
            ],
            "photoshop": [
                "photoshop",
                "ps"
            ],
            "filmora": [
                "filmora"
            ]
        }

    # ==================================================
    # MAIN ANALYZE
    # ==================================================
    def analyze(self, text: str) -> Dict[str, Any]:
        user_input = text.strip().lower()

        if not user_input:
            return self._response(
                intent="empty",
                message="No input detected."
            )

        # Exit
        if self._is_exit_command(user_input):
            return self._response(
                intent="system_action",
                action="exit_app",
                message="Exit command detected."
            )

        # Open App
        if self._is_open_app(user_input):
            app_name = self._extract_app_name(user_input)

            return self._response(
                intent="open_app",
                target=app_name,
                message=f"{app_name} খুলছি।"
            )

        # Search Web
        if self._is_search_request(user_input):
            query = self._extract_search_query(text)

            return self._response(
                intent="search_web",
                target=query,
                message="Search request detected."
            )

        # File / Project
        if self._is_file_request(user_input):
            return self._response(
                intent="create_file",
                message="File / project creation request detected."
            )

        # System Command
        if self._is_system_command(user_input):
            action = self._extract_system_action(user_input)

            return self._response(
                intent="system_action",
                action=action,
                message="System command detected."
            )

        # Fallback AI
        return self._fallback_ai_or_chat(text)

    # ==================================================
    # RESPONSE FORMAT
    # ==================================================
    def _response(
        self,
        intent: str,
        message: str,
        target: str = "",
        action: str = ""
    ) -> Dict[str, Any]:

        return {
            "intent": intent,
            "target": target,
            "action": action,
            "message": message
        }

    # ==================================================
    # EXIT
    # ==================================================
    def _is_exit_command(self, text: str) -> bool:
        keywords = [
            "exit",
            "quit",
            "close",
            "বন্ধ করো",
            "shutdown assistant"
        ]

        return any(word in text for word in keywords)

    # ==================================================
    # OPEN APP
    # ==================================================
    def _is_open_app(self, text: str) -> bool:
        trigger_words = [
            "open",
            "launch",
            "start",
            "run",
            "খুলো",
            "চালু করো"
        ]

        has_trigger = any(
            word in text for word in trigger_words
        )

        has_app = self._extract_app_name(text) != ""

        return has_trigger and has_app

    def _extract_app_name(self, text: str) -> str:
        # Direct Match
        for app_name, aliases in self.app_keywords.items():
            for alias in aliases:
                if alias in text:
                    return app_name

        # Fuzzy Match
        all_aliases = []
        alias_map = {}

        for app_name, aliases in self.app_keywords.items():
            for alias in aliases:
                all_aliases.append(alias)
                alias_map[alias] = app_name

        for word in text.split():
            match = get_close_matches(
                word,
                all_aliases,
                n=1,
                cutoff=0.72
            )

            if match:
                return alias_map[match[0]]

        return ""

    # ==================================================
    # SEARCH
    # ==================================================
    def _is_search_request(self, text: str) -> bool:
        keywords = [
            "search",
            "google",
            "find",
            "look for",
            "খুঁজে দাও"
        ]

        return any(word in text for word in keywords)

    def _extract_search_query(self, text: str) -> str:
        cleaned = re.sub(
            r"(search|google|find|look for)",
            "",
            text,
            flags=re.IGNORECASE
        )

        return cleaned.strip()

    # ==================================================
    # FILE REQUEST
    # ==================================================
    def _is_file_request(self, text: str) -> bool:
        keywords = [
            "create file",
            "make file",
            "new project",
            "create project",
            "ফাইল বানাও",
            "প্রজেক্ট বানাও"
        ]

        return any(word in text for word in keywords)

    # ==================================================
    # SYSTEM COMMAND
    # ==================================================
    def _is_system_command(self, text: str) -> bool:
        keywords = [
            "shutdown",
            "restart",
            "lock",
            "sleep",
            "mute",
            "volume up",
            "volume down",
            "brightness up",
            "brightness down"
        ]

        return any(word in text for word in keywords)

    def _extract_system_action(self, text: str) -> str:
        mapping = {
            "shutdown": "shutdown",
            "restart": "restart",
            "lock": "lock",
            "sleep": "sleep",
            "mute": "mute",
            "volume up": "volume_up",
            "volume down": "volume_down",
            "brightness up": "brightness_up",
            "brightness down": "brightness_down"
        }

        for key, value in mapping.items():
            if key in text:
                return value

        return "unknown"

    # ==================================================
    # FALLBACK AI
    # ==================================================
    def _fallback_ai_or_chat(
        self,
        text: str
    ) -> Dict[str, Any]:

        if self.ai_engine:
            try:
                result = self.ai_engine.detect_intent(text)

                if isinstance(result, dict):
                    return {
                        "intent": result.get(
                            "intent",
                            "chat"
                        ),
                        "target": result.get(
                            "target",
                            ""
                        ),
                        "action": result.get(
                            "action",
                            ""
                        ),
                        "message": result.get(
                            "message",
                            "General conversation."
                        )
                    }

            except Exception as error:
                print(
                    "Fallback AI Error:",
                    str(error)
                )

        return self._response(
            intent="chat",
            message="General conversation."
        )


# ==================================================
# TEST MODE
# ==================================================
if __name__ == "__main__":
    from backend.core.ai_engine import AIEngine

    ai = AIEngine()
    engine = DecisionEngine(ai)

    tests = [
        "open vscode",
        "open vscod",
        "open chrome",
        "google python decorators",
        "volume up",
        "restart pc",
        "create project",
        "hello nilima",
        "who are you"
    ]

    for item in tests:
        print("Input:", item)
        print(engine.analyze(item))
        print("-" * 50)