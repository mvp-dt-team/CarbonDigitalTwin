from dataclasses import dataclass
from enum import Enum

from modbus_to_sql.sensors_module.property import Property


class RegisterLocation(Enum):
    COILS = 0
    DISCRETE_INPUTS = 1
    HOLDING_REGISTERS = 2
    INPUT_REGISTERS = 3


class ModbusDataType(Enum):
    INT16 = 0


def modbus_data_type_from_str(value: str) -> ModbusDataType:
    if value == 'int16':
        return ModbusDataType.INT16
    return ModbusDataType.INT16


@dataclass
class ModbusProperty(Property):
    address: int
    location: RegisterLocation
    dataType: ModbusDataType
