from __future__ import annotations

import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


class AuditLogger:
    """
    Central audit logger for LIAO AI Assistant.

    Tracks:
    - API actions
    - System commands
    - Security blocks
    - Errors
    - User activity
    """

    def __init__(
        self,
        log_dir: str = "data/logs",
        file_name: str = "audit.log",
        max_bytes: int = 2_000_000,
        backup_count: int = 5
    ):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.log_file = self.log_dir / file_name
        self.logger = logging.getLogger(
            "liao_audit"
        )

        if not self.logger.handlers:
            self.logger.setLevel(
                logging.INFO
            )

            handler = RotatingFileHandler(
                filename=self.log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8"
            )

            formatter = logging.Formatter(
                "%(message)s"
            )

            handler.setFormatter(
                formatter
            )

            self.logger.addHandler(
                handler
            )

    # --------------------------------------------------
    # Core Writer
    # --------------------------------------------------
    def _write(
        self,
        level: str,
        event: str,
        message: str,
        user: str = "local",
        source: str = "system",
        data: Optional[Dict[str, Any]] = None
    ) -> None:

        payload = {
            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "level": level.upper(),
            "event": event,
            "user": user,
            "source": source,
            "message": message,
            "data": data or {}
        }

        line = json.dumps(
            payload,
            ensure_ascii=False
        )

        if level.lower() == "error":
            self.logger.error(line)

        elif level.lower() == "warning":
            self.logger.warning(line)

        else:
            self.logger.info(line)

    # --------------------------------------------------
    # Public Methods
    # --------------------------------------------------
    def info(
        self,
        event: str,
        message: str,
        user: str = "local",
        source: str = "system",
        data: Optional[dict] = None
    ) -> None:

        self._write(
            level="info",
            event=event,
            message=message,
            user=user,
            source=source,
            data=data
        )

    def warning(
        self,
        event: str,
        message: str,
        user: str = "local",
        source: str = "system",
        data: Optional[dict] = None
    ) -> None:

        self._write(
            level="warning",
            event=event,
            message=message,
            user=user,
            source=source,
            data=data
        )

    def error(
        self,
        event: str,
        message: str,
        user: str = "local",
        source: str = "system",
        data: Optional[dict] = None
    ) -> None:

        self._write(
            level="error",
            event=event,
            message=message,
            user=user,
            source=source,
            data=data
        )

    # --------------------------------------------------
    # Ready-Made Actions
    # --------------------------------------------------
    def command_run(
        self,
        command: str,
        status: str = "success"
    ) -> None:

        self.info(
            event="command_run",
            message=f"{command} executed",
            data={
                "status": status
            }
        )

    def command_blocked(
        self,
        command: str,
        reason: str
    ) -> None:

        self.warning(
            event="command_blocked",
            message=f"{command} blocked",
            data={
                "reason": reason
            }
        )

    def login_attempt(
        self,
        username: str,
        success: bool
    ) -> None:

        self.info(
            event="login_attempt",
            message="Login checked",
            user=username,
            data={
                "success": success
            }
        )

    def provider_error(
        self,
        provider: str,
        error_text: str
    ) -> None:

        self.error(
            event="provider_error",
            message=f"{provider} failed",
            data={
                "error": error_text
            }
        )

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------
    def get_log_path(self) -> str:
        return str(self.log_file)

    def clear_logs(self) -> None:
        self.log_file.write_text(
            "",
            encoding="utf-8"
        )


# ------------------------------------------------------
# Singleton
# ------------------------------------------------------
audit_logger = AuditLogger()


# ------------------------------------------------------
# Local Test
# ------------------------------------------------------
if __name__ == "__main__":
    audit_logger.info(
        event="startup",
        message="System booted"
    )

    audit_logger.command_run(
        "open chrome"
    )

    audit_logger.command_blocked(
        "shutdown",
        "permission denied"
    )

    audit_logger.provider_error(
        "Gemini",
        "429 quota exceeded"
    )

    print(
        "Audit log ready:",
        audit_logger.get_log_path()
    )