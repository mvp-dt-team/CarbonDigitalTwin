from attr import dataclass
from unit import Unit


@dataclass
class Property():
    name: str
    unit: Unit
