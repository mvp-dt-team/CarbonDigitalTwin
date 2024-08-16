from models import Model
from sources import Source

import logging
import requests

from datetime import datetime
from typing import Union, List, Dict


class Block:
    def __init__(
        self, id: int, model: Model, sensors: List[Source], properties: List[int]
    ):
        self.id = id
        self.model = model
        self.sensors = sensors
        self.properties = properties

    def poll_sensors(self, url) -> Union[List[float], List[int]]:
        measurements = []
        for sensor in self.sensors:
            measurements.append(sensor.measurement_source_id)
        try:
            response = requests.get(
                url=f"{url}/measurement?"
                + "&".join(["measurement_source_ids=" + str(x) for x in measurements])
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
                measurements_list = [x["m_data"] for x in latest_measurements_list]

                return measurements_list
            else:
                raise Exception(f"{response.status_code} {response.reason}")
        except Exception as e:
            return e

    def get_list_sensors_id(self) -> list:
        return [x.id for x in self.sensors]

    def __repr__(self) -> str:
        return f"BLOCK: id={self.id}, model_id={self.model.id}, sensors={[sensor.measurement_source_id for sensor in self.sensors]}, properties={self.properties}"
