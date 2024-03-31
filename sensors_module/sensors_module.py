from time import sleep
import threading
from typing import List, Any, Dict
import requests

from network_models.sensors_info import SensorInfo
from sensors_module.modbus.modbus_sensor import ModbusSensor
from sensors_module.property import Property
from sensors_module.random_sensor.random_sensor import RandomSensor
from sensors_module.sensor import Sensor
from sensors_module.unit import Unit

data_storage_address = 'http://localhost:3000'
continue_running = True


class SensorsModule:
    sensors: Dict[int, Sensor]
    asker = None

    def __init__(self):
        from_db = True
        if from_db:
            url = data_storage_address + '/sensor?active=true'
            sensor_data = fetch_sensor_data(url)

            if sensor_data:
                process_sensor_data(sensor_data)
                self.sensors = create_sensors_from_response(sensor_data)
        else:
            self.sensors = {
                1: RandomSensor("test 1", 1, {
                    1: Property(1, "first prop", Unit.CELSIUS),
                    2: Property(2, "second prop", Unit.TOGGLER)
                }),
                2: RandomSensor("test 2", 1, {
                    3: Property(3, "У входа в фильеру", Unit.CELSIUS),
                    4: Property(4, "У выхода", Unit.CELSIUS),
                    5: Property(5, "В центре", Unit.CELSIUS)
                })
            }

        print("module inited")

    def start(self, callback):
        print("module starting")
        self.asker = threading.Thread(target=lambda: repeat_every_5_seconds(callback, self.read_sensors_verbose))
        print("thread started")
        self.asker.start()
        print("module started")

    def stop(self):
        global continue_running
        print("module stopping")
        continue_running = False
        self.asker.join()
        print("module stopped")

    def read_sensors(self):
        print("reading sensors")
        results = {}
        for sensor_id in self.sensors:
            sensor = self.sensors[sensor_id]
            results[sensor_id] = sensor.read_all_properties()
        return results

    def read_sensors_verbose(self):
        print("reading sensors verbose")
        results = {}
        for sensor_id in self.sensors:
            sensor = self.sensors[sensor_id]
            p_data = sensor.read_all_properties()
            results[sensor.title] = {sensor.properties[p].name: p_data[p] for p in p_data}
        return results


def repeat_every_5_seconds(callback, task):
    global continue_running
    while continue_running:
        print("task is running")
        callback(task())
        sleep(5)


def fetch_sensor_data(url: str) -> List[Any]:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Это вызовет исключение для кодов состояния 4xx/5xx
        sensor_data = response.json()
        return sensor_data
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
    return []


def process_sensor_data(sensor_data: List[Any]):
    # Простая обработка: печатаем информацию о каждом сенсоре
    for sensor in sensor_data:
        print(f"Sensor ID: {sensor['id']}")
        print(f"Sensor Type: {sensor['type']}")
        print(f" Sensor parameters:")
        for param_name, param_value in sensor['parameters'].items():
            print(f" - {param_name}: {param_value}")
        print("Properties:")
        for prop in sensor['properties']:
            print(f" - Property ID: {prop['id']}, Unit: {prop['unit']}, Name: {prop['name']}")
            print(f" - - Prop parameters:")
            for param_name, param_value in prop['parameters'].items():
                print(f" - - - {param_name}: {param_value}")
        print("---")


def create_sensors_from_response(items: List[SensorInfo]) -> Dict[int, Sensor]:
    sensors = {}
    for item in items:
        if item['type'] == "modbus":
            sensor = ModbusSensor.from_network(item)
            sensors[sensor.id] = sensor
        elif item['type'] == "random":
            sensor = RandomSensor.from_network(item)
            sensors[sensor.id] = sensor
        else:
            print(f"Unknown sensor type: {item['type']}")
    return sensors
