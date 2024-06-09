import os

from fastapi import FastAPI, UploadFile, File, Query
from fastapi.staticfiles import StaticFiles

from data_storage.mysql_storage import MySQLStorage
from data_storage.routers.measurement_sources import get_measurement_sources_router
from data_storage.routers.measurements import get_measurements_router
from data_storage.routers.sensor_models import get_sensor_models_router
from data_storage.routers.sensors import get_sensors_router

import logging
from config_reader import config

# Настройки MySQL
# mysql_host = 'localhost'
# mysql_user = 'digital_twin'
# mysql_password = 'digital_twin'
# mysql_database = 'digital_twin_database'

storage = MySQLStorage()

app = FastAPI()

UPLOAD_FOLDER = "uploads"

logging.basicConfig(level=logging.INFO, filename=config.STORAGE_LOG_FILENAME, encoding='utf8')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")


@app.post("/uploadfile/")
async def upload_file(description: str = Query(...), file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    new_id = storage.add_file(description, file_location)
    return {"id": new_id, "filename": file.filename, "description": description}


# Temporary Redirect возникает из-за префиксов роутера, возможно, они используются как-то неверно
app.include_router(get_measurement_sources_router(storage), prefix="/measurement_source")
app.include_router(get_measurements_router(storage), prefix="/measurement")
app.include_router(get_sensors_router(storage), prefix="/sensor")
app.include_router(get_sensor_models_router(storage), prefix="/sensor_model")
