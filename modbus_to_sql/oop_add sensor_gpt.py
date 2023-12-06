import serial
from pymodbus.client.sync import ModbusSerialClient
import mysql.connector

class Sensor:
    def __init__(self, com_port, modbus_address, table_name):
        self.com_port = com_port
        self.modbus_address = modbus_address
        self.table_name = table_name
        self.com_port_reader = COMPortReader(port=com_port)
        self.modbus_reader = ModbusReader(port=com_port, address=modbus_address)
    
    def read_data(self):
        com_port_data = self.com_port_reader.read_data()
        modbus_data = self.modbus_reader.read_data(register_address=0)
        return com_port_data, modbus_data
    
    def write_data_to_mysql(self):
        com_port_data, modbus_data = self.read_data()
        mysql_writer.write_data(com_port_data, modbus_data, self.table_name)
    
    def close(self):
        self.com_port_reader.close()
        self.modbus_reader.close()

# Пример использования классов для двух датчиков
sensor1 = Sensor(com_port='/dev/ttyUSB0', modbus_address=1, table_name='sensor1_data')
sensor2 = Sensor(com_port='/dev/ttyUSB1', modbus_address=2, table_name='sensor2_data')

mysql_writer = MySQLWriter(host='localhost', user='your_username', password='your_password', database='your_database')

try:
    sensor1.write_data_to_mysql()
    sensor2.write_data_to_mysql()
    print("Данные успешно записаны в MySQL.")
except Exception as e:
    print(f"Ошибка: {e}")
finally:
    sensor1.close()
    sensor2.close()
    mysql_writer.close()
