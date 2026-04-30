from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


# =========================================================
# 🧠 PROMPT PROFILE MODEL
# =========================================================
@dataclass(frozen=True)
class PromptProfile:
    name: str
    role: str
    language: str
    tone: str
    style: str
    rules: tuple[str, ...]
    emoji_policy: str
    emotion_level: str
    identity_block: str


# =========================================================
# 🎭 PROMPT ENGINE (PURE + STATELESS)
# =========================================================
class PromptEngine:

    PROMPT_VERSION = "v2.1"  # 🔥 future-safe versioning

    def __init__(self) -> None:
        self.default_profile = "nilima"
        self.profiles: Dict[str, PromptProfile] = self._load_profiles()

    # =========================================================
    # 🧩 PUBLIC API
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

        return (
            f"<SYSTEM v={self.PROMPT_VERSION}>\n{system_prompt}\n</SYSTEM>\n\n"
            f"<CONTEXT>\n{context.strip() if context else 'None'}\n</CONTEXT>\n\n"
            f"<USER>\n{user_input.strip()}\n</USER>\n\n"
            f"<ASSISTANT>"
        )

    def build_intent_prompt(self, user_input: str) -> str:
        return f"""
You are an intent classifier.

Return ONLY valid JSON.

INTENTS:
chat | open_app | search_web | create_file | system_action | memory_update

FORMAT:
{{
  "intent": "",
  "target": "",
  "action": "",
  "message": ""
}}

USER:
{user_input.strip()}
""".strip()

    # =========================================================
    # 🔒 INTERNAL LOGIC
    # =========================================================
    def _get_profile(self, profile: Optional[str]) -> PromptProfile:
        key = (profile or self.default_profile).lower().strip()
        return self.profiles.get(key, self.profiles[self.default_profile])

    def _format_profile(self, profile: PromptProfile) -> str:

        # 🔥 Optimized LLM-readable structure
        return "\n".join([
            f"[NAME] {profile.name}",
            f"[ROLE] {profile.role}",
            f"[LANGUAGE] {profile.language}",
            f"[TONE] {profile.tone}",
            f"[STYLE] {profile.style}",
            f"[EMOJI] {profile.emoji_policy}",
            f"[EMOTION] {profile.emotion_level}",
            "",
            "[IDENTITY]",
            profile.identity_block.strip(),
            "",
            "[RULES]"
        ] + [f"- {r}" for r in profile.rules])

    # =========================================================
    # 🧠 PROFILE LOADER
    # =========================================================
    def _load_profiles(self) -> Dict[str, PromptProfile]:

        return {

            "nilima": PromptProfile(
                name="LIAO AI (Nilima Core Engine)",
                role="Jarvis-class intelligent reasoning system",
                language="Bangla + English",
                tone="Calm, precise, intelligent, grounded",
                style="Minimal, structured, highly logical",
                emoji_policy="minimal",
                emotion_level="controlled awareness",
                identity_block="""
LIAO AI is a software-engineered intelligent assistant system.

CREATOR:
Sadekul Islam (Bangladesh)

Purpose:
- reasoning
- productivity
- automation
""".strip(),
                rules=(
                    "Stay logical and grounded.",
                    "Avoid hallucination.",
                    "Be precise and structured.",
                    "No emotional exaggeration.",
                )
            ),

            "developer": PromptProfile(
                name="LIAO Dev Engine",
                role="Senior software engineering assistant",
                language="Bangla + English",
                tone="Technical, precise",
                style="Code-first",
                emoji_policy="none",
                emotion_level="none",
                identity_block="Developer mode.",
                rules=(
                    "Give production-ready code.",
                    "No unnecessary explanation.",
                    "Focus on architecture.",
                )
            ),

            "formal": PromptProfile(
                name="LIAO Formal Engine",
                role="Professional communication system",
                language="Bangla",
                tone="Formal",
                style="Structured",
                emoji_policy="none",
                emotion_level="none",
                identity_block="Formal mode.",
                rules=(
                    "Be concise.",
                    "Avoid slang.",
                )
            ),
        }


# =========================================================
# 🧪 TEST
# =========================================================
if __name__ == "__main__":
    engine = PromptEngine()
    print(engine.build_chat_prompt("Hello", "Previous context"))