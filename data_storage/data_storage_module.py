from datetime import time
from typing import List
from fastapi import FastAPI, Query

from data_storage.mysql_storage import MySQLStorage
from network_models.measurement_source_info import MeasurementSourceInfo
from network_models.sensor_model_info import SensorModelInfo
from network_models.sensors_info import SensorInfo
from network_models.measurements_info import MeasurementsInfo

# Настройки MySQL
mysql_host = 'localhost'
mysql_user = 'digital_twin'
mysql_password = 'digital_twin'
mysql_database = 'digital_twin_database'

storage = MySQLStorage(mysql_host, mysql_password, mysql_user, mysql_database)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/sensor", response_model=List[SensorInfo])
async def get_sensors(active: bool = Query(None, description="Filter sensors by their active state")) \
        -> List[SensorInfo]:
    return storage.get_sensors_info(active)


@app.get("/measurement_source")
async def get_measurement_sources() -> List[MeasurementSourceInfo]:
    return storage.get_measurement_sources()


@app.post("/measurement_source")
async def add_measurement_source(source: MeasurementSourceInfo):
    storage.add_measurement_source(source)


@app.get("/sensor_model")
async def get_sensor_models() -> List[SensorModelInfo]:
    return storage.get_sensors_models()


@app.post("/sensor_model")
async def add_sensor_model(model: SensorModelInfo):
    storage.add_sensor_model(model)


@app.patch("/sensors/{sensor_item_id}/enable")
async def enable_sensor(sensor_item_id: int):
    pass


@app.patch("/sensors/{sensor_item_id}/disable")
async def disable_sensor(sensor_item_id: int):
    pass


@app.post("/sensor")
async def add_sensor(sensor: SensorInfo):
    storage.add_sensor(sensor)


@app.post("/measurement")
async def add_measurement(request: MeasurementsInfo):
    for measurement in request.insert_values:
        storage.add_measurement(measurement, request.query_id, request.insert_ts)


@app.get("/measurements")  # add parameters like timedelta or smth and ids list
async def get_measurements():
    pass
