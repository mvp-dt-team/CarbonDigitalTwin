import datetime
import json
import random
from time import sleep
import threading
from typing import List, Any, Dict
import requests

from network_models.measurements_info import MeasurementsInfo, Measurement
from network_models.sensors_info import SensorInfo
from sensors_module.sensors.modbus_sensor.sensor import ModbusSensor
from sensors_module.sensors.property import Property
from sensors_module.sensors.random_sensor.sensor import RandomSensor
from sensors_module.sensors.sensor import Sensor
from sensors_module.sensors.unit import Unit

data_storage_address = 'http://localhost:8000'
continue_running = True


class SensorsModule:
    sensors: Dict[int, Sensor]
    asker = None

    def __init__(self):
        from_db = True #  TODO Изменил на True для проверки на работоспособность соединение с модулем хранения данных
        if from_db:
            url = data_storage_address + '/sensor?active=true'
            sensor_data = fetch_sensor_data(url)

            if sensor_data:
                print_sensor_data(sensor_data)
                self.sensors = create_sensors_from_response(sensor_data)
            else:
                print('Датчиков не обнаружено')
        else:
            self.sensors = {
                1: RandomSensor("Терморегулятор в промывочной ванне", 1, {
                    1: Property(1, "Температура в ванне", Unit.CELSIUS),
                    2: Property(2, "Состояние нагревателя", Unit.TOGGLER)
                }),
                2: RandomSensor("Термопара", 2, {
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

    def read_sensors(self) -> dict[int, dict[int, Any]]:
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

    def send_data_to_storage(self, data: dict[int, dict[int, Any]]):
        print("sending data to storage")
        values = []
        for sensor_id in data:
            for property_id in data[sensor_id]:
                values.append(Measurement(
                    m_data=data[sensor_id][property_id],
                    sensor_item_id=sensor_id,
                    measurement_source_id=property_id
                ))
        query_id = random.randint(0, 10 ** 9)
        sent_data = MeasurementsInfo(
            query_id=query_id,
            insert_ts=datetime.datetime.now(),
            insert_values=values
        )
        send_measurement_data(data_storage_address + '/measurement', sent_data)


def repeat_every_5_seconds(callback, task):
    global continue_running
    while continue_running:
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


def print_sensor_data(sensor_data: List[Any]):
    for sensor in sensor_data:
        print(f"Sensor ID: {sensor['id']}")
        print(f"Sensor Type: {sensor['type']}")
        if sensor['parameters']:
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
        if item['type'] == "modbus_sensor":
            sensor = ModbusSensor.from_network(item)
            sensors[sensor.id] = sensor
        elif item['type'] == "random":
            sensor = RandomSensor.from_network(item)
            sensors[sensor.id] = sensor
        else:
            print(f"Unknown sensor type: {item['type']}")
    return sensors


def send_measurement_data(url: str, data: MeasurementsInfo):
    try:
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, data=json.dumps(data), headers=headers)
        print(f'Status Code: {response.status_code}')
        print(f'Response Body: {response.json()}')
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")
