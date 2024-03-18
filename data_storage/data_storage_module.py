from datetime import time
from typing import List
from fastapi import FastAPI

from data_storage.mysql_storage import MySQLStorage
from network_models.active_sensors_response import ActiveSensorsResponseItem
from network_models.insert_measurement_request import InsertMeasurementsRequest

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


@app.get("/active_sensors", response_model=List[ActiveSensorsResponseItem])
async def get_active_sensors() -> List[ActiveSensorsResponseItem]:
    sensors = storage.get_sensors_info()
    return sensors


@app.get("/sensors")
async def get_sensors():
    pass


@app.get("/measurement_sources")
async def get_measurement_sources():  # -> List[]:
    pass


@app.get("/sensor_models")
async def get_sensor_models():
    pass


@app.patch("/sensors/{sensor_item_id}/enable")
async def enable_sensor(sensor_item_id: int):
    pass


@app.patch("/sensors/{sensor_item_id}/disable")
async def disable_sensor(sensor_item_id: int):
    pass


@app.post("/sensors/")
async def add_sensor():
    pass


@app.post("/measurements/")
async def add_measurement(request: InsertMeasurementsRequest):
    insert_time = time.fromisoformat(request.insert_ts)
    for measurement in request.insert_values:
        storage.add_measurement(measurement, request.query_id, insert_time)


@app.get("/measurements")  # add parameters like timedelta or smth and ids list
async def get_measurements():
    pass
