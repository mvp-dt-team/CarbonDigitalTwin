from fastapi import FastAPI

from mysql_storage import MySQLStorage
from routers.measurement_sources import get_measurement_sources_router
from routers.measurements import get_measurements_router
from routers.sensor_models import get_sensor_models_router
from routers.sensors import get_sensors_router
from routers.blocks_router import blocks_router

import logging

from yaml import load
from yaml.loader import SafeLoader

with open("config.yaml", "r") as config_file:
    config = load(config_file, Loader=SafeLoader)

# Настройки MySQL
# mysql_host = 'localhost'
# mysql_user = 'digital_twin'
# mysql_password = 'digital_twin'
# mysql_database = 'digital_twin_database'

storage = MySQLStorage()

app = FastAPI()

logging.basicConfig(level=logging.INFO, filename=config["LOGNAME"], encoding="utf8")

# Temporary Redirect возникает из-за префиксов роутера, возможно, они используются как-то неверно
app.include_router(
    get_measurement_sources_router(storage), prefix="/measurement_source"
)
app.include_router(get_measurements_router(storage), prefix="/measurement")
app.include_router(get_sensors_router(storage), prefix="/sensor")
app.include_router(get_sensor_models_router(storage), prefix="/sensor_model")
app.include_router(blocks_router(storage), prefix="/blocks")
