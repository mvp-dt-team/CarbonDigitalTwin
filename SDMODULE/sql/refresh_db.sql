-- Информация о моделях сенсоров
CREATE TABLE IF NOT EXISTS sensor
(
    id          INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(255) NOT NULL,
    description TEXT
);

-- Информация о месте получения данных
CREATE TABLE IF NOT EXISTS measurement_source
(
    id          INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(255) NOT NULL,
    units       VARCHAR(255) NOT NULL,
    description TEXT
);

-- Информация о конкретных установленных датчиках
CREATE TABLE IF NOT EXISTS sensor_item
(
    id                INT PRIMARY KEY AUTO_INCREMENT,
    sensor_id         INT                                NOT NULL,
    installation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_active         BOOLEAN                            NOT NULL,
    sensor_type       VARCHAR(50)                        NOT NULL,
    addition_info     text,
    FOREIGN KEY (sensor_id) REFERENCES sensor (id)
);

-- Информация о том, какие конкретные данные получает один конкретный датчик
CREATE TABLE IF NOT EXISTS sensor_source_mapping
(
    measurement_source_id INT NOT NULL,
    sensor_item_id        INT NOT NULL,
    PRIMARY KEY (measurement_source_id, sensor_item_id),
    FOREIGN KEY (measurement_source_id) REFERENCES measurement_source (id),
    FOREIGN KEY (sensor_item_id) REFERENCES sensor_item (id)
);

-- Информация о свойствах конкретного датчика, какой адрес у датчика, по каким регистрам опрашивать данные
CREATE TABLE IF NOT EXISTS sensor_params
(
    id             INT PRIMARY KEY,
    sensor_item_id INT          NOT NULL,
    property_id    INT,
    param_name     VARCHAR(255) NOT NULL,
    param_value    VARCHAR(255) NOT NULL,
    FOREIGN KEY (sensor_item_id) REFERENCES sensor_item (id),
    FOREIGN KEY (property_id) REFERENCES measurement_source (id)
);
-- Информация о файлах, полученных от потковых методов неразрушаемого контроля
CREATE TABLE IF NOT EXISTS raw_data
(
    query_id              INT  NOT NULL,
    m_data                TEXT NOT NULL,
    block_id INT  NOT NULL,
    file_id INT NOT NULL,
    PRIMARY KEY (query_id, block_id, file_id),
    FOREIGN KEY (query_id) REFERENCES prediction (query_id),
    FOREIGN KEY (block_id) REFERENCES blocks (id)
    FOREIGN KEY (file_id) REFERENCES files (id)
);

-- Возможные другие данные
CREATE TABLE IF NOT EXISTS measurement
(
    query_id              INT   NOT NULL,
    insert_ts             INT   NOT NULL,
    m_data                FLOAT NOT NULL,
    measurement_source_id INT   NOT NULL,
    sensor_item_id        INT   NOT NULL,
    PRIMARY KEY (query_id, measurement_source_id),
    FOREIGN KEY (sensor_item_id) REFERENCES sensor_item (id),
    FOREIGN KEY (measurement_source_id) REFERENCES measurement_source (id)
);

-- Хранение файлов
CREATE TABLE IF NOT EXISTS files
(
    id          INT PRIMARY KEY AUTO_INCREMENT,
    description VARCHAR(255)         NOT NULL,
    path        VARCHAR(255) UNIQUE NOT NULL
);

-- Связка для моделей и датчиков
CREATE TABLE IF NOT EXISTS blocks (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    active BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);

-- Измеряемые свойства продукта
CREATE TABLE IF NOT EXISTS property (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    unit VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);

-- Информация о моделях
CREATE TABLE IF NOT EXISTS models (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    type VARCHAR(50) NOT NULL,
    file_id INT NOT NULL,
    block_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (file_id) REFERENCES files(id),
    FOREIGN KEY (block_id) REFERENCES blocks(id)
);

-- Связка для моделей и датчиков
CREATE TABLE IF NOT EXISTS model_mapping (
    id INT NOT NULL AUTO_INCREMENT,
    measurement_source_id INT NOT NULL,
    sensor_item_id INT NOT NULL,
    model_id INT NOT NULL,
    property_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (measurement_source_id) REFERENCES measurement_source(id),
    FOREIGN KEY (sensor_item_id) REFERENCES sensor_item(id),
    FOREIGN KEY (model_id) REFERENCES models(id),
    FOREIGN KEY (property_id) REFERENCES property(id)
);

-- Предсказания, сделанные моделью
CREATE TABLE IF NOT EXISTS prediction (
    id INT NOT NULL AUTO_INCREMENT,
    insert_ts INT NOT NULL,
    m_data FLOAT NOT NULL,
    property_id INT NOT NULL,
    block_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (property_id) REFERENCES property(id),
    FOREIGN KEY (block_id) REFERENCES block(id)
);