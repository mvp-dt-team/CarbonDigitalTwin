import logging
import random
from typing import Any, Dict, Tuple, Callable

from network_models.sensors_info import SensorInfoPost
from sensors_module.sensors.property import Property
from sensors_module.sensors.sensor import Sensor
from sensors_module.sensors.unit import Unit, get_unit_from_str

logger = logging.getLogger('RandomSensor')

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
    def from_network(cls, sensor: SensorInfoPost) -> 'Sensor':
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
        prop_values = {}
        for prop_id in self.properties:
            try:
                prop_values[prop_id] = self.read_property_data(prop_id)
            except Exception as e:
                logger.error(e)
        return prop_values

    def read_property_data(self, property_id: int) -> Any:
        prop = self.properties[property_id]
        if prop is None:
            raise Exception("Property not found")
        if prop.unit == Unit.CELSIUS:
            return random.uniform(17, 23)
        if prop.unit == Unit.PASCAL:
            return random.uniform(900, 950)
        if prop.unit == Unit.PERCENT:
            return random.uniform(40, 60)
        if prop.unit == Unit.TOGGLER:
            return random.choice([0, 1])
        raise Exception("Unit not supported")
