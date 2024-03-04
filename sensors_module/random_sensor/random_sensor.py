import random
from typing import Any, Dict

from network_models.active_sensors_response import ActiveSensorsResponseItem
from sensors_module.property import Property
from sensors_module.sensor import Sensor
from sensors_module.unit import Unit, get_unit_from_str


class RandomSensor(Sensor):
    def read_property_data(self, property_id: int) -> Any:
        prop = self.properties[property_id]
        if prop is None:
            raise Exception("Property not found")
        if prop.unit == Unit.CELSIUS:
            return random.uniform(-1, 100)
        raise Exception("Unit not supported")

    def __init__(self, title: str, s_id: int, properties: Dict[int, Property]):
        super().__init__(title, s_id, properties)

    @classmethod
    def from_network(cls, sensor: ActiveSensorsResponseItem) -> 'Sensor':
        properties = {
            prop.p_id: Property(
                id=prop.p_id,
                name=prop.name,
                unit=get_unit_from_str(prop.unit),
            )
            for prop in sensor.properties
        }

        return RandomSensor(sensor.s_type, sensor.s_id, properties)

    def read_all_properties(self) -> Dict[int, Any]:
        return {p_id: self.read_property_data(p_id) for p_id in self.properties}