from enum import StrEnum, auto


class Unit(StrEnum):
    CELSIUS = auto()
    PASCAL = auto()
    CUBIC_METER_PER_SECOND = auto()


def get_unit_from_str(unit_str: str) -> Unit:
    if unit_str == "Цельсии":
        return Unit.CELSIUS
