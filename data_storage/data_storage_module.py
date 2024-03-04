from typing import List
from fastapi import FastAPI

from data_storage.mysql_storage import MySQLStorage
from network_models.active_sensors_response import ActiveSensorsResponseItem

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
async def read_item() -> List[ActiveSensorsResponseItem]:
    sensors = storage.get_sensors_info()
    return sensors
