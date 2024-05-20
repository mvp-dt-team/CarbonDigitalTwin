"""
Сервер для работы с БД. Содержит API запросы для выполнения операций с БД
"""

from datetime import time
from typing import List, Annotated
from fastapi import FastAPI, Query, HTTPException
from mysql.connector import IntegrityError

from data_storage.mysql_storage import MySQLStorage
from network_models.measurement_source_info import MeasurementSourceInfo
from network_models.sensor_model_info import SensorModelInfo
from network_models.sensors_info import SensorInfo
from network_models.measurements_info import MeasurementsInfo, Measurement
from config import config

# Настройки MySQL
mysql_host = config.url
mysql_user = config.login.get_secret_value()
mysql_password = config.password.get_secret_value()
mysql_database = config.db_name

storage = MySQLStorage(mysql_host, mysql_password, mysql_user, mysql_database)

app = FastAPI()

print(storage)

@app.get("/measurement_source")
async def get_measurement_sources() -> List[MeasurementSourceInfo]:
    """
    Получение источников измерения
    """
    return storage.get_measurement_sources()


@app.post("/measurement_source")
async def add_measurement_source(source: MeasurementSourceInfo):
    """
    Добавление источников измерения
    """
    storage.add_measurement_source(source)


@app.get("/sensor", response_model=List[SensorInfo])
async def get_sensors(active: bool = Query(None, description="Filter sensors by their active state")) \
        -> List[SensorInfo]:
    """
    Получение активных объектов датчиков
    """
    return storage.get_sensors_info(active)

@app.post("/sensor")
async def add_sensor(sensor: SensorInfo):
    """
    Добавление объектов датчиков в БД
    """
    storage.add_sensor(sensor)


@app.get("/sensor_model")
async def get_sensor_models() -> List[SensorModelInfo]:
    """
    Получение типов датчиков, зарегистрированных в БД (таблица Sensor)
    """
    return storage.get_sensors_models()


@app.post("/sensor_model")
async def add_sensor_model(model: SensorModelInfo):
    """
    Добавление типов датчиков (таблица Sensor)
    """
    storage.add_sensor_model(model)


@app.patch("/sensors/{sensor_item_id}/enable")
async def enable_sensor(sensor_item_id: int):
    """
    Переключение статуса объекта датчика на "Активный"
    """
    storage.toggle_sensor_activation(sensor_item_id, True)


@app.patch("/sensors/{sensor_item_id}/disable")
async def disable_sensor(sensor_item_id: int):
    """
    Переключение статуса объекта датчика на "Неактивный"
    """
    storage.toggle_sensor_activation(sensor_item_id, False)


@app.post("/measurement")
async def add_measurement(request: MeasurementsInfo):
    """
    Добавление измерения
    """
    for measurement in request.insert_values:
        try:
            storage.add_measurement(measurement, request.query_id, request.insert_ts)
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                raise HTTPException(status_code=400, detail="Duplicate entry error. The data might already exist.")
            else:
                raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@app.get("/measurement")
async def get_measurements(measurement_source_ids: Annotated[list[int], Query()] = []) -> List[Measurement]:
    """
    Получения измерений
    """
    if len(measurement_source_ids) == 0:
        raise HTTPException(status_code=400, detail="Indicate the sources")
    return storage.get_last_three_measurements_for_sources(measurement_source_ids)


# Проверка запуска как основного скрипта
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)