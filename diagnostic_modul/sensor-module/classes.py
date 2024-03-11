from queue import Queue
from torch import Tensor
from typing import Union
from enum import Enum
import numpy as np

class TypingSource(Enum):
    VIDEO = 0
    OTHER = 1

class Handler:
    def __init__(self):
        self.sources = []
        self.models = []
        self.queue = Queue()

    def polling_sensors(self) -> int:
        pass

    def value_predict(self, source_value: Tensor) -> Union[int, Tensor]:
        pass

    def write_db_request(self, value_list: list) -> int:
        # Запрос на запись значений в БД
        pass

    def run(self) -> None:
        pass

class Source:
    def __init__(self, id, unit, number):
        self.id = id
        self.unit = unit
        self.number = number

    def get_value(self) -> Union[list, np.array]:
        # Запрос к источнику данных
        return 0

class Model:
    def __init__(self, version: str, path: str):
        self.version = version
        self.path = path
    
    def predict(self, value: Tensor) -> Tensor:
        pass

    def initialization(self):
        pass