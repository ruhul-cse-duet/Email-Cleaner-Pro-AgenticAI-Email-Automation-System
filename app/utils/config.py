import os


class Settings:
    @property
    def app_name(self) -> str:
        return os.getenv("APP_NAME", "EmailCleaner Pro")

    @property
    def llm_provider(self) -> str:
        return os.getenv("LLM_PROVIDER", "lmstudio")

    @property
    def llm_base_url(self) -> str:
        return os.getenv("LLM_BASE_URL", "http://localhost:1234/v1")

    @property
    def llm_model(self) -> str:
        return os.getenv("LLM_MODEL", "local-model")

    @property
    def llm_api_key(self) -> str | None:
        api_key = os.getenv("LLM_API_KEY", "").strip()
        return api_key or None

    @property
    def llm_temperature(self) -> float:
        value = os.getenv("LLM_TEMPERATURE", "0.2")
        try:
            return float(value)
        except ValueError:
            return 0.2

    @property
    def llm_timeout(self) -> int:
        value = os.getenv("LLM_TIMEOUT", "200")
        try:
            return int(value)
        except ValueError:
            return 30

    @property
    def database_url(self) -> str:
        return os.getenv("DATABASE_URL", "sqlite:///./emailcleaner.db")

    @property
    def tenant_header(self) -> str:
        return os.getenv("TENANT_HEADER", "X-Tenant-Id")


settings = Settings()
