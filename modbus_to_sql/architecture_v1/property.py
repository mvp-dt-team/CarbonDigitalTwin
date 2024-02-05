from dataclasses import dataclass
from modbus_to_sql.architecture_v1.unit import Unit


@dataclass
class Property:
    id: int  # measurement_source_id
    name: str
    unit: Unit
