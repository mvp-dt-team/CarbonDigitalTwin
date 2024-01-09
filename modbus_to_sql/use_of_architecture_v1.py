
# Настройки COM-порта
from modbus_to_sql.architecture_v1.com_client import COMClient
from modbus_to_sql.architecture_v1.modbus_property import ModbusDataType, ModbusProperty, RegisterLocation
from modbus_to_sql.architecture_v1.modbus_sensor import ModbusSensor
from modbus_to_sql.architecture_v1.unit import Unit


com_port = 'COM2'  # Укажите ваш COM-порт
baud_rate = 115200

# Настройки Modbus
modbus_address = 1  # Адрес устройства на шине Modbus
modbus_register_address = 0x00  # Адрес регистра, который вы хотите считать

connection = COMClient(com_port, baud_rate, 5)
sensor = ModbusSensor("Терморегулятор", "Комната", 1,
                      [ModbusProperty("Температура", Unit.CELSIUS, 0x00,
                                      RegisterLocation.HOLDING_REGISTERS, ModbusDataType.INT16)],
                      1, connection)
