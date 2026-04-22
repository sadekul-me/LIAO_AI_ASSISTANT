import logging
import os
from datetime import datetime
from typing import Optional


class Logger:
    """
    Central Logging System for LIAO AI Assistant

    Features:
    - File + console logging
    - Error tracking
    - Info/debug separation
    - Timestamped logs
    """

    def __init__(self, name: str = "LIAO", log_file: Optional[str] = None):
        self.name = name

        # Create logs directory if not exists
        os.makedirs("data/logs", exist_ok=True)

        # Default log file
        if not log_file:
            log_file = f"data/logs/{datetime.now().strftime('%Y-%m-%d')}.log"

        self.log_file = log_file

        # Logger setup
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Prevent duplicate handlers
        if not self.logger.handlers:

            # Formatter
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            # File handler
            file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(logging.INFO)

            # Add handlers
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    # --------------------------------------
    # INFO LOG
    # --------------------------------------
    def info(self, message: str):
        self.logger.info(message)

    # --------------------------------------
    # DEBUG LOG
    # --------------------------------------
    def debug(self, message: str):
        self.logger.debug(message)

    # --------------------------------------
    # WARNING LOG
    # --------------------------------------
    def warning(self, message: str):
        self.logger.warning(message)

    # --------------------------------------
    # ERROR LOG
    # --------------------------------------
    def error(self, message: str):
        self.logger.error(message)

    # --------------------------------------
    # CRITICAL LOG
    # --------------------------------------
    def critical(self, message: str):
        self.logger.critical(message)

    # --------------------------------------
    # RAW LOG
    # --------------------------------------
    def raw(self, level: str, message: str):
        """
        Custom log level handler
        """
        level = level.lower()

        if level == "info":
            self.info(message)
        elif level == "debug":
            self.debug(message)
        elif level == "warning":
            self.warning(message)
        elif level == "error":
            self.error(message)
        elif level == "critical":
            self.critical(message)
        else:
            self.info(message)


# --------------------------------------
# GLOBAL LOGGER INSTANCE
# --------------------------------------
logger = Logger()