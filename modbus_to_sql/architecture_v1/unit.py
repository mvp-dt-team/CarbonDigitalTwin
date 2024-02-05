from enum import Enum


class Unit(Enum):
    CELSIUS = 0
    PASCAL = 1
    CUBIC_METER_PER_SECOND = 2


def get_unit_from_str(unit_str: str) -> Unit:
    if unit_str == "Celsius":
        return Unit.CELSIUS
