from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    VARCHAR,
    Float,
    BigInteger,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from sqlalchemy.sql import text
# from config_reader import config

# Определение базового класса для декларативного стиля
Base = declarative_base()

from yaml import load
from yaml.loader import SafeLoader
with open('config.yaml', 'r') as config_file:
    config = load(config_file, Loader=SafeLoader)
    


# Определение моделей
class SensorModel(Base):
    __tablename__ = "sensor"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    description = Column(Text)


class MeasurementSourceModel(Base):
    __tablename__ = "measurement_source"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    units = Column(VARCHAR(255), nullable=False)
    description = Column(Text)


class SensorItemModel(Base):
    __tablename__ = "sensor_item"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(Integer, ForeignKey("sensor.id"), nullable=False)
    installation_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, nullable=False)
    sensor_type = Column(VARCHAR(50), nullable=False)
    addition_info = Column(Text)


class SensorSourceMappingModel(Base):
    __tablename__ = "sensor_source_mapping"
    measurement_source_id = Column(
        Integer, ForeignKey("measurement_source.id"), primary_key=True
    )
    sensor_item_id = Column(Integer, ForeignKey("sensor_item.id"), primary_key=True)


class SensorParamsModel(Base):
    __tablename__ = "sensor_params"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_item_id = Column(Integer, ForeignKey("sensor_item.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("measurement_source.id"))
    param_name = Column(VARCHAR(255), nullable=False)
    param_value = Column(VARCHAR(255), nullable=False)


class RawDataModel(Base):
    __tablename__ = "raw_data"
    query_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    m_data = Column(Text, nullable=False)
    measurement_source_id = Column(
        Integer, ForeignKey("measurement_source.id"), primary_key=True
    )


class MeasurementModel(Base):
    __tablename__ = "measurement"
    query_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    insert_ts = Column(Integer, nullable=False)
    m_data = Column(Float, nullable=False)
    measurement_source_id = Column(
        Integer, ForeignKey("measurement_source.id"), primary_key=True
    )
    sensor_item_id = Column(Integer, ForeignKey("sensor_item.id"), nullable=False)


### MODULE ML


class BlockModel(Base):
    __tablename__ = "block"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, nullable=False)


class PropertyModel(Base):
    __tablename__ = "property"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    unit = Column(String(100), nullable=False)


class ModelsModel(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    type = Column(String(50), nullable=False)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("block.id"), nullable=False)


class FileModel(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(VARCHAR(255), nullable=False)
    path = Column(VARCHAR(255), nullable=False)


class ModelMappingModel(Base):
    __tablename__ = "model_mapping"
    id = Column(Integer, primary_key=True, autoincrement=True)
    measurement_source_id = Column(
        Integer, ForeignKey("measurement_source.id"), nullable=False
    )
    sensor_item_id = Column(Integer, ForeignKey("sensor_item.id"), nullable=False)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("property.id"), nullable=False)


class PredictionModel(Base):
    __tablename__ = "prediction"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    insert_ts = Column(Integer, nullable=False, primary_key=True)
    m_data = Column(Float, nullable=False)
    property_id = Column(Integer, ForeignKey("property.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("block.id"), nullable=False)


# НЕОБХОДИМО ПРОПИСАТЬ ОТ SUPER НА СЕРВЕРЕ MYSQL
# DELIMITER //
# CREATE TRIGGER reset_query_id_seq
# BEFORE INSERT ON measurement
# FOR EACH ROW
# BEGIN
#     DECLARE max_value BIGINT;
#     SET max_value = 9223372036854775807; -- BIGINT max value

#     IF NEW.query_id >= max_value THEN
#         SET NEW.query_id = 1;
#     END IF;
# END//
# DELIMITER ;

# Создание экземпляра двигателя
# engine = create_engine('sqlite:///app.db')
engine = create_engine(
    f"mysql+pymysql://{config['USER']}:{config['PASSWORD']}@{config['HOST']}:3306/{config['DB']}"
)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Создание всех таблиц
Base.metadata.create_all(engine)

# Закрытие сессии
session.close()
