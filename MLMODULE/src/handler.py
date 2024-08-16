from typing import List, Dict, Union
import logging
import hashlib
from datetime import datetime, timezone
import time
import requests
import os
import uuid

import random

from blocks import Block
from models import initialize_model
from sources import Source
from pathlib import Path

from functools import wraps

import warnings

warnings.filterwarnings("ignore", module="sklearn")


def timeit(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        result = func(self, *args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.logger.debug(
            f"Функция {func.__name__} выполнена за {elapsed_time:.6f} секунд"
        )
        return result

    return wrapper


"""
реконнекшен для сессии
"""


class Handler:
    def __init__(self, config) -> None:
        self.status = 0
        self.running = True
        self.session = requests.Session()

        self.blocks: List[Block] = []
        self.polling_interval: int = config["POLLINT"]
        self.url = "http://" + config["SDIP"] + ":" + str(config["SDPORT"])

        self.models_folder = "./uploads"
        Path(self.models_folder).mkdir(parents=True, exist_ok=True)

        # Настройка логгера
        self.logger = logging.getLogger(config["LOGNAME"])
        self.logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        self.logger.info("Инициализация обработчика")

    @timeit
    def init_block_data(self) -> None:
        self.blocks = []
        block_data = self.session.get(f"{self.url}/blocks/?need_active=true").json()
        for block in block_data:
            if block["model"] is None:
                continue
            sensors = [
                Source(
                    source_point_id=sensor["measurement_source_id"],
                    source_id=sensor["sensor_item_id"],
                    source_type="sensor",
                )
                for sensor in block["sensors"]
            ]

            for relation_block in block["relation_blocks"]:
                sensors.append(
                    Source(
                        source_point_id=relation_block["source_property_id"],
                        source_id=relation_block["source_block_id"],
                        source_type="block",
                    )
                )

            status_response = self.session.get(
                f"{self.url}/blocks/models/check/{block['model']['id']}"
            ).json()
            models_files = [filename for filename in os.listdir(self.models_folder)]
            if status_response["file_name"] in models_files:
                self.logger.debug("Файл есть в системе")
                with open(
                    f"{self.models_folder}/{status_response['file_name']}", "rb"
                ) as model_file:
                    hash_file = hashlib.sha256(model_file.read())
                    if hash_file.hexdigest() != status_response["file_hash"]:
                        self.logger.debug("У файла не тот хэш, устанавливаю его")
                        file = self.session.get(
                            f"{self.url}/blocks/models/{block['model']['id']}"
                        )
                        with open(
                            f"{self.models_folder}/{status_response['file_name']}", "wb"
                        ) as f:
                            for chunk in file.iter_content(1024):
                                f.write(chunk)
            else:
                self.logger.debug("Файла нет, устанавливаю его")
                file = self.session.get(
                    f"{self.url}/blocks/models/{block['model']['id']}"
                )
                with open(
                    f"{self.models_folder}/{status_response['file_name']}", "wb"
                ) as f:
                    for chunk in file.iter_content(1024):
                        f.write(chunk)

            model = initialize_model(
                model_name=block["model"]["type"],
                id=block["model"]["id"],
                model_path=f"{self.models_folder}/{status_response['file_name']}",
            )
            properties = [item["id"] for item in block["properties"]]
            self.blocks.append(
                Block(
                    id=block["id"],
                    model=model,
                    sensors=sensors.copy(),
                    properties=properties.copy(),
                )
            )
        self.logger.debug(self.blocks)

    # TODO
    def write_db_data(self, data: Union[List[int], List[float]], block: Block) -> int:
        try:
            current_time = datetime.now(timezone.utc)
            data_to_recive = [
                {
                    "m_data": data[i],
                    "property_id": block.properties[i],
                    "block_id": block.id,
                }
                for i in range(len(data))
            ]
            response = self.session.post(
                url=f"{self.url}/blocks/prediction",
                json={
                    "insert_ts": current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
                    + "Z",
                    "query_uuid": str(uuid.uuid4()),
                    "insert_values": data_to_recive,
                },
            )
            if response.ok:
                return 0
            else:
                raise Exception(f"{response.status_code}")
        except Exception as e:
            self.logger.error(f"Ошибка при записи в БД: {e}")
            return 1

    @timeit
    def workflow(self, block: Block):
        start_time = time.time()
        self.logger.debug(f"Получение данных для блока {block.id}")
        data = block.poll_sensors(self.url, self.session)
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.logger.debug(f"ДАННЫЕ: {elapsed_time:.6f} секунд")

        start_time = time.time()
        self.logger.debug(f"Получение предсказания для блока {block.id}")
        predict_value: Union[List[int], List[float]] = block.model.predict(data)
        time.sleep(0.8)  # Заглушка для модели
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.logger.debug(f"ПРЕДСКАЗАНИЕ: {elapsed_time:.6f} секунд")

        self.logger.info(f"Отправка данных блока {block.id} на сервер")
        start_time = time.time()
        self.write_db_data(data=predict_value, block=block)
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.logger.debug(f"ОТПРАВЛЕНИЕ: {elapsed_time:.6f} секунд")

    # TODO Переделать отправку данных, для отправки пакета данных по всем блокам, а не делать милион запросов для отправки каждого предсказания
    def action(self):
        self.logger.info(f"Инициализация блоков")
        start_time = time.time()
        self.init_block_data()
        for block in self.blocks:
            self.workflow(block)
        end_time = time.time()
        elapsed_time = end_time - start_time
        if self.polling_interval - elapsed_time > 0:
            self.logger.info(f"Ожидание...")
            time.sleep(self.polling_interval - elapsed_time)

    def stop(self) -> None:
        self.running = False
