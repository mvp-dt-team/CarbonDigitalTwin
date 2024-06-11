from fastapi import APIRouter, Query, HTTPException, UploadFile, File, Form
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
)
from data_storage.mysql_storage import MySQLStorage
from mysql.connector import IntegrityError

import os

UPLOAD_FOLDER = "uploads"


def blocks_router(storage: MySQLStorage):
    router = APIRouter(
        tags=["Работа с блоками"],
    )

    @router.get("/", response_model=List[BlockModelGet])
    async def get_block_list(need_active: bool):
        return storage.get_block_list(need_active)

    # @router.get("/{block_id}", response_model=BlockModelGet)
    # async def get_block(block_id: int):
    #     return storage.get_block(block_id)

    # @router.patch("/{block_id}")
    # async def toggle_block(block_id: int):
    #     return storage.toggle_block(block_id)

    @router.post("/")
    async def add_block(block_data: BlockModelPost):
        storage.add_block(block_data)

    # @router.get("/models", response_model=List[MLModelGet])
    # async def get_model_list():
    #     return storage.get_model_list()

    # @router.get("/models/{model_id}")
    # async def get_model(model_id: int):
    #     return storage.get_model(model_id)

    # @router.post("/models")
    # async def add_model(file: UploadFile = File(...), data: AttachmentGet = Body(...)):
    #     print(file)
    #     if not data.name:
    #         raise HTTPException(status_code=400, detail="Name is required.")
    #     content = await file.read()
    #     storage.add_model(data, content=content)

    # @router.get("/prediction")
    # async def get_predictions(block_ids: Annotated[list[int], Query()] = []) -> List[PredictionGet]:
    #     if len(block_ids) == 0:
    #         raise HTTPException(status_code=400, detail="Indicate the blocks")
    #     return storage.get_predictions(block_ids)

    # @router.post("/")
    # async def add_prediction(request: PredictionPost):
    #     for prediction in request.insert_values:
    #         try:
    #             storage.add_prediction(prediction, request.insert_ts)
    #         except IntegrityError as e:
    #             if "Duplicate entry" in str(e):
    #                 raise HTTPException(status_code=400, detail="Duplicate entry error. The data might already exist.")
    #             else:
    #                 raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    # @router.get("/attachments")
    # async def get_attachments(block_ids: Annotated[list[int], Query()] = []) -> List[AttachmentGet]:
    #     if len(block_ids) == 0:
    #         raise HTTPException(status_code=400, detail="Indicate the blocks")
    #     return storage.get_attachments(block_ids)

    # @router.get("/attachments/{attachment_id}")
    # async def get_attachment(attachment_id: int):
    #     return storage.get_attachment(attachment_id)

    # @router.post("/")
    # async def add_attachments(request: AttachmentPost):
    #     for attachment in request.insert_values:
    #         try:
    #             storage.add_attachments(attachment)
    #         except IntegrityError as e:
    #             if "Duplicate entry" in str(e):
    #                 raise HTTPException(status_code=400, detail="Duplicate entry error. The data might already exist.")
    #             else:
    #                 raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    @router.post("/property")
    async def add_property(property_data: PropertyPost):
        storage.add_property(property_data)

    @router.get("/property", response_model=List[PropertyGet])
    async def get_properties():
        return storage.get_properties()

    # @router.post("/models")
    # async def upload_file(description: str = Query(...), file: UploadFile = File(...)):
    #     file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    #     with open(file_location, "wb+") as file_object:
    #         file_object.write(file.file.read())

    #     new_id = storage.add_file(description, file_location)

    #     return {"id": new_id, "filename": file.filename, "description": description}

    # @router.post("/models")
    # async def upload_model(name: str = Query(...), description: str = Query(...), type_model: str = Query(...), block_id: int = Query(...), file: UploadFile = File(...)):
    #     file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    #     with open(file_location, "wb+") as file_object:
    #         file_object.write(file.file.read())

    #     new_id = storage.add_model(name, description, type_model, block_id, file_location)

    #     return {"id": new_id, "filename": file.filename,"name": name, "description": description, "type": type_model, "block": block_id}

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
            file_object.write(file.file.read())

        new_id = storage.add_block_params(
            model_params={
                "name": name,
                "description": description,
                "type_model": type_model,
                "block_id": block_id,
                "file_path": file_location,
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
