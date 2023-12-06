import serial
from pymodbus.client.sync import ModbusSerialClient
import mysql.connector

class COMPortReader:
    def __init__(self, port, baud_rate=9600):
        self.ser = serial.Serial(port=port, baudrate=baud_rate, timeout=2)

    def read_data(self):
        return self.ser.readline().decode('utf-8').strip()

    def close(self):
        self.ser.close()

class ModbusReader:
    def __init__(self, port, baud_rate=9600, address=1):
        self.client = ModbusSerialClient(method='rtu', port=port, baudrate=baud_rate)
        self.address = address

    def read_data(self, register_address):
        response = self.client.read_input_registers(register_address, 1, unit=self.address)
        return response.registers[0]

    def close(self):
        self.client.close()

class MySQLWriter:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.connection.cursor()

    def write_data(self, com_port_data, modbus_data, table_name):
        sql_query = f"INSERT INTO {table_name} (com_port_data, modbus_data) VALUES (%s, %s)"
        sql_data = (com_port_data, modbus_data)
        self.cursor.execute(sql_query, sql_data)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

# Пример использования классов
com_port_reader = COMPortReader(port='/dev/ttyUSB0')
modbus_reader = ModbusReader(port='/dev/ttyUSB0')
mysql_writer = MySQLWriter(host='localhost', user='your_username', password='your_password', database='your_database')

try:
    com_port_data = com_port_reader.read_data()
    modbus_data = modbus_reader.read_data(register_address=0)
    mysql_writer.write_data(com_port_data, modbus_data, table_name='your_table_name')
    print("Данные успешно записаны в MySQL.")
except Exception as e:
    print(f"Ошибка: {e}")
finally:
    com_port_reader.close()
    modbus_reader.close()
    mysql_writer.close()
