from fastapi import APIRouter
from typing import List
from network_models.sensor_model_info import SensorModelInfo
from data_storage.mysql_storage import MySQLStorage

def get_sensor_models_router(storage: MySQLStorage):
    router = APIRouter(
        tags=["Модели датчиков"],
    )

    @router.get("/", response_model=List[SensorModelInfo])
    async def get_sensor_models():
        return storage.get_sensors_models()

    @router.post("/")
    async def add_sensor_model(model: SensorModelInfo):
        storage.add_sensor_model(model)

    return router
