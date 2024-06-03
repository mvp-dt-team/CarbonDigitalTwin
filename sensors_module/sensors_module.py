import logging
from time import sleep
import threading
from typing import Any, Dict, Callable

from sensors_module.customer_settings import CustomerSettings
from sensors_module.sensors.sensor import Sensor
from sensors_module.storage_client import StorageClient

from config_reader import config

data_storage_address = config.SMADDRESS
continue_running = True
logger = logging.getLogger('SensorsModule')

class SensorsModule:
    sensors: Dict[int, Sensor]
    asker = None
    storage_client: StorageClient
    customer_settings: CustomerSettings

    def __init__(self):
        self.storage_client = StorageClient(data_storage_address)
        self.customer_settings = CustomerSettings()
        sensor_data = self.storage_client.fetch_sensor_data()

        self.sensors = self.customer_settings.create_sensors_from_response(sensor_data)

    def start(self, callback: Callable[[dict[str, dict[str, Any]]], None]):
        logger.debug("module starting")

        def send_and_callback(data: dict[int, dict[int, Any]]):
            self.storage_client.send_measurement_data(data)
            verbose = self.made_measurement_verbose(data)
            callback(verbose)

        self.asker = threading.Thread(
            target=lambda: repeat_every_n_seconds(send_and_callback, self.read_sensors))
        logger.debug("thread started")
        self.asker.start()
        logger.info("module started")

    def stop(self):
        global continue_running
        logger.debug("module stopping")
        continue_running = False
        self.asker.join()
        logger.info("module stopped")

    def read_sensors(self) -> dict[int, dict[int, Any]]:
        logger.debug("reading sensors")
        results = {}
        for sensor_id in self.sensors:
            sensor = self.sensors[sensor_id]
            results[sensor_id] = sensor.read_all_properties()  # обработка ошибок
        return results

    def made_measurement_verbose(self, data: dict[int, dict[int, Any]]) -> dict[str, dict[str, Any]]:
        logger.debug("made sensors verbose")
        results = {}
        for sensor_id in data:
            sensor = self.sensors[sensor_id]
            results[sensor.title] = {sensor.properties[p].name: data[sensor_id][p] for p in data[sensor_id]}
        return results


def repeat_every_n_seconds(callback, task):
    n = config.POLL_INTERVAL
    global continue_running
    while continue_running:
        callback(task())
        sleep(n)
