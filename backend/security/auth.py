from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional


class AuthManager:
    """
    Authentication manager for LIAO AI Assistant.

    Features:
    - local password verification
    - session token generation
    - token validation
    - logout support
    - simple memory-based session store
    """

    def __init__(
        self,
        master_password: str = "liao123",
        session_minutes: int = 180
    ):
        self._password_hash = self._hash_text(
            master_password
        )

        self.session_minutes = session_minutes

        self.sessions: Dict[str, dict] = {}

    # --------------------------------------------------
    # Hash Helpers
    # --------------------------------------------------
    def _hash_text(
        self,
        text: str
    ) -> str:
        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

    def _safe_compare(
        self,
        a: str,
        b: str
    ) -> bool:
        return hmac.compare_digest(a, b)

    # --------------------------------------------------
    # Password Management
    # --------------------------------------------------
    def verify_password(
        self,
        password: str
    ) -> bool:
        incoming = self._hash_text(password)

        return self._safe_compare(
            incoming,
            self._password_hash
        )

    def change_password(
        self,
        old_password: str,
        new_password: str
    ) -> bool:

        if not self.verify_password(
            old_password
        ):
            return False

        self._password_hash = self._hash_text(
            new_password
        )

        self.sessions.clear()

        return True

    # --------------------------------------------------
    # Session Handling
    # --------------------------------------------------
    def login(
        self,
        password: str,
        username: str = "local"
    ) -> Optional[str]:

        if not self.verify_password(
            password
        ):
            return None

        token = secrets.token_urlsafe(32)

        expires = (
            datetime.now()
            + timedelta(
                minutes=self.session_minutes
            )
        )

        self.sessions[token] = {
            "username": username,
            "created_at": datetime.now(),
            "expires_at": expires
        }

        return token

    def validate_token(
        self,
        token: str
    ) -> bool:

        session = self.sessions.get(token)

        if not session:
            return False

        if datetime.now() > session["expires_at"]:
            self.sessions.pop(
                token,
                None
            )
            return False

        return True

    def get_user(
        self,
        token: str
    ) -> Optional[str]:

        if not self.validate_token(
            token
        ):
            return None

        return self.sessions[token][
            "username"
        ]

    def logout(
        self,
        token: str
    ) -> bool:

        if token in self.sessions:
            self.sessions.pop(token)
            return True

        return False

    def logout_all(self) -> None:
        self.sessions.clear()

    # --------------------------------------------------
    # Security Utilities
    # --------------------------------------------------
    def refresh_token(
        self,
        token: str
    ) -> bool:

        if not self.validate_token(
            token
        ):
            return False

        self.sessions[token][
            "expires_at"
        ] = (
            datetime.now()
            + timedelta(
                minutes=self.session_minutes
            )
        )

        return True

    def active_sessions(self) -> int:
        self.cleanup_expired()
        return len(self.sessions)

    def cleanup_expired(self) -> None:
        now = datetime.now()

        expired = [
            token
            for token, data
            in self.sessions.items()
            if now > data["expires_at"]
        ]

        for token in expired:
            self.sessions.pop(
                token,
                None
            )


# ------------------------------------------------------
# Singleton
# ------------------------------------------------------
auth_manager = AuthManager()


# ------------------------------------------------------
# Local Test
# ------------------------------------------------------
if __name__ == "__main__":
    auth = AuthManager(
        master_password="admin123"
    )

    token = auth.login(
        password="admin123",
        username="Sadik"
    )

    print("Token:", token)

    if token:
        print(
            "Valid:",
            auth.validate_token(token)
        )

        print(
            "User:",
            auth.get_user(token)
        )

        auth.logout(token)

        print(
            "After logout:",
            auth.validate_token(token)
        )