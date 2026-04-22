import re
from typing import Optional


class AudioProcessor:
    """
    Audio/Text Processing Layer for Voice Engine

    Responsibilities:
    - Clean speech-to-text output
    - Normalize text
    - Remove noise and symbols
    - Prepare input for AI engine
    """

    def __init__(self):
        # optional: extend rules later
        self.allowed_pattern = re.compile(r"[^a-zA-Z0-9\s\u0980-\u09FF]")

    # --------------------------------------
    # MAIN CLEAN FUNCTION
    # --------------------------------------
    def clean(self, text: Optional[str]) -> str:
        """
        Clean raw speech text
        """

        if not text:
            return ""

        # lowercase
        text = text.lower().strip()

        # remove unwanted symbols
        text = self.allowed_pattern.sub("", text)

        # remove extra spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # --------------------------------------
    # SIMPLE NORMALIZER
    # --------------------------------------
    def normalize(self, text: str) -> str:
        """
        Additional normalization layer
        """

        if not text:
            return ""

        text = text.strip()

        # remove repeated characters (basic fix)
        text = re.sub(r"(.)\1{2,}", r"\1", text)

        return text

    # --------------------------------------
    # FULL PIPELINE
    # --------------------------------------
    def process(self, text: str) -> str:
        """
        Complete processing pipeline
        """

        text = self.clean(text)
        text = self.normalize(text)

        return text