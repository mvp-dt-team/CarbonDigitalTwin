from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple, Callable

from network_models.sensors_info import SensorInfoPost
from sensors.property import Property


class Sensor(ABC):

    @classmethod
    @abstractmethod
    def sensor_parameters(cls) -> Dict[str, Tuple[str, Callable[[Any], bool]]]:
        pass

    @classmethod
    @abstractmethod
    def property_parameters(cls) -> Dict[str, Tuple[str, Callable[[Any], bool]]]:
        pass

    def __init__(self, title: str, id: int, properties: Dict[int, Property]) -> None:
        self.title = title
        self.id = id
        self.properties = properties

    @abstractmethod
    def read_property_data(self, property_id: int) -> Any:
        pass

    @abstractmethod
    def read_all_properties(self) -> Dict[int, Any]:
        pass

    @classmethod
    @abstractmethod
    def from_network(cls, sensor: SensorInfoPost) -> "Sensor":
        pass
