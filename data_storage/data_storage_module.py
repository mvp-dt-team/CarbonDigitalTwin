from fastapi import FastAPI

from data_storage.mysql_storage import MySQLStorage
from data_storage.routers.measurement_sources import get_measurement_sources_router
from data_storage.routers.measurements import get_measurements_router
from data_storage.routers.sensor_models import get_sensor_models_router
from data_storage.routers.sensors import get_sensors_router

import logging
from config_reader import config

# Настройки MySQL
# mysql_host = 'localhost'
# mysql_user = 'digital_twin'
# mysql_password = 'digital_twin'
# mysql_database = 'digital_twin_database'

storage = MySQLStorage()

app = FastAPI()

logging.basicConfig(level=logging.INFO, filename=config.STORAGE_LOG_FILENAME, encoding='utf8')

# Temporary Redirect возникает из-за префиксов роутера, возможно, они используются как-то неверно
app.include_router(get_measurement_sources_router(storage), prefix="/measurement_source")
app.include_router(get_measurements_router(storage), prefix="/measurement")
app.include_router(get_sensors_router(storage), prefix="/sensor")
app.include_router(get_sensor_models_router(storage), prefix="/sensor_model")
