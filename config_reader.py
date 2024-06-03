from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    HOST: str
    USER: str
    PASSWORD: SecretStr
    DATABASE: str

    # Настройки модуля хранения
    SMADDRESS: str
    SMPORT: int
    # Настройки мудуля сбора
    POLL_INTERVAL: int

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()
print(config)