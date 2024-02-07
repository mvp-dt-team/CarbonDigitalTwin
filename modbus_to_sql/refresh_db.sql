DROP DATABASE IF EXISTS digital_twin_database;

CREATE DATABASE IF NOT EXISTS digital_twin_database;
USE digital_twin_database;

CREATE TABLE IF NOT EXISTS sensor
(
    id          INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS measurement_source
(
    id          INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(255) NOT NULL,
    units       VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS sensor_item
(
    id                INT PRIMARY KEY AUTO_INCREMENT,
    sensor_id         INT                                NOT NULL,
    installation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_active         BOOLEAN                            NOT NULL,
    addition_info     text,
    FOREIGN KEY (sensor_id) REFERENCES sensor (id)
);

CREATE TABLE IF NOT EXISTS sensor_source_mapping
(
    measurement_source_id INT NOT NULL,
    sensor_item_id        INT NOT NULL,
    PRIMARY KEY (measurement_source_id, sensor_item_id),
    FOREIGN KEY (measurement_source_id) REFERENCES measurement_source (id),
    FOREIGN KEY (sensor_item_id) REFERENCES sensor_item (id)
);

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


CREATE TABLE IF NOT EXISTS measurement
(
    query_id              INT   NOT NULL,
    insert_ts             INT   NOT NULL,
    m_data                FLOAT NOT NULL,
    sensor_item_id        INT   NOT NULL,
    measurement_source_id INT   NOT NULL,
    PRIMARY KEY (query_id, insert_ts),
    FOREIGN KEY (sensor_item_id) REFERENCES sensor_item (id),
    FOREIGN KEY (measurement_source_id) REFERENCES measurement_source (id)
);

CREATE TABLE IF NOT EXISTS raw_data
(
    query_id  INT  NOT NULL,
    insert_ts INT  NOT NULL,
    m_data    TEXT NOT NULL,
    PRIMARY KEY (query_id, insert_ts)
);
