USE digital_twin_database;

INSERT INTO sensor (name, description)
VALUES ('Терморегулятор ESM', 'Поддерживает подключение термопары и нагревателя\\охладителя'),
       ('Реле а345', 'Поддерживает подключение по modbus');

INSERT INTO sensor_item (sensor_id, is_active)
VALUES (1, TRUE),
       (2, FALSE);

INSERT INTO measurement_source (name, units, description)
VALUES ('Температура у входа в фильеру', 'Цельсии', NULL),
       ('Состояние нагревателя у входа в фильеру', 'Включен/выключен', 'Управляется за счет температуры');

INSERT INTO connection_params (sensor_item_id, param_name, param_value)
VALUES (1, 'type', 'modbus'),
       (1, 'address', '1');

INSERT INTO sensor_source_mapping
VALUES (1, 1)