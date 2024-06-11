from typing import List, Dict, Union
import logging
import random
from datetime import datetime
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
        model_path: str,
        params: Dict = None,
        version: str = None,
        property_names: List[str] = None,
    ):
        self.model_path = model_path
        self.params = params
        self.property_names = property_names

    def predict(self, X) -> Dict[str, float]:
        pass


class RandomForestModel(Model):
    def __init__(
        self, model_path: str, params: Dict, version: str, property_names: List[str]
    ):
        super().__init__(model_path, params, version, property_names)
        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)

    def predict(self, X) -> Dict[str, float]:
        result = self.model.predict(np.array(X).reshape(1, -1))
        return {"property_names": self.property_names, "values": result.tolist()}


class YOLOModel(Model):
    def __init__(self, model_path: str):
        super().__init__(model_path)
        self.model = YOLO(self.model_path)

    def predict(self, frame: Image.Image) -> Tensor:
        results = self.model(frame, verbose=False)
        return results


class Block:
    def __init__(
        self,
        model: Model,
        sensors: Union[List[Sensor], List[Camera]],
        logger: logging.Logger,
    ):
        self.model = model
        self.sensors = sensors
        self.logger = logger

    def poll_sensors(self, url) -> Union[List[float], int, Dict[int, Image.Image]]:
        if isinstance(self.sensors[0], Sensor):  # Если просто датчик
            measurements = []
            for sensor in self.sensors:
                measurements.append(
                    {
                        "sensor_id": sensor.id,
                        "measurement_source_id": sensor.measurement_source_id,
                        "time_from": "2001-03-26T00:00:00Z",
                        "time_to": datetime.utcnow().replace(microsecond=0).isoformat()
                        + "Z",
                    }
                )
            try:
                response = requests.post(
                    url=f"http://{url}/measurements",
                    json={"measurements": measurements},
                )
                if response.ok:
                    return [x["data"][-1] for x in json.loads(response.content)]
                else:
                    raise Exception(f"{response.status_code} {response.reason}")
            except Exception as e:
                self.logger.error(f"Ошибка опроса датчиков: {e}")
                return 1
        elif isinstance(self.sensors[0], Camera):  # Если камера
            data = {}
            for source in self.sensors:
                self.logger.debug(f"Получаю данные с камеры {source.id}")
                data[source.id] = source.get_value()
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
        self, model: Model, sensors: Union[List[Sensor], List[Camera]]
    ) -> int:
        block = Block(model, sensors, self.logger)
        self.blocks.append(block)
        return 0

    def write_db_data(self, data: Dict[str, float], sensors: List[int]) -> int:
        try:
            response = requests.post(
                url=f"http://{self.url}/save_prediction_data",
                json={
                    "sources": sensors,
                    "property_names": data["property_names"],
                    "values": data["values"],
                },
            )
            if response.ok:
                return 0
            else:
                raise Exception(f"{response.status_code}")
        except Exception as e:
            self.logger.error(f"Ошибка при записи в БД: {e}")
            return 1

    def write_db_request(self, source_id: int, prediction: float) -> int:
        try:
            response = requests.post(
                url=f"http://{self.url}/camera/{source_id}",
                json={"value": str(prediction)},
            )
            if response.ok:
                return 0
            else:
                raise Exception(f"{response.status_code}")
        except Exception as e:
            self.logger.error(f"Ошибка передачи значений в БД: {e}")
            return 1

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

    def processing_values(self, defects: List[dict]) -> float:
        if len(defects) == 0:
            return MAX_RESULT
        else:
            return np.mean(
                [WEIGHTS_DEFECTS[x["class_"]] * x["confidence_"] for x in defects]
            )

    def action(self):
        self.logger.info("Модуль начал работать")
        try:
            while self.running:
                for block in self.blocks:
                    self.logger.info("Опрос датчиков")
                    data = block.poll_sensors(self.url)

                    if isinstance(data, int):
                        self.running = False
                        raise Exception("Не удалось опросить датчики")
                    elif isinstance(data, list):
                        self.logger.info("Передача данных модели")
                        predict_value = block.model.predict(data)
                        self.logger.debug(f"X: {data}, y: {predict_value}")

                        if isinstance(predict_value, dict):
                            self.logger.info("Отправка данных на сервер")
                            self.write_db_data(
                                predict_value, sensors=block.get_list_sensors_id()
                            )
                        else:
                            self.running = False
                            raise Exception("Ошибка при обработке данных моделью")
                    elif isinstance(data, dict):
                        self.queue.put(data)
                        if not self.queue.empty():
                            data = self.queue.get()

                            for source_id, source_value in data.items():
                                model_result = block.model.predict(source_value)
                                if model_result:
                                    defects = []
                                    for r in model_result:
                                        for b in r.boxes:
                                            defects.append(
                                                {
                                                    "class_": int(b.cls),
                                                    "confidence_": float(b.conf),
                                                }
                                            )
                                    self.write_db_request(
                                        source_id, self.processing_values(defects)
                                    )
                                    if count % self.frequency_archivating == 0:
                                        self.archiving_images(
                                            source_id=source_id, image=source_value
                                        )
                time.sleep(self.polling_interval)
        except Exception as exc:
            self.logger.error(f"{exc}")

    def stop(self) -> None:
        self.running = False
