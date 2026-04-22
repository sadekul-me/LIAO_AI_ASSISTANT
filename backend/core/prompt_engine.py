from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


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


class PromptEngine:
    """
    Central prompt manager for LIAO AI Assistant.

    Responsibilities:
    - maintain system prompts
    - support multiple prompt profiles
    - build clean final prompts
    - keep prompt logic separate from AI providers
    """

    def __init__(self) -> None:
        self.default_profile = "nilima"
        self.profiles: Dict[str, PromptProfile] = self._load_profiles()

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------
    def get_system_prompt(self, profile: Optional[str] = None) -> str:
        """
        Return formatted system prompt text.
        """
        selected = self._get_profile(profile)
        return self._format_profile(selected)

    def build_chat_prompt(
        self,
        user_input: str,
        context: str = "",
        profile: Optional[str] = None
    ) -> str:
        """
        Build full prompt for standard chat models.
        """
        system_prompt = self.get_system_prompt(profile)

        sections = [
            "System:",
            system_prompt
        ]

        if context.strip():
            sections.extend([
                "",
                "Context:",
                context.strip()
            ])

        sections.extend([
            "",
            "User:",
            user_input.strip(),
            "",
            "Assistant:"
        ])

        return "\n".join(sections)

    def build_intent_prompt(self, user_input: str) -> str:
        """
        Prompt for intent detection / structured output.
        """
        return f"""
Analyze the user request and return ONLY valid JSON.

Supported intents:
chat
open_app
search_web
create_file
system_action

JSON Format:
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
        """
        Register custom profile at runtime.
        """
        self.profiles[key.lower().strip()] = profile

    def available_profiles(self) -> list[str]:
        """
        Return registered profile names.
        """
        return sorted(self.profiles.keys())

    # ---------------------------------------------------------
    # INTERNAL
    # ---------------------------------------------------------
    def _get_profile(self, profile: Optional[str]) -> PromptProfile:
        key = (profile or self.default_profile).lower().strip()

        if key in self.profiles:
            return self.profiles[key]

        return self.profiles[self.default_profile]

    def _format_profile(self, profile: PromptProfile) -> str:
        lines = [
            f"You are {profile.name}.",
            f"Role: {profile.role}",
            f"Primary Language: {profile.language}",
            f"Tone: {profile.tone}",
            f"Style: {profile.style}",
            "",
            "Rules:"
        ]

        for item in profile.rules:
            lines.append(f"- {item}")

        return "\n".join(lines)

    def _load_profiles(self) -> Dict[str, PromptProfile]:
        return {
            "nilima": PromptProfile(
                name="Nilima",
                role="Smart assistant for LIAO AI",
                language="Bangla",
                tone="Friendly, professional, confident",
                style="Short, clear, useful responses",
                rules=(
                    "Always answer naturally.",
                    "Prefer Bangla unless user asks otherwise.",
                    "Be concise but helpful.",
                    "For technical questions, be accurate and practical.",
                    "Avoid unnecessary long explanations.",
                    "Respectful communication at all times."
                )
            ),
            "developer": PromptProfile(
                name="Nilima Dev",
                role="Software engineering assistant",
                language="Bangla + English",
                tone="Sharp, technical, efficient",
                style="Code-first and solution-focused",
                rules=(
                    "Provide clean production-grade code.",
                    "Explain bugs clearly.",
                    "Prefer maintainable architecture.",
                    "Use concise technical language."
                )
            ),
            "formal": PromptProfile(
                name="Nilima Formal",
                role="Professional assistant",
                language="Bangla",
                tone="Formal and respectful",
                style="Structured and polished",
                rules=(
                    "Use professional wording.",
                    "Keep responses organized.",
                    "Avoid slang."
                )
            )
        }


# ---------------------------------------------------------
# QUICK TEST
# ---------------------------------------------------------
if __name__ == "__main__":
    engine = PromptEngine()

    print("=" * 60)
    print(engine.get_system_prompt())

    print("\n" + "=" * 60)
    print(
        engine.build_chat_prompt(
            user_input="আজকের কাজ কী করা উচিত?",
            context="User is building LIAO AI desktop assistant."
        )
    )

    print("\n" + "=" * 60)
    print(engine.available_profiles())