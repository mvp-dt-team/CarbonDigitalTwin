from typing import Any, Sequence
from modbus_to_sql.sensors_module.modbus.com_client import COMClient
from modbus_to_sql.sensors_module.sensor import Sensor
from modbus_to_sql.sensors_module.modbus.modbus_property import ModbusProperty, RegisterLocation, modbus_data_type_from_str
from pymodbus.exceptions import ModbusIOException

from modbus_to_sql.sensors_module.unit import get_unit_from_str
from modbus_to_sql.network_models.active_sensors_response import ActiveSensorsResponseItem


class ModbusSensor(Sensor):
    def __init__(self, title: str, id: int,
                 properties: Sequence[ModbusProperty],
                 address: int) -> None:
        super().__init__(title, id, properties)
        self.connection = None
        self.address = address

    def init_from_network(self, sensor_data: ActiveSensorsResponseItem) -> None:
        # добавить проверку наличия свойств и выдать соответствующие ошибки
        address = int(sensor_data.parameters.get("address", 0))

        properties = [
            ModbusProperty(
                id=prop.p_id,
                name=prop.name,
                unit=get_unit_from_str(prop.unit),
                address=int(prop.parameters.get("register", 0)),
                location=RegisterLocation[prop.parameters.get("location", "HOLDING_REGISTERS")],
                dataType=modbus_data_type_from_str(prop.parameters.get("data_type", ""))
            )
            for prop in sensor_data.properties
        ]

        super().__init__(title=sensor_data.s_type, id=sensor_data.s_id, properties=properties)
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