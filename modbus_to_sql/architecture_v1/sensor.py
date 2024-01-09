from abc import ABC, abstractmethod
from typing import Sequence, Any
from property import Property


class Sensor(ABC):

    def __init__(self, title: str, position: str, id: int, properties: Sequence[Property]) -> None:
        self.title = title
        self.position = position
        self.id = id
        self.properties = properties

    @abstractmethod
    def readAllData(self) -> Sequence[Any]:
        pass

    @abstractmethod
    def readPropertyData(self, property_index: int) -> Any:
        pass

    @abstractmethod
    def writeData(self, property_index: int, data: Any) -> None:
        pass
