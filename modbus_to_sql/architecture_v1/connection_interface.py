from abc import ABC, abstractmethod


class ConnectionInterface(ABC):

    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass
