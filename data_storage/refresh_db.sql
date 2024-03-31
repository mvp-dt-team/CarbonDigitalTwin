DROP DATABASE IF EXISTS digital_twin_database;

CREATE DATABASE IF NOT EXISTS digital_twin_database;
USE digital_twin_database;

# Информация о моделях сенсоров
CREATE TABLE IF NOT EXISTS sensor
(
    id          INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(255) NOT NULL,
    description TEXT
);

# Информация о месте получения данных
CREATE TABLE IF NOT EXISTS measurement_source
(
    id          INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(255) NOT NULL,
    units       VARCHAR(255) NOT NULL,
    description TEXT
);

# Информация о конкретных установленных датчиках
CREATE TABLE IF NOT EXISTS sensor_item
(
    id                INT PRIMARY KEY AUTO_INCREMENT,
    sensor_id         INT                                NOT NULL,
    installation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_active         BOOLEAN                            NOT NULL,
    sensor_type       VARCHAR(50) NOT NULL,
    addition_info     text,
    FOREIGN KEY (sensor_id) REFERENCES sensor (id)
);

# Информация о том, какие конкретные данные получает один конкретный датчик
CREATE TABLE IF NOT EXISTS sensor_source_mapping
(
    measurement_source_id INT NOT NULL,
    sensor_item_id        INT NOT NULL,
    PRIMARY KEY (measurement_source_id, sensor_item_id),
    FOREIGN KEY (measurement_source_id) REFERENCES measurement_source (id),
    FOREIGN KEY (sensor_item_id) REFERENCES sensor_item (id)
);

# Информация о свойствах конкретного датчика, какой адрес у датчика, по каким регистрам опрашивать данные
CREATE TABLE IF NOT EXISTS sensor_params
(
    id             INT PRIMARY KEY AUTO_INCREMENT,
    sensor_item_id INT          NOT NULL,
    property_id    INT,
    param_name     VARCHAR(255) NOT NULL,
    param_value    VARCHAR(255) NOT NULL,
    FOREIGN KEY (sensor_item_id) REFERENCES sensor_item (id),
    FOREIGN KEY (property_id) REFERENCES measurement_source (id)
);

# Информация о измерениях, снятых с датчиков
CREATE TABLE IF NOT EXISTS measurement
(
    query_id              INT   NOT NULL,
    insert_ts             INT   NOT NULL,
    m_data                FLOAT NOT NULL,
    sensor_item_id        INT   NOT NULL,
    measurement_source_id INT   NOT NULL,
    PRIMARY KEY (query_id, measurement_source_id),
    FOREIGN KEY (sensor_item_id) REFERENCES sensor_item (id),
    FOREIGN KEY (measurement_source_id) REFERENCES measurement_source (id)
);

# Возможные другие данные
CREATE TABLE IF NOT EXISTS raw_data
(
    query_id  INT  NOT NULL,
    insert_ts INT  NOT NULL,
    m_data    TEXT NOT NULL,
    PRIMARY KEY (query_id, insert_ts)
);
