from typing import Any, Dict, Tuple, Callable
from sensors_module.sensors.modbus_sensor.rtu_client import ModbusRTUClient
from sensors_module.sensors.modbus_sensor.tcp_client import ModbusTCPClient
from sensors_module.sensors.sensor import Sensor
from sensors_module.sensors.modbus_sensor.property import ModbusProperty, RegisterLocation, \
    modbus_data_type_from_str
from pymodbus.exceptions import ModbusIOException

from sensors_module.sensors.unit import get_unit_from_str
from network_models.sensors_info import SensorInfo


class ModbusSensor(Sensor):
    @classmethod
    def sensor_parameters(cls) -> Dict[str, Tuple[str, Callable[[Any], bool]]]:
        return {
            'address': ("Введите адрес датчика", lambda x: x.isdigit() and int(x) > 0)
        }

    @classmethod
    def property_parameters(cls) -> Dict[str, Tuple[str, Callable[[Any], bool]]]:
        return {
            'address': ("Введите адрес регистра", lambda x: x.isdigit() and int(x) >= 0),
            'location': ("Введите тип регистра:\n\tCOILS\n\tDISCRETE_INPUTS\n\tHOLDING_REGISTERS\n\tINPUT_REGISTERS",
                         lambda x: x in ["COILS", "DISCRETE_INPUTS", "HOLDING_REGISTERS", "INPUT_REGISTERS"]),
            'data_type': ("Введите тип данных:\n\tint16",
                          lambda x: x in ["int16"])
        }

    def read_all_properties(self) -> Dict[int, Any]:
        return {id: self.read_property_data(id) for id in self.properties}

    def __init__(self, title: str, id: int,
                 properties: Dict[int, ModbusProperty],
                 address: int) -> None:
        super().__init__(title, id, properties)
        self.connection = None
        self.address = address

    @classmethod
    def from_network(cls, sensor: SensorInfo) -> 'Sensor':
        # добавить проверку наличия свойств и выдать соответствующие ошибки
        address = int(sensor['parameters'].get("address", 0))

        properties = {
            prop['measurement_source_id']: ModbusProperty(
                id=prop['measurement_source_id'],
                name=prop['name'],
                unit=get_unit_from_str(prop['unit']),
                address=int(prop['parameters'].get("register", 0)),
                location=RegisterLocation[prop['parameters'].get("location", "HOLDING_REGISTERS")],
                dataType=modbus_data_type_from_str(prop['parameters'].get("data_type", ""))
            )
            for prop in sensor['properties']
        }

        return cls(sensor['type'], sensor['id'], properties, address)

    def set_connection(self, connection: ModbusRTUClient or ModbusTCPClient) -> None:
        self.connection = connection
        print(self.connection, "set conn", self)

    def __str__(self):
        return (self.title + '(m_addr: ' + str(self.address) + ')' if self.address is not None else self.title) + str(
            self.properties)

    def read_property_data(self, property_id: int) -> Any:
        try:
            client = self.connection.modbus_client
            print(self.connection, "client", self.id, self)
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
