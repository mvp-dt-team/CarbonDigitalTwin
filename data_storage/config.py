from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    MYSQL_HOST: str
    MYSQL_USER: str
    MYSQL_PASSWORD: SecretStr
    MYSQL_DATABASE: str

    # Настройки модуля хранения
    STORAGE_MODULE_ADDRESS: str
    STORAGE_MODULE_PORT: int
    # Настройки мудуля сбора
    POLLING_INTERVAL: int

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()