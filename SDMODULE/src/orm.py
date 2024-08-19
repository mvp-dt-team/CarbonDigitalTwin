from sqlalchemy import (
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

import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import async_sessionmaker
from datetime import datetime
from sqlalchemy.sql import text

# from config_reader import config
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

# Определение базового класса для декларативного стиля
# Base = declarative_base()


class Base(AsyncAttrs, DeclarativeBase):
    pass


from yaml import load
from yaml.loader import SafeLoader

with open("../config.yaml", "r") as config_file:
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
    query_id = Column(VARCHAR(36), primary_key=True, nullable=False, autoincrement=True)
    m_data = Column(Text, nullable=False)
    measurement_source_id = Column(
        Integer, ForeignKey("measurement_source.id"), primary_key=True
    )


class MeasurementModel(Base):
    __tablename__ = "measurement"
    query_id = Column(VARCHAR(36), primary_key=True, nullable=False)
    insert_ts = Column(Integer, primary_key=True, nullable=False)
    m_data = Column(Float, nullable=False)
    measurement_source_id = Column(
        Integer, ForeignKey("measurement_source.id"), primary_key=True
    )
    sensor_item_id = Column(Integer, ForeignKey("sensor_item.id"), nullable=False)


### MODULE ML


class BlockModel(Base):
    __tablename__ = "blocks"
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
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)


class FileModel(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(VARCHAR(255), nullable=False)
    path = Column(VARCHAR(255), nullable=False)
    filename = Column(VARCHAR(255), nullable=False)
    filehash = Column(VARCHAR(255), nullable=False)


class ModelMappingModel(Base):
    __tablename__ = "model_mapping"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Тип источника данных: 'sensor' или 'block'
    source_type = Column(VARCHAR(50), nullable=False)

    # Поля для сенсоров
    measurement_source_id = Column(
        Integer, ForeignKey("measurement_source.id"), nullable=True
    )
    sensor_item_id = Column(Integer, ForeignKey("sensor_item.id"), nullable=True)

    # Поля для блоков
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=True)
    property_source_id = Column(Integer, ForeignKey("property.id"), nullable=True)

    # Общие поля
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("property.id"), nullable=False)

    # Связи (relationship)
    measurement_source = relationship(
        "MeasurementSourceModel", foreign_keys=[measurement_source_id]
    )
    sensor_item = relationship("SensorItemModel", foreign_keys=[sensor_item_id])
    block = relationship("BlockModel", foreign_keys=[block_id])
    property_source = relationship("PropertyModel", foreign_keys=[property_source_id])
    model = relationship("ModelsModel", foreign_keys=[model_id])
    property = relationship("PropertyModel", foreign_keys=[property_id])


class PredictionModel(Base):
    __tablename__ = "prediction"
    query_id = Column(VARCHAR(36), nullable=False, primary_key=True)
    insert_ts = Column(Integer, nullable=False, primary_key=True)
    m_data = Column(Float, nullable=False)
    property_id = Column(
        Integer, ForeignKey("property.id"), nullable=False, primary_key=True
    )
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)


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
# engine = create_async_engine(
#     f"mysql+aiomysql://{config['USER']}:{config['PASSWORD']}@{config['HOST']}:3306/{config['DB']}"
# )

# # Создание сессии
# Session = async_sessionmaker(bind=engine)
# session = Session()

# async with engine.begin() as conn:
#     await conn.run_sync(Base.metadata.create_all)
# # Создание всех таблиц
# Base.metadata.create_all(engine)

# # Закрытие сессии
# session.close()
