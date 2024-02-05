from typing import Any, Sequence
from modbus_to_sql.architecture_v1.com_client import COMClient
from modbus_to_sql.architecture_v1.sensor import Sensor
from modbus_to_sql.architecture_v1.modbus_property import ModbusProperty, RegisterLocation
from pymodbus.exceptions import ModbusIOException


class ModbusSensor(Sensor):
    def __init__(self, title: str, id: int,
                 properties: Sequence[ModbusProperty],
                 address: int) -> None:
        super().__init__(title, id, properties)
        self.connection = None
        self.address = address

    def set_connection(self, connection: COMClient):
        self.connection = connection

    def __str__(self):
        return (self.title + '(m_addr: ' + str(self.address) + ')' if self.address is not None else self.title) + str(
            self.properties)

    def readPropertyData(self, property_index: int) -> Any:
        if self.connection.is_connected() and self.connection.modbus_client is not None:
            try:
                client = self.connection.modbus_client
                property = self.properties[property_index]
                if not isinstance(property, ModbusProperty):
                    raise TypeError("Ожидается поле типа ModbusProperty")
                modbus_response = None
                if property.location == RegisterLocation.HOLDING_REGISTERS:
                    modbus_response = client.read_holding_registers(
                        property.address, slave=self.address)

                if modbus_response is None:
                    raise Exception(
                        f"Данная позиция регистра {str(property.location)} не поддерживается")

                if modbus_response.isError():
                    print("Error reading register!")
                    print(modbus_response)
                else:
                    print(modbus_response.registers)
                    print("Register value:", modbus_response.registers[0])
                    return modbus_response.registers[0]

            except ModbusIOException as modbus_error:
                print(f"Ошибка Modbus: {modbus_error}")
            except Exception as e:
                print(f"Ошибка: {e}")

    def readAllData(self) -> Sequence[Any]:
        return super().readAllData()
