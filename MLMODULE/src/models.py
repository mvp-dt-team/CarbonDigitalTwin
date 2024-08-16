import random
from typing import List, Union
import importlib
import pickle
import numpy as np


class Model:
    def __init__(
        self,
        id: int,
        model_path: str,
    ):
        self.model_path = model_path
        self.id = id

    def predict(
        self, data: Union[List[int], List[float]]
    ) -> Union[List[int], List[float]]:
        return [random.random()]

    def __repr__(self) -> str:
        return self.id


class RandomForestModel(Model):
    def __init__(self, id: int, model_path: str):
        super().__init__(
            id=id,
            model_path=model_path,
        )
        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)

    def predict(self, data) -> dict:
        result = self.model.predict(np.array(data).reshape(1, -1)).tolist()
        return result


def initialize_model(model_name, *args, **kwargs):
    if model_name == "randomforest":
        return RandomForestModel(*args, **kwargs)
    else:
        return Model
