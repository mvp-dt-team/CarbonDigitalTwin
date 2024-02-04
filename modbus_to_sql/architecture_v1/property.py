from attr import dataclass
from unit import Unit


@dataclass
class Property:
    id: int
    name: str
    unit: Unit
