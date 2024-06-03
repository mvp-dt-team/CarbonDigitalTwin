import datetime
import logging
from typing import List, Any

import requests

from network_models.measurements_info import MeasurementsPost, MeasurementsGet

logger = logging.getLogger('StorageClient')


def print_sensor_data(sensor_data: List[Any]):
    log_entry = ""
    for sensor in sensor_data:
        log_entry += f"Sensor ID: {sensor['id']}\n"
        log_entry += f"Sensor Type: {sensor['type']}\n"
        log_entry += f" Sensor parameters:\n"
        for param_name, param_value in sensor['parameters'].items():
            log_entry += f" - {param_name}: {param_value}\n"
        log_entry += "Properties:\n"
        for prop in sensor['properties']:
            log_entry += f" - Source ID: {prop['measurement_source_id']}, Unit: {prop['unit']}, Name: {prop['name']}\n"
            log_entry += f" - - Prop parameters:\n"
            for param_name, param_value in prop['parameters'].items():
                log_entry += f" - - - {param_name}: {param_value}\n"
        log_entry += "---\n"
    logger.debug(log_entry)


class StorageClient:
    def __init__(self, storage_address):
        self.storage_address = storage_address

    def fetch_sensor_data(self) -> List[Any]:
        url = self.storage_address + '/sensor?active=true'

        sensor_data = []
        try:
            response = requests.get(url)
            response.raise_for_status()
            sensor_data = response.json()
        except requests.exceptions.HTTPError as errh:
            logger.error(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            logger.error(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            logger.error(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            logger.error(f"Oops: Something Else: {err}")

        print_sensor_data(sensor_data)

        return sensor_data

    def send_measurement_data(self, data: dict[int, dict[int, Any]]):
        values = []
        logger.info(data)
        for sensor_id in data:
            for property_id in data[sensor_id]:
                values.append(MeasurementsGet(
                    m_data=data[sensor_id][property_id],
                    sensor_item_id=sensor_id,
                    measurement_source_id=property_id
                ))
            sent_data = MeasurementsPost(
                insert_ts=datetime.datetime.now(),
                insert_values=values
            )

            url = self.storage_address + '/measurement'
            try:
                headers = {'Content-Type': 'application/json'}

                response = requests.post(url, data=sent_data.model_dump_json(), headers=headers)
                logger.info(f'Sent measurement: Status Code: {response.status_code}; Response Body: {response.json()}')
            except requests.exceptions.RequestException as err:
                logger.warning(f"Sent measurement: Something went wrong: {err}")
