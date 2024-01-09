from attr import dataclass
from property import Property
from enum import Enum


class RegisterLocation(Enum):
    COILS = 0
    DISCRETE_INPUTS = 1
    HOLDING_REGISTERS = 2
    INPUT_REGISTERS = 3


class ModbusDataType(Enum):
    INT16 = 0


@dataclass
class ModbusProperty(Property):
    address: int
    location: RegisterLocation
    dataType: ModbusDataType
