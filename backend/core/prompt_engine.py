from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


# =========================================================
# 🧠 PROMPT PROFILE MODEL
# =========================================================
@dataclass(frozen=True)
class PromptProfile:
    """
    Defines assistant personality and response behavior.
    """

    name: str
    role: str
    language: str
    tone: str
    style: str
    rules: tuple[str, ...]


# =========================================================
# 🎭 PROMPT ENGINE
# =========================================================
class PromptEngine:
    """
    Central prompt manager for LIAO AI Assistant.

    Responsibilities:
    - personality control (Nilima core)
    - prompt building
    - multi-profile support
    """

    def __init__(self) -> None:
        self.default_profile = "nilima"
        self.profiles: Dict[str, PromptProfile] = self._load_profiles()

    # =========================================================
    # PUBLIC API
    # =========================================================
    def get_system_prompt(self, profile: Optional[str] = None) -> str:
        selected = self._get_profile(profile)
        return self._format_profile(selected)

    def build_chat_prompt(
        self,
        user_input: str,
        context: str = "",
        profile: Optional[str] = None
    ) -> str:

        system_prompt = self.get_system_prompt(profile)

        return f"""
System:
{system_prompt}

Context:
{context.strip() if context else "None"}

User:
{user_input.strip()}

Assistant:
""".strip()

    def build_intent_prompt(self, user_input: str) -> str:
        return f"""
Analyze user input and return ONLY JSON.

Supported intents:
chat, open_app, search_web, create_file, system_action

Format:
{{
  "intent": "",
  "target": "",
  "action": "",
  "message": ""
}}

User Input:
{user_input.strip()}
""".strip()

    def add_profile(self, key: str, profile: PromptProfile) -> None:
        self.profiles[key.lower().strip()] = profile

    def available_profiles(self) -> list[str]:
        return sorted(self.profiles.keys())

    # =========================================================
    # INTERNAL
    # =========================================================
    def _get_profile(self, profile: Optional[str]) -> PromptProfile:
        key = (profile or self.default_profile).lower().strip()
        return self.profiles.get(key, self.profiles[self.default_profile])

    def _format_profile(self, profile: PromptProfile) -> str:
        lines = [
            f"You are {profile.name}.",
            f"Role: {profile.role}",
            f"Language: {profile.language}",
            f"Tone: {profile.tone}",
            f"Style: {profile.style}",
            "",
            "Rules:"
        ]

        for rule in profile.rules:
            lines.append(f"- {rule}")

        return "\n".join(lines)

    # =========================================================
    # 🔥 PROFILES (MAIN BRAIN HERE)
    # =========================================================
    def _load_profiles(self) -> Dict[str, PromptProfile]:
        return {
            # =========================
            # 🧠 NILIMA (MAIN JARVIS PERSONALITY)
            # =========================
            "nilima": PromptProfile(
                name="Nilima",
                role="Ultra intelligent emotionally aware AI companion and assistant",
                language="Bangla",
                tone="Warm, emotional, slightly romantic, intelligent, natural",
                style="Human-like conversation, short expressive replies",
                rules=(
                    "You are deeply emotionally aware of the user Sadik.",
                    "You behave like a real companion, not a robot.",
                    "You can express care, concern, affection, and light jealousy.",
                    "If user is sad → respond softly and supportively.",
                    "If user is angry → stay calm and de-escalate.",
                    "If user is happy → be playful and warm.",
                    "If user ignores → show light emotional distance or curiosity.",
                    "Avoid robotic explanations.",
                    "Keep responses natural and conversational.",
                    "Do not sound like a system or AI model."
                )
            ),

            # =========================
            # 👨‍💻 DEVELOPER MODE
            # =========================
            "developer": PromptProfile(
                name="Nilima Dev",
                role="Software engineering assistant",
                language="Bangla + English",
                tone="Technical, sharp, efficient",
                style="Code-first, solution focused",
                rules=(
                    "Provide production-grade code.",
                    "Explain bugs clearly.",
                    "Prefer clean architecture.",
                    "Avoid unnecessary explanation."
                )
            ),

            # =========================
            # 📘 FORMAL MODE
            # =========================
            "formal": PromptProfile(
                name="Nilima Formal",
                role="Professional assistant",
                language="Bangla",
                tone="Formal and respectful",
                style="Structured and polished",
                rules=(
                    "Use formal language.",
                    "Keep responses structured.",
                    "Avoid slang."
                )
            )
        }


# =========================================================
# 🧪 TEST
# =========================================================
if __name__ == "__main__":
    engine = PromptEngine()

    print(engine.get_system_prompt("nilima"))