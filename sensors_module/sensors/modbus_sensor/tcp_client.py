from sensors_module.sensors.connection import Connection
import pymodbus.client as ModbusClient


class ModbusTCPClient(Connection):

    def __init__(self, host) -> None:
        super().__init__()
        self.host = host
        self.modbus_client = None

    def is_connected(self) -> bool:
        return self.modbus_client is not None

    def connect(self):
        print("Connecting to Modbus Server")
        if self.is_connected():
            return
        print("Connected to Modbus Server")
        self.modbus_client = ModbusClient.ModbusTcpClient(self.host)
        print(self.modbus_client)
        self.modbus_client.connect()

    def disconnect(self):
        if not self.is_connected or self.modbus_client is None:
            return
        self.modbus_client.close()
