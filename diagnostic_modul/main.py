from classes import Model, Block, Sensor, Handler, RandomForestModel, Camera
from typing import List, Dict, Union
import requests
import json
import os

from config_reader import config

"""
Сейчас для теста сделан только один блок, поэтому датчики и модель загружаются в единые переменные
"""
URL = config.SMADDRESS

models_folder = "./diagnostic_modul/uploads"

if not os.path.exists(models_folder):
    os.makedirs(models_folder)

blocks = requests.get(f"{URL}/blocks?need_active=true")

# Загрузка всех датчиков
sensors = []
model = None

for block in blocks.json():
    block_id = block["id"]

    sensors_in_block = {
        x["sensor_item_id"]: x["measurement_source_id"] for x in block["sensors"]
    }
    sensors_data = requests.get(f"{URL}/sensor?need_active=true").json()

    for sensor in sensors_data:
        if sensor["id"] in sensors_in_block:
            if sensor["type"] == "camera":
                sensors.append(
                    Camera(
                        id=sensor["id"],
                        description=sensor["description"],
                        address=sensor["parameters"]["address"],
                    )
                )
            else:
                measurement_source = next(
                    prop
                    for prop in sensor["properties"]
                    if prop["measurement_source_id"] == sensors_in_block[sensor["id"]]
                )
                sensors.append(
                    Sensor(
                        id=sensor["id"],
                        measurement_source_id=sensors_in_block[sensor["id"]],
                        type_sensor=sensor["type"],
                        name=measurement_source["name"],
                        unit=measurement_source["unit"],
                        description=sensor["description"],
                    )
                )

    response = requests.get(f"{URL}/blocks/models/{block['model']['id']}")
    if response.status_code == 200:
        filename = response.headers.get("Content-Disposition").split("%5C")[-1]
        file_path = os.path.join(models_folder, filename)
        if os.path.exists(file_path):
            base, ext = os.path.splitext(filename)
            print(base, ext)
            counter = 1
            new_filename = f"{base}_{counter}{ext}"
            new_file_path = os.path.join(models_folder, new_filename)
            while os.path.exists(new_file_path):
                counter += 1
                new_filename = f"{base}_{counter}{ext}"
                new_file_path = os.path.join(models_folder, new_filename)
            file_path = new_file_path
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        model = RandomForestModel(
            id=block["model"]["id"],
            name=block["model"]["name"],
            description=block["model"]["description"],
            model_path=file_path,
            property_names=block["properties"],
        )

test_handler = Handler(polling_interval=2, url=URL)
test_handler.add_block(block_id, model, sensors)
test_handler.action()
