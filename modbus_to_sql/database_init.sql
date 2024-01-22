-- Создание базы данных
CREATE DATABASE IF NOT EXISTS digital_twin_database;
USE digital_twin_database;

-- Создание таблицы sensor
CREATE TABLE IF NOT EXISTS sensor (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

-- Создание таблицы measurement_source
CREATE TABLE IF NOT EXISTS measurement_source (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    units VARCHAR(255),
    description TEXT
);

-- Создание таблицы sensor_item
CREATE TABLE IF NOT EXISTS sensor_item (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sensor_id INT,
    installation_date DATE,
    is_active BOOLEAN,
    FOREIGN KEY (sensor_id) REFERENCES sensor(id)
);

-- Создание таблицы measurement
CREATE TABLE IF NOT EXISTS measurement (
    query_id INT,
    insert_ts INT,
    m_data FLOAT,
    sensor_item_id INT,
    measurement_source_id INT,
    PRIMARY KEY (query_id, insert_ts),
    FOREIGN KEY (sensor_item_id) REFERENCES sensor_item(id),
    FOREIGN KEY (measurement_source_id) REFERENCES measurement_source(id)
);

-- Создание таблицы raw_data
CREATE TABLE IF NOT EXISTS raw_data (
    query_id INT,
    insert_ts INT,
    m_data TEXT,
    PRIMARY KEY (query_id, insert_ts)
);

-- Создание представления (view) для получения информации о measurement
CREATE VIEW measurement_info AS
SELECT 
    m.query_id,
    m.insert_ts,
    m.value,
    s.name AS sensor_name,
    si.installation_date,
    si.is_active,
    ms.name AS source_name,
    ms.units,
    ms.description AS source_description
FROM 
    measurement m
JOIN 
    sensor_item si ON m.sensor_item_id = si.id
JOIN 
    sensor s ON si.sensor_id = s.id
JOIN 
    measurement_source ms ON m.measurement_source_id = ms.id;
