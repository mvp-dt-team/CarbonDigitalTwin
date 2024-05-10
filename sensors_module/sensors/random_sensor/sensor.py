import random
from typing import Any, Dict, Tuple, Callable

from network_models.sensors_info import SensorInfo
from sensors_module.sensors.property import Property
from sensors_module.sensors.sensor import Sensor
from sensors_module.sensors.unit import Unit, get_unit_from_str


class RandomSensor(Sensor):
    @classmethod
    def sensor_parameters(cls) -> Dict[str, Tuple[str, Callable[[Any], bool]]]:
        return {}

    @classmethod
    def property_parameters(cls) -> Dict[str, Tuple[str, Callable[[Any], bool]]]:
        return {}

    def __init__(self, title: str, id: int, properties: Dict[int, Property]):
        super().__init__(title, id, properties)

    @classmethod
    def from_network(cls, sensor: SensorInfo) -> 'Sensor':
        properties = {
            prop['measurement_source_id']: Property(
                id=prop['measurement_source_id'],
                name=prop['name'],
                unit=get_unit_from_str(prop['unit']),
            )
            for prop in sensor['properties']
        }

        return RandomSensor(sensor['id'], sensor['id'], properties)

    def read_all_properties(self) -> Dict[int, Any]:
        return {id: self.read_property_data(id) for id in self.properties}

    def read_property_data(self, property_id: int) -> Any:
        prop = self.properties[property_id]
        if prop is None:
            raise Exception("Property not found")
        if prop.unit == Unit.CELSIUS:
            return random.uniform(-1, 100)
        if prop.unit == Unit.TOGGLER:
            return random.choice([0, 1])
        if prop.unit == Unit.PASCAL:
            return random.uniform(-100, 0)
        raise Exception("Unit not supported")
