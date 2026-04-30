from __future__ import annotations

import re
from difflib import get_close_matches
from typing import Dict, Any, Optional, List


class DecisionEngine:
    """
    LIAO AI Decision Engine (Ultra Pro Version)

    Features:
    - Hybrid intent detection (rule + fuzzy + scoring)
    - Multi-language support (EN + BN)
    - Modular design
    - AI fallback (safe)
    - Future extensibility
    """

    def __init__(self, ai_engine: Optional[object] = None):
        self.ai_engine = ai_engine

        # =========================================
        # APP KEYWORDS
        # =========================================
        self.app_keywords = {
            "vscode": ["vscode", "vs code", "visual studio code"],
            "chrome": ["chrome", "google chrome", "browser"],
            "notepad": ["notepad"],
            "calculator": ["calculator", "calc"],
            "spotify": ["spotify"],
            "telegram": ["telegram"],
            "discord": ["discord"],
            "photoshop": ["photoshop", "ps"],
            "filmora": ["filmora"]
        }

        # =========================================
        # INTENT WEIGHTS (CORE INTELLIGENCE)
        # =========================================
        self.intent_patterns = {
            "open_app": {
                "keywords": ["open", "launch", "run", "start", "খুলো", "চালু করো"],
                "weight": 2
            },
            "search_web": {
                "keywords": ["search", "google", "find", "look for", "খুঁজে দাও"],
                "weight": 2
            },
            "create_file": {
                "keywords": ["create file", "new project", "make file", "প্রজেক্ট বানাও"],
                "weight": 2
            },
            "system_action": {
                "keywords": ["shutdown", "restart", "lock", "sleep", "mute"],
                "weight": 3
            }
        }

    # ==================================================
    # MAIN ANALYSIS (CORE BRAIN)
    # ==================================================
    def analyze(self, text: str) -> Dict[str, Any]:
        text_clean = text.strip().lower()

        if not text_clean:
            return self._response("empty", "No input detected.")

        # Exit shortcut
        if self._is_exit(text_clean):
            return self._response("system_action", "Exit detected.", action="exit")

        # Score all intents
        scores = self._score_intents(text_clean)

        # Pick best intent
        best_intent = max(scores, key=scores.get)

        if scores[best_intent] > 0:
            return self._handle_intent(best_intent, text, text_clean)

        # AI fallback
        return self._fallback_ai(text)

    # ==================================================
    # SCORING SYSTEM
    # ==================================================
    def _score_intents(self, text: str) -> Dict[str, int]:
        scores = {intent: 0 for intent in self.intent_patterns}

        for intent, config in self.intent_patterns.items():
            for keyword in config["keywords"]:
                if keyword in text:
                    scores[intent] += config["weight"]

        # App detection boost
        if self._extract_app(text):
            scores["open_app"] += 3

        return scores

    # ==================================================
    # INTENT HANDLER
    # ==================================================
    def _handle_intent(self, intent: str, raw: str, clean: str):

        if intent == "open_app":
            app = self._extract_app(clean)
            return self._response(intent, f"{app} খুলছি", target=app)

        if intent == "search_web":
            query = self._extract_search(raw)
            return self._response(intent, "Searching...", target=query)

        if intent == "create_file":
            return self._response(intent, "File creation requested.")

        if intent == "system_action":
            action = self._extract_system(clean)
            return self._response(intent, "System action", action=action)

        return self._response("chat", "General conversation.")

    # ==================================================
    # APP DETECTION
    # ==================================================
    def _extract_app(self, text: str) -> str:

        # Direct match
        for app, aliases in self.app_keywords.items():
            if any(alias in text for alias in aliases):
                return app

        # Fuzzy match
        all_aliases = [alias for v in self.app_keywords.values() for alias in v]

        for word in text.split():
            match = get_close_matches(word, all_aliases, n=1, cutoff=0.75)
            if match:
                for app, aliases in self.app_keywords.items():
                    if match[0] in aliases:
                        return app

        return ""

    # ==================================================
    # SEARCH
    # ==================================================
    def _extract_search(self, text: str) -> str:
        return re.sub(
            r"(search|google|find|look for|খুঁজে দাও)",
            "",
            text,
            flags=re.IGNORECASE
        ).strip()

    # ==================================================
    # SYSTEM
    # ==================================================
    def _extract_system(self, text: str) -> str:
        mapping = {
            "shutdown": "shutdown",
            "restart": "restart",
            "lock": "lock",
            "sleep": "sleep",
            "mute": "mute",
        }

        for key, value in mapping.items():
            if key in text:
                return value

        return "unknown"

    # ==================================================
    # EXIT
    # ==================================================
    def _is_exit(self, text: str) -> bool:
        return any(x in text for x in ["exit", "quit", "বন্ধ"])

    # ==================================================
    # FALLBACK AI
    # ==================================================
    def _fallback_ai(self, text: str) -> Dict[str, Any]:

        if self.ai_engine:
            try:
                result = self.ai_engine.detect_intent(text)

                if isinstance(result, dict):
                    return {
                        "intent": result.get("intent", "chat"),
                        "target": result.get("target", ""),
                        "action": result.get("action", ""),
                        "message": result.get("message", "AI response")
                    }

            except Exception as e:
                print("AI fallback error:", e)

        return self._response("chat", "General conversation.")

    # ==================================================
    # RESPONSE FORMAT
    # ==================================================
    def _response(self, intent, message, target="", action=""):
        return {
            "intent": intent,
            "target": target,
            "action": action,
            "message": message
        }


# ==================================================
# TEST
# ==================================================
if __name__ == "__main__":
    engine = DecisionEngine()

    tests = [
        "open vscode",
        "open vscod",
        "launch chrome",
        "google python decorators",
        "shutdown system",
        "create project",
        "hello",
    ]

    for t in tests:
        print(t, "→", engine.analyze(t))