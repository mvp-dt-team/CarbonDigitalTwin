from typing import Any, Sequence, Dict
from modbus_to_sql.sensors_module.modbus.modbus_rtu_client import ModbusRTUClient
from modbus_to_sql.sensors_module.sensor import Sensor
from modbus_to_sql.sensors_module.modbus.modbus_property import ModbusProperty, RegisterLocation, \
    modbus_data_type_from_str
from pymodbus.exceptions import ModbusIOException

from modbus_to_sql.sensors_module.unit import get_unit_from_str
from modbus_to_sql.network_models.active_sensors_response import ActiveSensorsResponseItem


class ModbusSensor(Sensor):
    def readAllProperties(self) -> Dict[int, Any]:
        return {p_id: self.readPropertyData(p_id) for p_id in self.properties}

    def __init__(self, title: str, s_id: int,
                 properties: Dict[int, ModbusProperty],
                 address: int) -> None:
        super().__init__(title, s_id, properties)
        self.connection = None
        self.address = address

    @staticmethod
    def init_from_network(sensor_data: ActiveSensorsResponseItem) -> ModbusSensor:
        # добавить проверку наличия свойств и выдать соответствующие ошибки
        address = int(sensor_data.parameters.get("address", 0))

        properties = {
            prop.p_id: ModbusProperty(
                id=prop.p_id,
                name=prop.name,
                unit=get_unit_from_str(prop.unit),
                address=int(prop.parameters.get("register", 0)),
                location=RegisterLocation[prop.parameters.get("location", "HOLDING_REGISTERS")],
                dataType=modbus_data_type_from_str(prop.parameters.get("data_type", ""))
            )
            for prop in sensor_data.properties
        }

        return ModbusSensor(sensor_data.s_type, sensor_data.s_id, properties, address)

    def set_connection(self, connection: ModbusRTUClient):
        self.connection = connection

    def __str__(self):
        return (self.title + '(m_addr: ' + str(self.address) + ')' if self.address is not None else self.title) + str(
            self.properties)

    def readPropertyData(self, property_id: int) -> Any:
        if self.connection.is_connected() and self.connection.modbus_client is not None:
            try:
                client = self.connection.modbus_client
                prop = self.properties[property_id]
                if not isinstance(prop, ModbusProperty):
                    raise TypeError("Ожидается поле типа ModbusProperty")
                modbus_response = None
                if prop.location == RegisterLocation.HOLDING_REGISTERS:
                    modbus_response = client.read_holding_registers(
                        prop.address, slave=self.address)

                if modbus_response is None:
                    raise Exception(
                        f"Данная позиция регистра {str(prop.location)} не поддерживается")

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
