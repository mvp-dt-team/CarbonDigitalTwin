from typing import List, Dict, Union
import logging
import random
from datetime import datetime, timezone
import time
import requests
import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import json
import warnings
from sklearn.exceptions import DataConversionWarning
from PIL import Image
from queue import Queue
from torch import Tensor
import cv2
from ultralytics import YOLO
from threading import Thread
import io

warnings.filterwarnings(action="ignore", category=UserWarning)

WEIGHTS_DEFECTS = {0: 0.05}
MAX_RESULT = 1.0

URLS = {
    "GET_SENSORS": "",
    "POST_PREDICTION": "",
}


class Sensor:
    def __init__(
        self,
        id: int,
        measurement_source_id: int,
        type_sensor: str,
        name: str,
        unit: int,
        description: str,
    ):
        self.type_sensor = type_sensor
        self.id = id
        self.measurement_source_id = measurement_source_id
        self.name = name
        self.unit = unit
        self.description = description

    def __repr__(self) -> str:
        return self.name


class Camera:
    def __init__(self, id: int, description: str, address: str):
        self.id = id
        self.description = description
        self.address = address

    def get_value(self) -> Image.Image:
        cap = cv2.VideoCapture(self.address)
        if not cap.isOpened():
            raise Exception("Не удалось получить данные с источника")

        # Заглушка временная, необходимо убрать перед настоящей съемкой TODO !
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        random_frame_index = random.randint(0, total_frames - 1)
        cap.set(cv2.CAP_PROP_POS_FRAMES, random_frame_index)
        #####################

        ret, frame = cap.read()
        data = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        cap.release()
        return data


class Model:
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        model_path: str,
        params: Dict = None,
        version: str = None,
        property_names: List[str] = None,
    ):
        self.model_path = model_path
        self.params = params
        self.property_names = property_names
        self.id = id
        self.name = name

    def predict(self, X) -> Dict[str, float]:
        pass

    def __repr__(self) -> str:
        return self.name


class RandomForestModel(Model):
    def __init__(
        self,
        model_path: str,
        property_names: List[str],
        id: int,
        name: str,
        description: str,
        params: Dict = None,
        version: str = None,
    ):
        super().__init__(
            description=description,
            model_path=model_path,
            params=params,
            version=version,
            property_names=property_names,
            id=id,
            name=name,
        )
        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)

    def predict(self, X) -> dict:
        result = self.model.predict(np.array(X).reshape(1, -1)).tolist()
        return [
            {"m_data": result[x], "property_id": self.property_names[x]["id"]}
            for x in range(len(self.property_names))
        ]


class YOLOModel(Model):
    def __init__(
        self,
        model_path: str,
        property_names: List[str],
        id: int,
        name: str,
        description: str,
        params: Dict = None,
        version: str = None,
    ):
        super().__init__(
            description=description,
            model_path=model_path,
            params=params,
            version=version,
            property_names=property_names,
            id=id,
            name=name,
        )
        self.model = YOLO(self.model_path, verbose=False)

    # TODO Пока нет методики обработки изображений
    def preprocessing(self, data) -> list:
        results = []
        for _ in self.property_names:
            results.append(random.random())
        return results

    def predict(self, frame: Image.Image) -> dict:
        labeling = self.model.predict(frame, verbose=False)
        results = self.preprocessing(labeling)
        return [
            {"m_data": results[x], "property_id": self.property_names[x]["id"]}
            for x in range(len(self.property_names))
        ]


class Block:
    def __init__(
        self,
        id: int,
        model: Model,
        sensors: Union[List[Sensor], List[Camera]],
        logger: logging.Logger,
    ):
        self.id = id
        self.model = model
        self.sensors = sensors
        self.logger = logger

    def poll_sensors(self, url) -> Union[List[float], int, Dict[int, Image.Image]]:
        if isinstance(self.sensors[0], Sensor):  # Если просто датчик
            measurements = []
            for sensor in self.sensors:
                measurements.append(sensor.measurement_source_id)
            try:
                response = requests.get(
                    url=f"{url}/measurement?"
                    + "&".join(
                        ["measurement_source_ids=" + str(x) for x in measurements]
                    )
                )
                if response.ok:
                    # TODO
                    def parse_date(date_str):
                        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

                    latest_measurements = {}

                    for entry in response.json():
                        ms_id = entry["measurement_source_id"]
                        ts = parse_date(entry["insert_ts"])

                        if ms_id not in latest_measurements or ts > parse_date(
                            latest_measurements[ms_id]["insert_ts"]
                        ):
                            latest_measurements[ms_id] = entry

                    latest_measurements_list = list(latest_measurements.values())

                    return latest_measurements_list
                else:
                    raise Exception(f"{response.status_code} {response.reason}")
            except Exception as e:
                self.logger.error(f"Ошибка опроса датчиков: {e}")
                return 1
        elif isinstance(self.sensors[0], Camera):  # Если камера
            data: Image.Image
            for source in self.sensors:
                self.logger.debug(f"Получаю данные с камеры {source.id}")
                data = source.get_value()
            return data

    def get_list_sensors_id(self) -> list:
        return [x.id for x in self.sensors]


class Handler:
    def __init__(self, polling_interval: int, url: str, frequency_archivating: int = 5):
        self.status = 0
        self.logger = logging.getLogger("MLModule")
        self.logger.setLevel(logging.INFO)
        self.blocks: List[Block] = []
        self.polling_interval: int = polling_interval
        self.running = True
        self.url = url
        self.frequency_archivating: int = frequency_archivating
        self.queue = Queue()

        # Настройка консольного логгера
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.info("Инициализация обработчика")

    def add_block(
        self, id: int, model: Model, sensors: Union[List[Sensor], List[Camera]]
    ) -> int:
        block = Block(id, model, sensors, self.logger)
        self.blocks.append(block)
        return 0

    def write_db_data(self, data: list) -> int:
        try:
            current_time = datetime.now(timezone.utc)

            response = requests.post(
                url=f"{self.url}/blocks/prediction",
                json={
                    "insert_ts": current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
                    + "Z",
                    "insert_values": data,
                },
            )
            if response.ok:
                return 0
            else:
                raise Exception(f"{response.status_code}")
        except Exception as e:
            self.logger.error(f"Ошибка при записи в БД: {e}")
            return 1

    # TODO Функцию необходимо исправить, а для этого нужно создать эндпоинт и изменить таблицу в БД
    def archiving_images(self, source_id: int, image: Image.Image) -> int:
        try:
            image_buffer = io.BytesIO()
            image.save(image_buffer, format="JPEG")
            image_buffer.seek(0)
            files = {"image": ("image.jpg", image_buffer, "image/jpeg")}
            response = requests.post(
                url=f"http://{self.url}/camera/{source_id}/archivate", files=files
            )

            if response.ok:
                self.logger.info("Изображение успешно отправлено.")
                return 0
            else:
                raise Exception(
                    f"Ошибка передачи изображения в БД: {response.content}  {response.status_code}"
                )
        except Exception as e:
            self.logger.error(f"{e}")
            return 1

    # TODO Переделать отправку данных, для отправки пакета данных по всем блокам, а не делать милион запросов для отправки каждого предсказания
    def action(self):
        self.logger.info("Модуль начал работать")
        try:
            while self.running:
                data_packet = []
                for block in self.blocks:
                    self.logger.info("Опрос датчиков")
                    data = block.poll_sensors(self.url)
                    self.logger.info("Передача данных модели")
                    if isinstance(
                        data, int
                    ):  # Если целое число, то это какая-то ошибка
                        self.running = False
                        raise Exception("Не удалось опросить датчики")
                    elif isinstance(
                        data, list
                    ):  # Если список, то это полученные значения с простых датчиков

                        predict_value = block.model.predict(
                            [float(x["m_data"]) for x in data]
                        )
                    elif isinstance(
                        data, Image.Image
                    ):  # Если словарь, то это данные изображения с источником TODO пока эта часть полностью не рабочая
                        predict_value = block.model.predict(data)

                    for value in predict_value:
                        value["block_id"] = block.id
                        data_packet.append(value)
                        # self.logger.debug(f"X: {data}, y: {value}")

                for result in data_packet:
                    if not isinstance(result, dict):
                        self.running = False
                        raise Exception("Ошибка при обработке данных моделью")

                self.logger.info("Отправка данных на сервер")
                self.write_db_data(data=data_packet)

                time.sleep(self.polling_interval)
        except Exception as exc:
            self.logger.error(f"{exc}")

    def stop(self) -> None:
        self.running = False
