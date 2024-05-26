from fastapi import FastAPI

from data_storage.mysql_storage import MySQLStorage
from data_storage.routers.measurement_sources import get_measurement_sources_router
from data_storage.routers.measurements import get_measurements_router
from data_storage.routers.sensor_models import get_sensor_models_router
from data_storage.routers.sensors import get_sensors_router

# Настройки MySQL
mysql_host = 'localhost'
mysql_user = 'digital_twin'
mysql_password = 'digital_twin'
mysql_database = 'digital_twin_database'

storage = MySQLStorage(mysql_host, mysql_password, mysql_user, mysql_database)

app = FastAPI()

app.include_router(get_measurement_sources_router(storage), prefix="/measurement_source")
app.include_router(get_measurements_router(storage), prefix="/measurement")
app.include_router(get_sensors_router(storage), prefix="/sensor")
app.include_router(get_sensor_models_router(storage), prefix="/sensor_model")
