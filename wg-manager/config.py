from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    wg_manager_port: int = 8001
    wg_manager_secret: str = "secret"
    log_level: str = "INFO"
    wg_config_path: str = "/etc/wireguard"
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()