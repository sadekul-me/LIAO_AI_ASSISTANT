import os
from pathlib import Path
from dotenv import load_dotenv


# ==================================================
# BASE PATH
# ==================================================
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


class Settings:
    """
    Global Settings for LIAO AI Assistant

    Handles:
    - environment variables
    - app/server config
    - Gemini + Groq AI config
    - database config
    - frontend config
    - voice config
    - feature flags
    """

    def __init__(self):
        # ------------------------------------------
        # APP INFO
        # ------------------------------------------
        self.project_name = self._get_env(
            "APP_NAME",
            "LIAO AI Assistant"
        )

        self.version = self._get_env(
            "APP_VERSION",
            "1.0.0"
        )

        self.environment = self._get_env(
            "APP_ENV",
            "development"
        )

        self.debug = self._to_bool(
            self._get_env("DEBUG", "true")
        )

        # ------------------------------------------
        # SERVER
        # ------------------------------------------
        self.host = self._get_env(
            "HOST",
            "127.0.0.1"
        )

        self.port = int(
            self._get_env("PORT", "8000")
        )

        self.reload = self._to_bool(
            self._get_env("RELOAD", "true")
        )

        # ------------------------------------------
        # SECURITY
        # ------------------------------------------
        self.secret_key = self._get_env(
            "SECRET_KEY",
            "change-this-secret-key"
        )

        self.token_expire_minutes = int(
            self._get_env(
                "TOKEN_EXPIRE_MINUTES",
                "1440"
            )
        )

        # ------------------------------------------
        # GEMINI AI
        # ------------------------------------------
        self.gemini_api_key = self._get_env(
            "GEMINI_API_KEY",
            ""
        )

        self.gemini_model = self._get_env(
            "GEMINI_MODEL",
            "gemini-2.0-flash"
        )

        # ------------------------------------------
        # GROQ AI
        # ------------------------------------------
        self.groq_api_key = self._get_env(
            "GROQ_API_KEY",
            ""
        )

        self.groq_model = self._get_env(
            "GROQ_MODEL",
            "llama3-70b-8192"
        )

        # ------------------------------------------
        # DATABASE
        # ------------------------------------------
        self.database_url = self._get_env(
            "DATABASE_URL",
            "sqlite:///data/memory.db"
        )

        self.memory_db_path = self._get_env(
            "MEMORY_DB_PATH",
            "data/memory.db"
        )

        # ------------------------------------------
        # LOGGING
        # ------------------------------------------
        self.log_level = self._get_env(
            "LOG_LEVEL",
            "INFO"
        ).upper()

        self.log_dir = BASE_DIR / "data" / "logs"
        self.cache_dir = BASE_DIR / "data" / "cache"

        # ------------------------------------------
        # FRONTEND
        # ------------------------------------------
        self.frontend_title = self._get_env(
            "FRONTEND_TITLE",
            "LIAO AI"
        )

        self.theme = self._get_env(
            "THEME",
            "dark"
        )

        # ------------------------------------------
        # VOICE
        # ------------------------------------------
        self.voice_enabled = self._to_bool(
            self._get_env(
                "VOICE_ENABLED",
                "true"
            )
        )

        self.default_voice = self._get_env(
            "DEFAULT_VOICE",
            "bn-BD-NabanitaNeural"
        )

        self.wake_word = self._get_env(
            "WAKE_WORD",
            "hey liao"
        )

        # ------------------------------------------
        # FEATURE FLAGS
        # ------------------------------------------
        self.enable_memory = self._to_bool(
            self._get_env(
                "ENABLE_MEMORY",
                "true"
            )
        )

        self.enable_voice = self._to_bool(
            self._get_env(
                "ENABLE_VOICE",
                "true"
            )
        )

        self.enable_automation = self._to_bool(
            self._get_env(
                "ENABLE_AUTOMATION",
                "true"
            )
        )

        self.enable_fallback_ai = self._to_bool(
            self._get_env(
                "ENABLE_FALLBACK_AI",
                "true"
            )
        )

        self.enable_offline_engine = self._to_bool(
            self._get_env(
                "ENABLE_OFFLINE_ENGINE",
                "true"
            )
        )

        # Create required folders
        self._create_directories()

    # ==================================================
    # HELPERS
    # ==================================================
    def _get_env(self, key: str, default=None):
        return os.getenv(key, default)

    def _to_bool(self, value) -> bool:
        return str(value).strip().lower() in (
            "1",
            "true",
            "yes",
            "on"
        )

    def _create_directories(self):
        self.log_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.cache_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        Path(self.memory_db_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

    # ==================================================
    # ENV CHECK
    # ==================================================
    def is_production(self):
        return self.environment.lower() == "production"

    def is_development(self):
        return self.environment.lower() == "development"

    # ==================================================
    # VALIDATION
    # ==================================================
    def validate(self):
        warnings = []

        if not self.gemini_api_key:
            warnings.append(
                "GEMINI_API_KEY missing."
            )

        if not self.groq_api_key:
            warnings.append(
                "GROQ_API_KEY missing."
            )

        if self.secret_key == "change-this-secret-key":
            warnings.append(
                "SECRET_KEY using default value."
            )

        return warnings

    # ==================================================
    # EXPORT
    # ==================================================
    def as_dict(self):
        return {
            "project_name": self.project_name,
            "version": self.version,
            "environment": self.environment,
            "debug": self.debug,
            "host": self.host,
            "port": self.port,
            "reload": self.reload,

            "gemini_model": self.gemini_model,
            "groq_model": self.groq_model,

            "database_url": self.database_url,
            "memory_db_path": self.memory_db_path,

            "log_level": self.log_level,

            "voice_enabled": self.voice_enabled,
            "default_voice": self.default_voice,
            "wake_word": self.wake_word,

            "enable_memory": self.enable_memory,
            "enable_voice": self.enable_voice,
            "enable_automation": self.enable_automation,
            "enable_fallback_ai": self.enable_fallback_ai,
            "enable_offline_engine": self.enable_offline_engine
        }


# ==================================================
# SINGLETON INSTANCE
# ==================================================
settings = Settings()


# ==================================================
# DEBUG RUN
# ==================================================
if __name__ == "__main__":
    print(settings.as_dict())

    issues = settings.validate()

    if issues:
        print("\nWarnings:")

        for item in issues:
            print("-", item)