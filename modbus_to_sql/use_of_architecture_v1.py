from modbus_to_sql.architecture_v1.com_client import COMClient
from modbus_to_sql.architecture_v1.modbus_sensor import ModbusSensor
from modbus_to_sql.architecture_v1.mysql_storage import MySQLStorage

# Настройки COM-порта
com_port = 'COM2'
baud_rate = 115200
# Настройки Modbus

# Настройки MySQL
mysql_host = 'localhost'
mysql_user = 'digital_twin'
mysql_password = 'digital_twin'
mysql_database = 'digital_twin_database'

connection = COMClient(com_port, baud_rate, 5)
connection.connect()

storage = MySQLStorage(mysql_host, mysql_password, mysql_user, mysql_database)
sensors = storage.get_sensors_info()
for s in sensors:
    print(str(s))
for s in sensors:
    if isinstance(s, ModbusSensor):
        s.set_connection(connection)
print(sensors[0].readPropertyData(0))
