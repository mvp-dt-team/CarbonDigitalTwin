from typing import List, Any
import requests

from modbus_to_sql.sensors_module.modbus.modbus_sensor import ModbusSensor

data_storage_address = 'http://localhost:3000'


class SensorsModule:
    sensors: List[ModbusSensor]

    def __init__(self):
        url = data_storage_address + '/active_sensors'
        sensor_data = fetch_sensor_data(url)

        if sensor_data:
            process_sensor_data(sensor_data)
            self.sensors = create_sensors_from_response(sensor_data)


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
        print(f"Sensor ID: {sensor['s_id']}")
        print(f"Sensor Type: {sensor['s_type']}")
        print(f" Sensor parameters:")
        for param_name, param_value in sensor['parameters'].items():
            print(f" - {param_name}: {param_value}")
        print("Properties:")
        for prop in sensor['properties']:
            print(f" - Property ID: {prop['p_id']}, Unit: {prop['unit']}, Name: {prop['name']}")
            print(f" - - Prop parameters:")
            for param_name, param_value in prop['parameters'].items():
                print(f" - - - {param_name}: {param_value}")
        print("---")


def create_sensors_from_response(items: List[ActiveSensorsResponseItem]) -> List[Sensor]:
    sensors = []
    for item in items:
        if item.s_type == "modbus":
            sensor = ModbusSensor(sensor_data=item)
            sensors.append(sensor)
        elif item.s_type == "anotherType":
            # Предположим, что у AnotherSensorType есть подходящий метод создания или конструктор
            sensor = AnotherSensorType(sensor_data=item)
            sensors.append(sensor)
        else:
            print(f"Unknown sensor type: {item.s_type}")
    return sensors
