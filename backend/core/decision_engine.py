from __future__ import annotations

import re
from difflib import get_close_matches
from typing import Dict, Any, Optional


class DecisionEngine:
    """
    🔥 LIAO AI - ULTRA BRAIN v4 (Real Jarvis Core)

    Features:
    - Bangla + English hybrid command support
    - Context-aware memory
    - Multi-intent scoring system
    - AI-powered code generation fallback
    - Smart extraction (file, path, project, message)
    - Dev automation ready
    """

    def __init__(self, ai_engine: Optional[object] = None):
        self.ai_engine = ai_engine

        # 🧠 context memory (last action)
        self.context: Dict[str, Any] = {}

        # =========================
        # APP KEYWORDS
        # =========================
        self.app_keywords = {
            "vscode": ["vscode", "vs code", "কোড এডিটর"],
            "chrome": ["chrome", "browser", "ব্রাউজার"],
            "notepad": ["notepad"],
            "spotify": ["spotify"],
            "terminal": ["terminal", "cmd", "টার্মিনাল"],
        }

        # =========================
        # INTENTS (WITH BANGLA)
        # =========================
        self.intents = {
            "open_app": {"k": ["open", "launch", "run", "খুলো"], "w": 2},
            "open_website": {"k": ["open website", "go to", "ওপেন কর"], "w": 2},
            "play_media": {"k": ["play", "watch", "চালাও"], "w": 3},

            "create_folder": {"k": ["create folder", "folder বানাও"], "w": 3},
            "create_file": {"k": ["create file", "file বানাও"], "w": 3},
            "write_code": {"k": ["write code", "code লিখ", "generate code"], "w": 5},
            "run_code": {"k": ["run code", "execute", "চালাও"], "w": 4},
            "create_project": {"k": ["create project", "project বানাও"], "w": 4},

            "copy": {"k": ["copy", "কপি"], "w": 3},
            "move": {"k": ["move", "সরাও"], "w": 3},
            "delete": {"k": ["delete", "remove", "ডিলিট"], "w": 3},

            "search_web": {"k": ["search", "google", "খুঁজ"], "w": 2},
            "send_whatsapp": {"k": ["whatsapp", "message পাঠাও"], "w": 3},

            "system": {"k": ["shutdown", "restart", "lock"], "w": 5},
        }

    # =========================================
    # 🧠 MAIN ENTRY
    # =========================================
    def analyze(self, text: str) -> Dict[str, Any]:
        clean = text.lower().strip()

        if not clean:
            return self._res("empty", "No input")

        # exit command
        if any(x in clean for x in ["exit", "quit"]):
            return self._res("system", "Exit", action="exit")

        intent = self._detect_intent(clean)

        if intent:
            result = self._handle(intent, text, clean)

            # 🔥 save context
            self.context = result
            return result

        return self._fallback(text)

    # =========================================
    # 🎯 INTENT DETECTION (SMART SCORING)
    # =========================================
    def _detect_intent(self, text: str) -> str:
        scores = {i: 0 for i in self.intents}

        for intent, data in self.intents.items():
            for k in data["k"]:
                if k in text:
                    scores[intent] += data["w"]

        # boost if app detected
        if self._extract_app(text):
            scores["open_app"] += 3

        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else ""

    # =========================================
    # ⚙️ HANDLER
    # =========================================
    def _handle(self, intent, raw, clean):

        if intent == "open_app":
            return self._res(intent, "Opening app", target=self._extract_app(clean))

        if intent == "create_file":
            return self._res(intent, "Creating file", target=self._extract_file(raw))

        if intent == "write_code":
            return self._res(
                intent,
                "Writing code",
                target=self._extract_file(raw),
                data={"code": self._generate_code(raw)}
            )

        if intent == "run_code":
            return self._res(intent, "Running code", target=self._extract_file(raw))

        if intent == "create_project":
            return self._res(
                intent,
                "Creating project",
                target=self._extract_project_name(raw),
                data={"type": self._extract_project_type(raw)}
            )

        if intent == "search_web":
            return self._res(intent, "Searching", target=self._extract_search(raw))

        if intent == "send_whatsapp":
            return self._res(intent, "Sending message", target=self._extract_message(raw))

        if intent == "system":
            return self._res(intent, "System action", action=self._extract_system(clean))

        return self._res("chat", "Normal conversation")

    # =========================================
    # 🧠 SMART CODE GENERATION
    # =========================================
    def _generate_code(self, text: str) -> str:

        # 🔥 AI-powered (BEST)
        if self.ai_engine and hasattr(self.ai_engine, "generate_code"):
            try:
                return self.ai_engine.generate_code(text)
            except:
                pass

        # ⚡ fallback templates
        if "fastapi" in text:
            return """from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from LIAO AI"}"""

        if "loop" in text:
            return """for i in range(10):
    print(i)"""

        return "print('🔥 LIAO AI')"

    # =========================================
    # 🔍 EXTRACTION
    # =========================================
    def _extract_app(self, text):
        for app, aliases in self.app_keywords.items():
            if any(a in text for a in aliases):
                return app
        return ""

    def _extract_file(self, text):
        match = re.search(r"([\w\-/\\]+\.\w+)", text)
        return match.group(1) if match else "main.py"

    def _extract_search(self, text):
        return re.sub(r"(search|google|play)", "", text, flags=re.I).strip()

    def _extract_message(self, text):
        return re.sub(r"(send message|whatsapp)", "", text, flags=re.I).strip()

    def _extract_project_name(self, text):
        match = re.search(r"project\s+(\w+)", text)
        return match.group(1) if match else "liao_project"

    def _extract_project_type(self, text):
        return "react" if "react" in text else "python"

    def _extract_system(self, text):
        for k in ["shutdown", "restart", "lock"]:
            if k in text:
                return k
        return "unknown"

    # =========================================
    # 🤖 FALLBACK AI
    # =========================================
    def _fallback(self, text):

        if self.ai_engine and hasattr(self.ai_engine, "detect_intent"):
            try:
                return self.ai_engine.detect_intent(text)
            except:
                pass

        return self._res("chat", "AI response")

    # =========================================
    # 📤 RESPONSE FORMAT
    # =========================================
    def _res(self, intent, message, target="", action="", data=None):
        return {
            "intent": intent,
            "message": message,
            "target": target,
            "action": action,
            "data": data or {}
        }