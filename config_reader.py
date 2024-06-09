from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    # Данные для подключения к MySQL серверу
    HOST: str
    USER: str
    PASSWORD: SecretStr
    DATABASE: str

    # Название файла лога для модуля хранения данных
    STORAGE_LOG_FILENAME: str = "storage_module.log"
    
    # Адрес микросервиса модуля хранения данных
    SMADDRESS: str

    # Порт микросервиса модуля хранения данных
    SMPORT: int

    # Адрес для подключения по modbus tcp
    MODBASTCP: str
    
    # Интервал опроса датчиков
    POLL_INTERVAL: int

    # Название файла лога для модуля опроса датчиков
    SENSOR_LOG_FILENAME: str = "sensors_module.log"

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()