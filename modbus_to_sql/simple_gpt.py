import serial
from pymodbus.client.sync import ModbusSerialClient
import mysql.connector

# Настройки COM-порта
com_port = '/dev/ttyUSB0'  # Укажите ваш COM-порт
baud_rate = 9600

# Настройки Modbus
modbus_address = 1  # Адрес устройства на шине Modbus
modbus_register_address = 0  # Адрес регистра, который вы хотите считать

# Настройки MySQL
mysql_host = 'localhost'
mysql_user = 'your_username'
mysql_password = 'your_password'
mysql_database = 'your_database'

# Инициализация COM-порта
ser = serial.Serial(port=com_port, baudrate=baud_rate, timeout=2)

# Инициализация Modbus клиента
modbus_client = ModbusSerialClient(method='rtu', port=com_port, baudrate=baud_rate)
modbus_client.connect()

# Инициализация MySQL соединения
mysql_connection = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database
)

# Создание курсора для выполнения SQL-запросов
cursor = mysql_connection.cursor()

try:
    # Чтение данных с COM-порта
    data_from_com_port = ser.readline().decode('utf-8').strip()

    # Чтение данных по протоколу Modbus
    modbus_response = modbus_client.read_input_registers(modbus_register_address, 1, unit=modbus_address)
    modbus_data = modbus_response.registers[0]

    # Запись данных в MySQL
    sql_query = "INSERT INTO your_table_name (com_port_data, modbus_data) VALUES (%s, %s)"
    sql_data = (data_from_com_port, modbus_data)
    cursor.execute(sql_query, sql_data)
    mysql_connection.commit()

    print("Данные успешно записаны в MySQL.")

except Exception as e:
    print(f"Ошибка: {e}")

finally:
    # Закрытие соединений
    ser.close()
    modbus_client.close()
    cursor.close()
    mysql_connection.close()
