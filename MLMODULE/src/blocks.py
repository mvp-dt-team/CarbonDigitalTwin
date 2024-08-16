from models import Model
from sources import Source

import logging
import requests

from datetime import datetime
from typing import Union, List, Dict

import time


class Block:
    def __init__(
        self, id: int, model: Model, sensors: List[Source], properties: List[int]
    ):
        self.id = id
        self.model = model
        self.sensors = sensors
        self.properties = properties

    def poll_sensors(self, url, session) -> Union[List[float], List[int]]:
        sensors_measurements = []
        block_predictions = []
        measurements_list = []
        for sensor in self.sensors:
            if sensor.source_type == "sensor":
                sensors_measurements.append(sensor.source_point_id)
            if sensor.source_type == "block":
                block_predictions.append((sensor.source_point_id, sensor.source_id))
        try:
            # Добавляем измерения с датчиков
            response = session.get(
                url=f"{url}/measurement/?"
                + "&".join(
                    ["measurement_source_ids=" + str(x) for x in sensors_measurements]
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
                for x in latest_measurements_list:
                    measurements_list.append(x["m_data"])
            else:
                raise Exception(f"{response.status_code} {response.reason}")

            # Добавляем предсказания зависимых блоков
            for block in block_predictions:
                response = session.get(
                    url=f"{url}/blocks/prediction?block_id={block[1]}&property_id={block[0]}&n_predictions=1"
                )
                if response.ok:
                    measurements_list.append(response.json()[0]["m_data"])
                else:
                    raise Exception(f"{response.status_code} {response.reason}")

            return measurements_list
        except Exception as e:
            return e

    def get_list_sensors_id(self) -> list:
        return [x.id for x in self.sensors]

    def __repr__(self) -> str:
        return f"BLOCK: id={self.id}, model_id={self.model.id}, sensors={[sensor.source_point_id for sensor in self.sensors]}, properties={self.properties}"
