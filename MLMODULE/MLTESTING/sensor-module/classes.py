from queue import Queue
from torch import Tensor
from typing import Union, List
from enum import Enum
import numpy as np
import cv2
import datetime
from PIL import Image
from ultralytics import YOLO
from threading import Thread
import time
import sqlite3
import sys
import logging

import json
import random
import requests
import io


WEIGHTS_DEFECTS = {
    0: 0.05,
}
MAX_RESULT = 1.0


class Handler:
    def __init__(self, url):
        self.sources: List[Source] = []
        self.models = []
        self.queue = Queue()
        self.source_model_mapping = {}
        self.polling_interval = 10
        self.running = True
        self.logger = logging.getLogger("Submodule")
        self.logger.setLevel(logging.DEBUG)
        self.url = url
        self.frequency_archivating = 5

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.info("Инициализация обработчика")

    def add_source_model_mapping(self, source, model) -> None:
        if type(source) is Source and type(model) is Model:
            self.sources.append(source)
            self.models.append(model)
            self.source_model_mapping[source.id] = model
        else:
            raise Exception("Модель или источник некорректны")

    def polling_sensors(self) -> dict:
        data = {}
        for source in self.sources:
            self.logger.debug(f"Получаю данные с камеры {source.id}")
            data[source.id] = source.get_value()
        return data

    def value_predict(self, source_id: int, source_value: Image) -> dict:
        model = self.source_model_mapping.get(source_id)
        if model:
            result = model.predict(source_value)
            return {source_id: result}
        else:
            return {}

    # endpoint: curl -X POST http://storage-module-address/camera/123 -H "Content-Type: application/json" -d '{"value": 12.34}
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

    # endpoint: curl -X POST http://storage-module-address/camera/123/archivate -F "image=@/path/to/your/image.jpg"
    def archiving_images(self, source_id: int, image: Image) -> int:
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

    def run(self) -> None:
        count = 0
        try:
            while self.running:
                data = self.polling_sensors()
                self.queue.put(data)
                if not self.queue.empty():
                    data = self.queue.get()

                    for source_id, source_value in data.items():
                        model_result = self.value_predict(source_id, source_value)
                        if model_result:
                            defects = []
                            for r in model_result[source_id]:
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
                count += 1
                if count > self.frequency_archivating:
                    count = 0
                time.sleep(self.polling_interval)
        except Exception as e:
            self.logger.error(f"Error in run: {e}")
            sys.exit(1)

    def stop(self) -> None:
        self.running = False


class Source:
    def __init__(self, id, description, address):
        self.id = id
        self.description = description
        self.address = address

    def get_value(self) -> Image:
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
    def __init__(self, path: str):
        self.path = path

    def predict(self, frame: Image) -> Tensor:
        model = YOLO(self.path)
        results = model(frame, verbose=False)
        return results
