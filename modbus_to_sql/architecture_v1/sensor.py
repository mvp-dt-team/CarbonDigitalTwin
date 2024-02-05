from abc import ABC, abstractmethod
from typing import Sequence, Any
from modbus_to_sql.architecture_v1.property import Property


class Sensor(ABC):

    def __init__(self, title: str, id: int, properties: Sequence[Property]) -> None:
        self.title = title
        self.id = id
        self.properties = properties

    @abstractmethod
    def readAllData(self) -> Sequence[Any]:
        pass

    @abstractmethod
    def readPropertyData(self, property_index: int) -> Any:
        pass
