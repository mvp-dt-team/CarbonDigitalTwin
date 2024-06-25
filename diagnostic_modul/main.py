from classes import Model, Block, Sensor, Handler, RandomForestModel, Camera, YOLOModel
from typing import List, Dict, Union
import requests
import json
import os

from config_reader import config

"""
RESUME
"""
URL = config.SMADDRESS

models_folder = "./diagnostic_modul/uploads"

if not os.path.exists(models_folder):
    os.makedirs(models_folder)

blocks_data = requests.get(f"{URL}/blocks?need_active=true")


def find_sensors_with_measurements(block_data):
    sensors_data = requests.get(f"{URL}/sensor?need_active=true").json()

    # Создаем словарь для быстрого доступа к датчикам по их id
    sensor_dict = {sensor["id"]: sensor for sensor in sensors_data}

    # Инициализируем список для хранения результатов
    result = []

    # Итерируемся по датчикам в данных блока
    for sensor in block_data.get("sensors", []):
        sensor_item_id = sensor.get("sensor_item_id")
        measurement_source_id = sensor.get("measurement_source_id")

        # Ищем датчик по sensor_item_id и measurement_source_id
        for sensor_id, sensor_info in sensor_dict.items():
            for prop in sensor_info["properties"]:
                if (
                    prop["measurement_source_id"] == measurement_source_id
                    and sensor_id == sensor_item_id
                ):
                    result.append(
                        {
                            "id": sensor_id,
                            "measurement_source_id": measurement_source_id,
                            "name": prop["name"],
                            "description": sensor_info["description"],
                            "unit": prop["unit"],
                            "type": sensor_info["type"],
                            "parameters": sensor_info["parameters"],
                        }
                    )

    return result


# Загрузка всех датчиков
sensors = []
model = None
blocks = []
print(f"len = {len(blocks_data.json())}")
for block in blocks_data.json():
    block_data = {}
    block_data["block_id"] = block["id"]
    block_data["sensors"] = []
    block_data["model"] = None

    sensors_in_block = [sensor for sensor in find_sensors_with_measurements(block)]

    for sensor in sensors_in_block:
        if sensor["type"] == "camera":
            block_data["sensors"].append(
                Camera(
                    id=sensor["id"],
                    description=sensor["description"],
                    address=sensor["parameters"]["address"],
                )
            )
        else:
            block_data["sensors"].append(
                Sensor(
                    id=sensor["id"],
                    measurement_source_id=sensor["measurement_source_id"],
                    type_sensor=sensor["type"],
                    name=sensor["name"],
                    unit=sensor["unit"],
                    description=sensor["description"],
                )
            )

    response = requests.get(f"{URL}/blocks/models/{block['model']['id']}")
    if response.status_code == 200:
        filename = response.headers.get("Content-Disposition").split("%5C")[-1]
        file_path = os.path.join(models_folder, filename)
        if os.path.exists(file_path):
            base, ext = os.path.splitext(filename)
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

        # TODO поменять, чтобы в зависимости от типа модели включался нужный класс модели
        if block["model"]["id"] == 12:
            block_data["model"] = YOLOModel(
                id=block["model"]["id"],
                name=block["model"]["name"],
                description=block["model"]["description"],
                model_path=file_path,
                property_names=block["properties"],
            )
        else:
            block_data["model"] = RandomForestModel(
                id=block["model"]["id"],
                name=block["model"]["name"],
                description=block["model"]["description"],
                model_path=file_path,
                property_names=block["properties"],
            )
    print(len(block_data["sensors"]))
    blocks.append(block_data)

test_handler = Handler(polling_interval=2, url=URL)
for block in blocks:
    test_handler.add_block(block["block_id"], block["model"], block["sensors"])
test_handler.action()
