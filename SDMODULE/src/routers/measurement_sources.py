from fastapi import APIRouter
from typing import List
from src.network_models.measurement_source_info import (
    MeasurementSourceInfoGet,
    MeasurementSourceInfoPost,
)
from src.mysql_storage import MySQLStorage


def get_measurement_sources_router(storage: MySQLStorage):
    router = APIRouter(
        tags=["Источники данных"],
    )

    @router.get("/", response_model=List[MeasurementSourceInfoGet])
    async def get_measurement_sources():
        return await storage.get_measurement_sources()

    @router.post("/")
    async def add_measurement_source(source: MeasurementSourceInfoPost):
        await storage.add_measurement_source(source)

    return router
