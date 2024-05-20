# CREATE DATABASE digital_twin_database;
USE digital_twin_database;

# Информация о моделях сенсоров
INSERT INTO sensor (id, name, description)
VALUES (0, 'Терморегулятор ESM', 'Поддерживает подключение термопары и нагревателя\\охладителя'),
       (1, 'Реле а345', 'Поддерживает подключение по modbus_sensor');

# Информация о конкретных установленных датчиках
INSERT INTO sensor_item (id, sensor_id, is_active, sensor_type)
VALUES (0, 0, TRUE, 'modbus_sensor'),
       (1, 1, FALSE, 'random');

# Информация о месте получения данных
INSERT INTO measurement_source (id, name, units, description)
VALUES (0, 'Температура у входа в фильеру', 'Цельсии', NULL),
       (1, 'Состояние нагревателя у входа в фильеру', 'Включен/выключен', 'Управляется за счет температуры');

# Информация о свойствах конкретного датчика, какой адрес у датчика, по каким регистрам опрашивать данные
INSERT INTO sensor_params (id, sensor_item_id, property_id, param_name, param_value)
VALUES (0, 1, null, 'address', '1'),
       (1, 1, 1, 'location', 'HOLDING_REGISTERS'),
       (2, 1, 1, 'register', '1'),
       (3, 1, 1, 'data_type', 'int16');

# Информация о том, какие конкретные данные получает один конкретный датчик
INSERT INTO sensor_source_mapping
VALUES (0, 0),
       (1, 1);
