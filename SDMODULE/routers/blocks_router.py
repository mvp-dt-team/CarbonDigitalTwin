from fastapi import APIRouter, Query, HTTPException, UploadFile, File, Form
from starlette.responses import FileResponse
from typing import List, Annotated
from network_models.blocks import (
    AttachmentGet,
    AttachmentPost,
    PredictionGet,
    PredictionPost,
    MLModelGet,
    BlockModelGet,
    SensorBlockinfo,
    BlockModelPost,
    PropertyGet,
    PropertyPost,
    PredictionMassivePost,
)
from mysql_storage import MySQLStorage
from mysql.connector import IntegrityError

import os
import hashlib


UPLOAD_FOLDER = "uploads"


def blocks_router(storage: MySQLStorage):
    router = APIRouter(
        tags=["Работа с блоками"],
    )

    @router.get("/", response_model=List[BlockModelGet])
    async def get_block_list(need_active: bool):
        return storage.get_block_list(need_active)

    @router.patch("/{block_id}")
    async def toggle_block(block_id: int):
        response = storage.toggle_block(block_id)
        if response["status_code"] != 200:
            raise HTTPException(
                status_code=response["status_code"], detail=response["detail"]
            )
        return response

    @router.post("/")
    async def add_block(block_data: BlockModelPost):
        return storage.add_block(block_data)

    @router.get("/models/{model_id}")
    async def get_model(model_id: int):
        response = storage.get_model(model_id)
        if response["status_code"] != 200:
            raise HTTPException(
                status_code=response["status_code"], detail=response["detail"]
            )

        return FileResponse(
            status_code=response["status_code"],
            path=response["file_path"],
            filename=response["file_path"].split("/")[-1],
        )

    @router.get("/models/check/{model_id}")
    async def check_model(model_id: int):
        response = storage.check_model(model_id)
        if response["status_code"] != 200:
            raise HTTPException(
                status_code=response["status_code"], detail=response["detail"]
            )

        return response

    @router.get("/prediction")
    async def get_predictions(
        block_id: int = Query(...), n_predictions: int = Query(...)
    ) -> List[PredictionGet]:
        response = storage.get_predictions(block_id, n_predictions)
        if type(response) is dict and response.get("status_code") != 200:
            raise HTTPException(
                status_code=response["status_code"], detail=response["detail"]
            )
        return response

    @router.post("/prediction")
    async def add_prediction(request: PredictionMassivePost):

        for prediction in request.insert_values:
            try:
                storage.add_prediction(
                    prediction, request.insert_ts, request.query_uuid
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

    @router.post("/property")
    async def add_property(property_data: PropertyPost):
        return storage.add_property(property_data)

    @router.get("/property", response_model=List[PropertyGet])
    async def get_properties():
        return storage.get_properties()

    @router.post("/models/params")
    async def add_block_params(
        name: str = Form(...),
        description: str = Form(...),
        type_model: str = Form(...),
        block_id: int = Form(...),
        file: UploadFile = File(...),
        measurement_source_ids: Annotated[list[int], Query()] = [],
        sensor_item_ids: Annotated[list[int], Query()] = [],
        properties_ids: Annotated[list[int], Query()] = [],
    ):

        # TODO Добавить проверки на несуществующие датчики или неправильное сочетание точки измерения и sensor-item
        if (
            len(measurement_source_ids) != len(sensor_item_ids)
            or len(properties_ids) == 0
        ):
            raise HTTPException(400, "Data is incorrected")

        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb+") as file_object:
            reads = file.file.read()
            filehash = hashlib.sha256(reads)
            file_object.write(reads)

        new_id = storage.add_block_params(
            model_params={
                "name": name,
                "description": description,
                "type_model": type_model,
                "block_id": block_id,
                "file_path": file_location,
                "file_name": file.filename,
                "file_hash": filehash.hexdigest(),
            },
            sensors=[
                {
                    "measurement_source_id": measurement_source_ids[i],
                    "sensor_item_id": sensor_item_ids[i],
                }
                for i in range(len(measurement_source_ids))
            ],
            properties=properties_ids,
        )

        return {
            "id": new_id,
            "filename": file.filename,
            "name": name,
            "description": description,
            "type": type_model,
            "block": block_id,
        }

    return router
