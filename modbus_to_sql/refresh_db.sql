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
    units       VARCHAR(255),
    description TEXT
);

CREATE TABLE IF NOT EXISTS sensor_item
(
    id                INT PRIMARY KEY AUTO_INCREMENT,
    sensor_id         INT NOT NULL,
    installation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_active         BOOLEAN NOT NULL,
    addition_info     text,
    FOREIGN KEY (sensor_id) REFERENCES sensor (id)
);

CREATE TABLE IF NOT EXISTS sensor_source_mapping (
    measurement_source_id INT,
    sensor_item_id INT,
    PRIMARY KEY (measurement_source_id, sensor_item_id),
    FOREIGN KEY (measurement_source_id) REFERENCES measurement_source(id),
    FOREIGN KEY (sensor_item_id) REFERENCES sensor_item(id)
);

CREATE TABLE IF NOT EXISTS connection_params (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sensor_item_id INT,
    param_name VARCHAR(255),
    param_value VARCHAR(255),
    FOREIGN KEY (sensor_item_id) REFERENCES sensor_item(id)
);

CREATE TABLE IF NOT EXISTS measurement
(
    query_id              INT,
    insert_ts             INT,
    m_data                FLOAT,
    sensor_item_id        INT,
    measurement_source_id INT,
    PRIMARY KEY (query_id, insert_ts),
    FOREIGN KEY (sensor_item_id) REFERENCES sensor_item (id),
    FOREIGN KEY (measurement_source_id) REFERENCES measurement_source (id)
);

CREATE TABLE IF NOT EXISTS raw_data
(
    query_id  INT,
    insert_ts INT,
    m_data    TEXT,
    PRIMARY KEY (query_id, insert_ts)
);

CREATE VIEW measurement_info AS
SELECT m.query_id,
       m.insert_ts,
       m.m_data,
       s.name         AS sensor_name,
       si.installation_date,
       si.is_active,
       ms.name        AS source_name,
       ms.units,
       ms.description AS source_description
FROM measurement m
         JOIN
     sensor_item si ON m.sensor_item_id = si.id
         JOIN
     sensor s ON si.sensor_id = s.id
         JOIN
     measurement_source ms ON m.measurement_source_id = ms.id;

