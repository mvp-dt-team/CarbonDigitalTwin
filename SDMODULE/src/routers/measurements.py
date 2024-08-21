from http.client import HTTPException
from mysql.connector import IntegrityError

from fastapi import APIRouter, Query, HTTPException
from typing import List, Annotated

from src.network_models.measurements_info import MeasurementsGet, MeasurementsPost
from src.mysql_storage import MySQLStorage


def get_measurements_router(storage: MySQLStorage):
    router = APIRouter(
        tags=["Измерения"],
    )

    @router.post("/")
    async def add_measurement(request: MeasurementsPost):
        for measurement in request.insert_values:
            try:
                await storage.add_measurement(
                    measurement, request.insert_ts, request.query_uuid
                )
            except IntegrityError as e:
                if "Duplicate entry" in str(e):
                    raise HTTPException(
                        status_code=400,
                        detail="Duplicate entry error. The data might already exist.",
                    )
                else:
                    raise HTTPException(
                        status_code=500, detail="An unexpected error occurred."
                    )

    @router.get("/")
    async def get_measurements(
        measurement_source_ids: Annotated[list[int], Query()] = []
    ) -> List[MeasurementsGet]:
        if len(measurement_source_ids) == 0:
            raise HTTPException(status_code=400, detail="Indicate the sources")
        return await storage.get_last_three_measurements_for_sources(
            measurement_source_ids
        )

    return router
