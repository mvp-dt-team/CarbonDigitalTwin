from queue import Queue
from torch import Tensor
from typing import Union
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
import random

logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

# class TypingSource(Enum):
#     VIDEO = 0
#     OTHER = 1

def create_database():
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_version TEXT NOT NULL,
                prediction TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()
        print("Database created successfully.")
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

    return True

class Handler:
    def __init__(self):
        self.sources = []
        self.models = []
        self.queue = Queue()
        self.source_model_mapping = {}
        self.polling_interval = 10
        logger.info('Инициализация обработчика')


    def add_source_model_mapping(self, source, model):
        self.sources.append(source)
        self.models.append(model)
        self.source_model_mapping[source.id] = model

    def polling_sensors(self) -> int:
        data = {}
        for source in self.sources:
            logger.debug(f'Получаю данные с камеры {source.id}')
            data[source.id] = source.get_value()
        return data

    def polling_sensors_async(self) -> None:
        try:
            while True:
                logger.info('Опрос камеры')
                data = self.polling_sensors()
                self.queue.put(data)
                logger.debug(self.queue.empty())
                time.sleep(self.polling_interval)
        except Exception as e:
            print(f"Error in polling_sensors_async: {e}")
            sys.exit(1)

    def value_predict(self, source_id: int, source_value: Image) -> dict:
        model = self.source_model_mapping.get(source_id)
        if model:
            result = model.predict(source_value)
            return {model.version: result}
        else:
            return {}

    # Пока записываем в тестовую
    def write_db_request(self, value_list: list) -> int:
        try:
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()

            for model_version, prediction in value_list:
                cursor.execute('''
                    INSERT INTO predictions (model_version, prediction) VALUES (?, ?)
                ''', (model_version, prediction))

            conn.commit()
            conn.close()
            return len(value_list)
        except Exception as e:
            print(f"Error writing to database: {e}")
            return 0

    def run(self) -> None:
        try:
            poll_thread = Thread(target=self.polling_sensors_async)
            poll_thread.start()

            while True:
                if not self.queue.empty():
                    logger.info("Обрабатываем модель")
                    data = self.queue.get()
                    for source_id, source_value in data.items():
                        model_result = self.value_predict(source_id, source_value)
                        if model_result:
                            # self.write_db_request(list(model_result.values()))
                            logger.info(model_result)
                            
        except Exception as e:
            logger.error(f"Error in run: {e}")
            # sys.exit(1)

class Source:
    def __init__(self, id, unit, number, address):
        self.id = id
        self.unit = unit
        self.number = number
        self.address = address

    def get_value(self) -> Image:
        logger.debug(f'Обращение к камере {self.id}')
        cap = cv2.VideoCapture(self.address)
        if not cap.isOpened():
            logger.debug('Нет доступа к камере')
            exit()

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        random_frame_index = random.randint(0, total_frames - 1)
        cap.set(cv2.CAP_PROP_POS_FRAMES, random_frame_index)

        ret, frame = cap.read()
        data = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        cap.release()
        logger.info(data)
        return data

class Model:
    def __init__(self, version: str, path: str):
        self.version = version
        self.path = path
    
    def predict(self, frame: Image) -> Tensor:
        model = YOLO(self.path)
        results = model(frame)
        return results