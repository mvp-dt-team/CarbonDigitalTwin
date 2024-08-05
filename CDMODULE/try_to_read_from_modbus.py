import serial
import pymodbus.client as ModbusClient
from pymodbus.exceptions import ModbusIOException
import logging

logging.basicConfig(level=logging.DEBUG)


# Настройки COM-порта
com_port = "COM2"  # Укажите ваш COM-порт
baud_rate = 9600

# Настройки Modbus
modbus_address = 1  # Адрес устройства на шине Modbus
modbus_register_address = 0x01  # Адрес регистра, который вы хотите считать

# Инициализация Modbus клиента
modbus_client = ModbusClient.ModbusSerialClient(
    method="rtu", port=com_port, baudrate=baud_rate, timeout=5
)
c = modbus_client.connect()

# # Инициализация MySQL соединения
# mysql_connection = mysql.connector.connect(
#     host=mysql_host,
#     user=mysql_user,
#     password=mysql_password,
#     database=mysql_database
# )

# # Создание курсора для выполнения SQL-запросов
# cursor = mysql_connection.cursor()
if not c:
    modbus_client.close()
else:
    try:

        # Чтение данных по протоколу Modbus
        print("read_holding_registers")
        modbus_response = modbus_client.read_holding_registers(
            modbus_register_address, count=5, slave=modbus_address
        )
        if modbus_response.isError():
            print("Error reading register!")
            print(modbus_response)
        else:
            print("try ti decode")
            print(modbus_response.registers)
            print("Register value:", modbus_response.registers[modbus_register_address])
        # # Запись данных в MySQL
        # sql_query = "INSERT INTO your_table_name (com_port_data, modbus_data) VALUES (%s, %s)"
        # sql_data = (data_from_com_port, modbus_data)
        # cursor.execute(sql_query, sql_data)
        # mysql_connection.commit()

        # print("Данные успешно записаны в MySQL.")

    except ModbusIOException as modbus_error:
        print(f"Ошибка Modbus: {modbus_error}")
        # Дополнительная обработка ошибки Modbus
    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        pass
        # Закрытие соединений
        # cursor.close()
        # mysql_connection.close()
    modbus_client.close()
