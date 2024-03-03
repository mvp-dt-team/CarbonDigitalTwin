from abc import ABC, abstractmethod
from typing import Any, Dict
from modbus_to_sql.sensors_module.property import Property


class Sensor(ABC):

    def __init__(self, title: str, id: int, properties: Dict[int, Property]) -> None:
        self.title = title
        self.id = id
        self.properties = properties

    @abstractmethod
    def readPropertyData(self, property_id: int) -> Any:
        pass

    @abstractmethod
    def readAllProperties(self) -> Dict[int, Any]:
        pass