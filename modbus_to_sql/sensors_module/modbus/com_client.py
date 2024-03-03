from modbus_to_sql.sensors_module.connection import Connection
import pymodbus.client as ModbusClient


class COMClient(Connection):
    modbus_client = None

    def __init__(self, port: str, baudrate: int, timeout: int = 5) -> None:
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def is_connected(self) -> bool:
        return self.modbus_client is None or self.modbus_client.is_active()

    def connect(self):
        if self.is_connected:
            return
        self.modbus_client = ModbusClient.ModbusSerialClient(
            method='rtu', port=self.port, baudrate=self.baudrate, timeout=self.timeout)
        self.modbus_client.connect()

    def disconnect(self):
        if not self.is_connected or self.modbus_client is None:
            return
        self.modbus_client.close()
