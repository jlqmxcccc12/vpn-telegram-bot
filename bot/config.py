from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    telegram_bot_token: str
    backend_host: str = "localhost"
    backend_port: int = 8000
    log_level: str = "INFO"
    class Config:
        env_file = ".env"
        case_sensitive = False
    @property
    def backend_url(self) -> str:
        return f"http://{self.backend_host}:{self.backend_port}/api"

settings = Settings()