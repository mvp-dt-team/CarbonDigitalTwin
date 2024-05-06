from dataclasses import dataclass
from sensors_module.sensors.unit import Unit


@dataclass
class Property:
    id: int  # measurement_source_id
    name: str
    unit: Unit
