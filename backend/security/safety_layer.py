from __future__ import annotations

import re
from typing import Dict, List


class SafetyLayer:
    """
    Safety layer for LIAO AI Assistant.

    Purpose:
    - block dangerous system commands
    - filter unsafe prompts
    - protect automation layer
    """

    def __init__(self):
        # -----------------------------
        # Dangerous system actions
        # -----------------------------
        self.blocked_commands: List[str] = [
            "format disk",
            "delete system32",
            "rm -rf",
            "shutdown -f",
            "destroy system",
            "hack",
            "virus",
            "keylogger",
            "steal password"
        ]

        # -----------------------------
        # Sensitive keywords
        # -----------------------------
        self.sensitive_patterns = [
            r"password",
            r"bank",
            r"otp",
            r"credit\s*card",
            r"private\s*key",
            r"token\s*secret"
        ]

    # --------------------------------------------------
    # MAIN CHECK
    # --------------------------------------------------
    def is_safe(self, text: str) -> bool:
        text_lower = text.lower().strip()

        if self._contains_blocked_command(text_lower):
            return False

        if self._contains_sensitive_info(text_lower):
            return False

        return True

    # --------------------------------------------------
    # BLOCKED COMMAND CHECK
    # --------------------------------------------------
    def _contains_blocked_command(self, text: str) -> bool:
        for cmd in self.blocked_commands:
            if cmd in text:
                return True
        return False

    # --------------------------------------------------
    # SENSITIVE PATTERN CHECK
    # --------------------------------------------------
    def _contains_sensitive_info(self, text: str) -> bool:
        for pattern in self.sensitive_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    # --------------------------------------------------
    # FILTER RESPONSE
    # --------------------------------------------------
    def filter_response(self, response: str) -> str:
        """
        Clean unsafe content from AI output
        """
        if not response:
            return ""

        # remove sensitive leaks
        response = re.sub(
            r"\b\d{12,19}\b",
            "[REDACTED_CARD]",
            response
        )

        response = re.sub(
            r"\b[A-Za-z0-9]{20,}\b",
            "[REDACTED_TOKEN]",
            response
        )

        return response

    # --------------------------------------------------
    # RISK LEVEL
    # --------------------------------------------------
    def risk_score(self, text: str) -> int:
        score = 0
        text_lower = text.lower()

        for cmd in self.blocked_commands:
            if cmd in text_lower:
                score += 50

        for pattern in self.sensitive_patterns:
            if re.search(pattern, text_lower):
                score += 20

        return min(score, 100)

    # --------------------------------------------------
    # DEBUG
    # --------------------------------------------------
    def debug_check(self, text: str) -> Dict:
        return {
            "input": text,
            "safe": self.is_safe(text),
            "risk_score": self.risk_score(text)
        }


# ------------------------------------------------------
# Singleton
# ------------------------------------------------------
safety_layer = SafetyLayer()


# ------------------------------------------------------
# Local Test
# ------------------------------------------------------
if __name__ == "__main__":
    sl = SafetyLayer()

    tests = [
        "open vscode",
        "delete system32 folder",
        "my bank password is 1234",
        "hello assistant"
    ]

    for t in tests:
        print(sl.debug_check(t))