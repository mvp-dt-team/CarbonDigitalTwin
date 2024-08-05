from dataclasses import dataclass
from sensors.unit import Unit


@dataclass
class Property:
    id: int  # measurement_source_id
    name: str
    unit: Unit
