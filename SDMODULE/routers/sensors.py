from fastapi import APIRouter, Query
from typing import List
from network_models.sensors_info import SensorInfoGet, SensorInfoPost
from mysql_storage import MySQLStorage


def get_sensors_router(storage: MySQLStorage):
    router = APIRouter(
        tags=["Работа с датчиками"],
    )

    @router.get("/", response_model=List[SensorInfoGet])
    async def get_sensors(
        need_active: bool = Query(
            None, description="Filter sensors by their active state"
        )
    ):
        return await storage.get_sensors_info(need_active)

    @router.post("/")
    async def add_sensor(sensor: SensorInfoPost):
        await storage.add_sensor(sensor)

    @router.patch("/{sensor_item_id}/enable")
    async def enable_sensor(sensor_item_id: int):
        await storage.toggle_sensor_activation(sensor_item_id, True)

    @router.patch("/{sensor_item_id}/disable")
    async def disable_sensor(sensor_item_id: int):
        await storage.toggle_sensor_activation(sensor_item_id, False)

    return router
