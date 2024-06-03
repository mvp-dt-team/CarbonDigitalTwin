import logging
from typing import Dict, List

from network_models.sensors_info import SensorInfo
from sensors_module.sensors.connection import Connection
from sensors_module.sensors.modbus_sensor.sensor import ModbusSensor
from sensors_module.sensors.modbus_sensor.tcp_client import ModbusTCPClient
from sensors_module.sensors.random_sensor.sensor import RandomSensor
from sensors_module.sensors.sensor import Sensor

logger = logging.getLogger('CustomerSettings')


class CustomerSettings:
    connections: Dict[str, Connection]

    def __init__(self) -> None:
        self.init_connections()

    def create_sensors_from_response(self, items: List[SensorInfo]) -> Dict[int, Sensor]:
        sensors = {}
        for item in items:
            if item['type'] == "modbus":
                sensor = ModbusSensor.from_network(item)
                if 'modbus' in self.connections:
                    sensor.set_connection(self.connections['modbus'])
                sensors[sensor.id] = sensor
            elif item['type'] == "random":
                sensor = RandomSensor.from_network(item)
                sensors[sensor.id] = sensor
            else:
                print(f"Unknown sensor type: {item['type']}")
        return sensors

    def init_connections(self):
        self.connections = {}

        self.connections['modbus'] = ModbusTCPClient('192.168.0.1')
        self.connections['modbus'].connect()