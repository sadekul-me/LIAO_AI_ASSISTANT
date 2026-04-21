import re
import json
from difflib import get_close_matches
from typing import Dict, Any, Optional


class DecisionEngine:
    """
    LIAO AI Assistant Decision Engine

    Responsibilities:
    - detect user intent
    - route commands
    - fuzzy matching
    - fallback AI intent detection
    - structured safe output
    """

    def __init__(self, ai_engine: Optional[object] = None):
        self.ai_engine = ai_engine

        self.app_keywords = {
            "vscode": [
                "vscode",
                "vs code",
                "visual studio code"
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
            "filmora": [
                "filmora"
            ],
            "photoshop": [
                "photoshop",
                "ps"
            ],
            "telegram": [
                "telegram"
            ],
            "discord": [
                "discord"
            ]
        }

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Main decision router
        """
        user_input = text.strip().lower()

        if not user_input:
            return self._response(
                intent="empty",
                message="No input detected."
            )

        if self._is_exit_command(user_input):
            return self._response(
                intent="system_action",
                action="exit_app",
                message="Exit command detected."
            )

        if self._is_open_app(user_input):
            app_name = self._extract_app_name(user_input)

            return self._response(
                intent="open_app",
                target=app_name,
                message=f"Open request for {app_name}."
            )

        if self._is_search_request(user_input):
            query = self._extract_search_query(text)

            return self._response(
                intent="search_web",
                target=query,
                message="Search request detected."
            )

        if self._is_file_request(user_input):
            return self._response(
                intent="create_file",
                message="File or project creation request detected."
            )

        if self._is_system_command(user_input):
            action = self._extract_system_action(user_input)

            return self._response(
                intent="system_action",
                action=action,
                message="System command detected."
            )

        return self._fallback_ai_or_chat(text)

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

    def _is_exit_command(self, text: str) -> bool:
        keywords = [
            "exit",
            "quit",
            "close app",
            "বন্ধ করো",
            "shutdown assistant"
        ]
        return any(word in text for word in keywords)

    def _is_open_app(self, text: str) -> bool:
        trigger_words = [
            "open",
            "launch",
            "start",
            "খুলো",
            "চালু করো"
        ]

        has_trigger = any(word in text for word in trigger_words)
        has_app = self._extract_app_name(text) != ""

        return has_trigger and has_app

    def _extract_app_name(self, text: str) -> str:
        for app_name, aliases in self.app_keywords.items():
            for alias in aliases:
                if alias in text:
                    return app_name

        all_aliases = []
        alias_map = {}

        for app_name, aliases in self.app_keywords.items():
            for alias in aliases:
                all_aliases.append(alias)
                alias_map[alias] = app_name

        words = text.split()

        for word in words:
            match = get_close_matches(
                word,
                all_aliases,
                n=1,
                cutoff=0.72
            )

            if match:
                return alias_map[match[0]]

        return ""

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

    def _is_system_command(self, text: str) -> bool:
        keywords = [
            "shutdown",
            "restart",
            "lock pc",
            "sleep pc",
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
            "lock pc": "lock",
            "sleep pc": "sleep",
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

    def _fallback_ai_or_chat(self, text: str) -> Dict[str, Any]:
        """
        AI fallback intent detection with safe JSON parsing.
        """
        if self.ai_engine:
            try:
                prompt = f"""
User request: {text}

Analyze the request and return ONLY valid JSON.

Supported intents:
chat
open_app
search_web
create_file
system_action

Format:
{{
  "intent": "",
  "target": "",
  "action": "",
  "message": ""
}}
"""

                result = self.ai_engine.generate_response(prompt)

                if not isinstance(result, str):
                    raise ValueError("Invalid AI response type")

                cleaned = re.sub(r"```json|```", "", result).strip()

                json_match = re.search(
                    r"\{.*\}",
                    cleaned,
                    re.DOTALL
                )

                if json_match:
                    json_text = json_match.group()

                    data = json.loads(json_text)

                    return {
                        "intent": data.get("intent", "chat"),
                        "target": data.get("target", ""),
                        "action": data.get("action", ""),
                        "message": data.get("message", "")
                    }

            except Exception as error:
                print("Fallback AI error:", error)

        return self._response(
            intent="chat",
            message="General conversation."
        )


if __name__ == "__main__":
    from backend.core.ai_engine import AIEngine

    ai = AIEngine()
    engine = DecisionEngine(ai)

    tests = [
        "open vscode",
        "open vscod",
        "google python decorators",
        "volume up",
        "create project",
        "আমার মন খারাপ গান চালাও",
        "hello nilima"
    ]

    for item in tests:
        print("Input:", item)
        print(engine.analyze(item))
        print("-" * 50)