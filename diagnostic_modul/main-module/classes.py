from typing import List, Dict, Union
import logging
import random
from enum import Enum
from datetime import datetime
import time
import sys

class TYPE_DATA(Enum):
    VALIDATION = 0
    TRAIN = 1

class STATUS(Enum):
    TRAIN = 0
    PREDICT = 1

# Заглушка
class Sensor:
    def __init__(self, id: int, type_sensor: str):
        self.type_sensor = type_sensor
        self.id = id

    def get_data(self):
        if self.type_sensor == 'VIDEO':
            return random.random()
        return random.random()

class Model:
    def __init__(self, model_path: str, params: dict, version: str):
        self.model_path = model_path
        self.params = params
        self.version = version
        self.status = 1  # Default to prediction status
        self.validation_dataset = []
        self.train_dataset = []

    def clear_datasets(self) -> None:
        self.validation_dataset = []
        self.train_dataset = []

    def append_dataset(self, data: any, type_data: int) -> int:
        if data is None:
            return 1
        if type_data == TYPE_DATA.TRAIN.value:
            self.train_dataset.append(data)
        elif type_data == TYPE_DATA.VALIDATION.value:
            self.validation_dataset.append(data)
        else:
            return 1
        return 0

    def proccessing(self, data: any) -> Union[dict, int]:
        if data is not None:
            if self.status == STATUS.TRAIN.value:
                pass
            elif self.status == STATUS.PREDICT.value:
                pass
        else:
            return 1

    def train(self):
        pass  # Placeholder for training the model

    def validate(self):
        pass  # Placeholder for model validation

    def predict(self) -> Dict[str, float]:

        return {}  # Placeholder for model prediction


class Block:
    def __init__(self, model: Model, sensors: List[Sensor]):
        self.model = model
        self.sensors = sensors

    def poll_sensors(self) -> Dict[str, Dict[str, float]]:
        data = {}
        for sensor in self.sensors:
            data[sensor.id] = sensor.get_data()
        return data

class Handler:
    def __init__(self, db_path: str, polling_interval: float):
        self.status = 0
        self.logger = logging.getLogger(__name__)
        self.blocks = []
        self.polling_interval = polling_interval
        self.db_path = db_path
        self.running = True

    def add_block(self, model: Model, sensors: List[Sensor]) -> int:
        block = Block(model, sensors)
        self.blocks.append(block)
        return 0

    def run_ml_module(self, block: Block, data: dict) -> Dict[str, float]:
        return block.model.proccessing(data)

    def write_db_data(self, data: Dict[str, float]) -> int:
        try:
            # Write data to the database
            return 0
        except Exception as e:
            self.logger.error(f"Ошибка при записи в БД: {e}")
            return 1
        
    def action(self):
        while self.running:
            for block in self.blocks:
                data = block.poll_sensors()
                status = self.run_ml_module(block, data)
                if type(status) == dict:
                    if status['type'] == 'predict':
                        self.write_db_data(status)
                    elif status['type'] == 'train':
                        pass
                    else:
                        self.running = False
                        raise Exception(f"Некорректный статус модели: {status['type']}")
                else:
                    self.running = False
                    raise Exception("Ошибка при обработке данных моделью")

            time.sleep(self.polling_interval)
            
            


