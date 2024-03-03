import random
from typing import Any, Dict

from modbus_to_sql.network_models.active_sensors_response import ActiveSensorsResponseItem
from modbus_to_sql.sensors_module.property import Property
from modbus_to_sql.sensors_module.sensor import Sensor
from modbus_to_sql.sensors_module.unit import Unit, get_unit_from_str


class RandomSensor(Sensor):
    def readPropertyData(self, property_id: int) -> Any:
        prop = self.properties[property_id]
        if prop is None:
            raise Exception("Property not found")
        if prop.unit == Unit.CELSIUS:
            return random.uniform(-1, 100)
        raise Exception("Unit not supported")

    def __init__(self, title: str, s_id: int, properties: Dict[int, Property]):
        super().__init__(title, s_id, properties)

    @staticmethod
    def init_from_network(sensor_data: ActiveSensorsResponseItem):
        properties = {
            prop.p_id: Property(
                id=prop.p_id,
                name=prop.name,
                unit=get_unit_from_str(prop.unit),
            )
            for prop in sensor_data.properties
        }

        return RandomSensor(sensor_data.s_type, sensor_data.s_id, properties)

    def readAllProperties(self) -> Dict[int, Any]:
        return {p_id: self.readPropertyData(p_id) for p_id in self.properties}