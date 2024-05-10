# CREATE DATABASE digital_twin_database;
USE digital_twin_database;

# Информация о моделях сенсоров
INSERT INTO sensor (name, description)
VALUES ('Терморегулятор ESM', 'Поддерживает подключение термопары и нагревателя\\охладителя'),
       ('Реле а345', 'Поддерживает подключение по modbus_sensor'),
       ('Экструдер', '');

# Информация о конкретных установленных датчиках
INSERT INTO sensor_item (sensor_id, is_active, sensor_type)
VALUES (1, TRUE, 'random'),
       (2, FALSE, 'random');

# Информация о месте получения данных
INSERT INTO measurement_source (name, units, description)
VALUES ('Температура у входа в фильеру', 'Цельсии', NULL),
       ('Состояние нагревателя у входа в фильеру', 'Включен/выключен', 'Управляется за счет температуры'),
       ('Давление в зоне 1', 'Паскаль', NULL),
       ('Температура в зоне 12', 'Цельсии', 'Описание');

# Информация о свойствах конкретного датчика, какой адрес у датчика, по каким регистрам опрашивать данные
INSERT INTO sensor_params (sensor_item_id, property_id, param_name, param_value)
VALUES (1, null, 'address', '1'),
       (1, 1, 'location', 'HOLDING_REGISTERS'),
       (1, 1, 'register', '1'),
       (1, 1, 'data_type', 'int16');

# Информация о том, какие конкретные данные получает один конкретный датчик
INSERT INTO sensor_source_mapping (measurement_source_id, sensor_item_id)
VALUES (1, 1),
       (2, 2),
       (3, 1),
       (4, 1);
