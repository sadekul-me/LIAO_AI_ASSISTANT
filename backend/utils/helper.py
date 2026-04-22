from datetime import datetime
import re
import json
from typing import Any, Dict, Optional


class Helper:
    """
    Common Utility Helper for LIAO AI Assistant Backend

    Purpose:
    - Reduce duplicate code
    - Clean text / data
    - Format system outputs
    - Safe conversions
    """

    # --------------------------------------
    # TEXT CLEANING
    # --------------------------------------
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Remove extra spaces and normalize text
        """
        if not text:
            return ""

        return re.sub(r'\s+', ' ', text).strip()

    # --------------------------------------
    # TIME FORMAT
    # --------------------------------------
    @staticmethod
    def current_time(format_24: bool = True) -> str:
        """
        Return current system time
        """
        if format_24:
            return datetime.now().strftime("%H:%M:%S")
        else:
            return datetime.now().strftime("%I:%M:%S %p")

    # --------------------------------------
    # DATE FORMAT
    # --------------------------------------
    @staticmethod
    def current_date() -> str:
        """
        Return current system date
        """
        return datetime.now().strftime("%Y-%m-%d")

    # --------------------------------------
    # SAFE JSON PARSE
    # --------------------------------------
    @staticmethod
    def safe_json_parse(text: str) -> Dict[str, Any]:
        """
        Safely parse JSON string
        """
        try:
            return json.loads(text)
        except Exception:
            return {}

    # --------------------------------------
    # EXTRACT JSON FROM TEXT
    # --------------------------------------
    @staticmethod
    def extract_json(text: str) -> Optional[Dict[str, Any]]:
        """
        Extract JSON object from raw text
        """
        try:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception:
            return None

        return None

    # --------------------------------------
    # BOOL PARSER
    # --------------------------------------
    @staticmethod
    def to_bool(value: str) -> bool:
        """
        Convert string to boolean
        """
        return str(value).lower() in ["true", "1", "yes", "y"]

    # --------------------------------------
    # LIMIT TEXT LENGTH
    # --------------------------------------
    @staticmethod
    def limit_text(text: str, max_length: int = 200) -> str:
        """
        Trim text safely
        """
        if not text:
            return ""

        if len(text) <= max_length:
            return text

        return text[:max_length].rstrip() + "..."

    # --------------------------------------
    # DEBUG FORMAT
    # --------------------------------------
    @staticmethod
    def debug_log(title: str, data: Any) -> str:
        """
        Format debug output cleanly
        """
        return f"[{title}] => {data}"