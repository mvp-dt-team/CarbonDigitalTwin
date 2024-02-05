from abc import ABC, abstractmethod
from typing import Sequence, Any

from modbus_to_sql.architecture_v1.property import Property
from modbus_to_sql.architecture_v1.sensor import Sensor


class DataStorage(ABC):

    @abstractmethod
    def write_data(self, sensor: Sensor, property: Property, value):
        pass

    @abstractmethod
    def get_sensors_info(self) -> Sequence[Sensor]:
        pass

    @abstractmethod
    def close(self):
        pass
