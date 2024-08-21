from fastapi import APIRouter
from typing import List
from src.network_models.sensor_model_info import SensorModelInfoGet, SensorModelInfoPost
from src.mysql_storage import MySQLStorage


def get_sensor_models_router(storage: MySQLStorage):
    router = APIRouter(
        tags=["Модели датчиков"],
    )

    @router.get("/", response_model=List[SensorModelInfoGet])
    async def get_sensor_models():
        return await storage.get_sensors_models()

    @router.post("/")
    async def add_sensor_model(model: SensorModelInfoPost):
        await storage.add_sensor_model(model)

    return router
