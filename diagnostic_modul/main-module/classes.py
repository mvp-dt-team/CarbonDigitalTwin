from typing import List, Dict, Union
import logging
import random
from enum import Enum
from datetime import datetime
import time
import sys
import requests
import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import json

import warnings
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=UserWarning)

class Sensor:
    def __init__(self, id: int, measurement_source_id: int, type_sensor: str, name: str, unit: int, description: str): # model_name: str, installation_time: str, deactivation_time: str
        self.type_sensor = type_sensor
        self.id = id
        self.measurement_source_id = measurement_source_id
        self.name = name
        self.unit = unit
        self.description = description


class Model:
    def __init__(self, model_path: str, params: dict, version: str, property_names: List[str]) -> None:
        self.model_path = model_path
        self.params = params
        self.version = version
        self.property_names = property_names

    def predict(self, X) -> Dict[str, float]:
        pass
 

class RandomForestModel(Model):
    def __init__(self, model_path: str, params: Dict, version: str, property_names: List[str]) -> None:
        super().__init__(model_path, params, version, property_names)
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)
    
    # Возможно, стоит добавить иттерацию по результатам прогноза на случай определения нескольких свойств TODO
    def predict(self, X) -> Dict[str, float]:
        result = self.model.predict(np.array(X).reshape(1 ,-1))
        return {"property_names": self.property_names, "values": result.tolist()}
            

class Block:
    def __init__(self, model: Model, sensors: List[Sensor], logger: logging.Logger):
        self.model = model
        self.sensors = sensors
        self.logger = logger

    def poll_sensors(self, url) -> Union[List[float], int]:
        measurements = []
        for sensor in self.sensors:
            measurements.append({
                "sensor_id": sensor.id,
                "measurement_source_id": sensor.measurement_source_id,
                "time_from": "2001-03-26T00:00:00Z",
                "time_to": datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
            })
        try:
            response = requests.post(url=f'http://{url}/measurement', json={'measurements': measurements})
            if response.ok:
                return [x['data'][-1] for x in json.loads(response.content)] 
            else:
                raise Exception(f"{response.status_code} {response.reason}")
        except Exception as e:
            self.logger.error(f"Ошибка опроса датчиков: {e}")
            return 1
    
    def get_list_sensors_id(self) -> list:
        return [x.measurement_source_id for x in self.sensors]

class Handler:
    def __init__(self, polling_interval: float, url: str) -> None:
        self.status = 0
        self.logger = logging.getLogger('MainModule')
        self.logger.setLevel(logging.DEBUG)
        self.blocks: List[Block] = []
        self.polling_interval = polling_interval
        self.running = True
        self.url = url

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.info('Инициализация обработчика')

    def add_block(self, model: Model, sensors: List[Sensor]) -> int:
        block = Block(model, sensors, self.logger)
        self.blocks.append(block)
        return 0

    def write_db_data(self, data: Dict[str, float], sensors: List[int]) -> int:
        try:
            response = requests.post(url=f'http://{self.url}/save_prediction_data', json={"sources": sensors, "property_names": data['property_names'], "values": data['values']})
            if response.ok:
                return 0
            else:
                raise Exception(f"{response.status_code}")
        except Exception as e:
            self.logger.error(f"Ошибка при записи в БД: {e}")
            return 1
        
    def action(self):
        self.logger.info('Модуль начал работать')
        try:
            while self.running:
                for block in self.blocks:
                    self.logger.info('Опрос датчиков')
                    data = block.poll_sensors(self.url)

                    if type(data) is int:
                        self.running = False
                        raise Exception("Не удалось опросить датчики")
                    else:
                        self.logger.info('Передача данных модели')
                        predict_value = block.model.predict(data)
                        self.logger.debug(f'X: {data}, y: {predict_value}')

                        if type(predict_value) == dict:
                                self.logger.info('Отправка данных на сервер')
                                self.write_db_data(predict_value, sensors=block.get_list_sensors_id())
                        else:
                            self.running = False
                            raise Exception("Ошибка при обработке данных моделью")

                time.sleep(self.polling_interval)
        except Exception as exc:
            self.logger.error(f'{exc}')
            
            


