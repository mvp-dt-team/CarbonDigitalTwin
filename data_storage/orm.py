from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, VARCHAR, Float, \
    BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.sql import text

from config_reader import config

# Определение базового класса для декларативного стиля
Base = declarative_base()


# Определение моделей
class SensorModel(Base):
    __tablename__ = 'sensor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    description = Column(Text)


class MeasurementSourceModel(Base):
    __tablename__ = 'measurement_source'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    units = Column(VARCHAR(255), nullable=False)
    description = Column(Text)


class SensorItemModel(Base):
    __tablename__ = 'sensor_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(Integer, ForeignKey('sensor.id'), nullable=False)
    installation_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, nullable=False)
    sensor_type = Column(VARCHAR(50), nullable=False)
    addition_info = Column(Text)


class SensorSourceMappingModel(Base):
    __tablename__ = 'sensor_source_mapping'
    measurement_source_id = Column(Integer, ForeignKey('measurement_source.id'), primary_key=True)
    sensor_item_id = Column(Integer, ForeignKey('sensor_item.id'), primary_key=True)


class SensorParamsModel(Base):
    __tablename__ = 'sensor_params'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_item_id = Column(Integer, ForeignKey('sensor_item.id'), nullable=False)
    property_id = Column(Integer, ForeignKey('measurement_source.id'))
    param_name = Column(VARCHAR(255), nullable=False)
    param_value = Column(VARCHAR(255), nullable=False)


class RawDataModel(Base):
    __tablename__ = 'raw_data'
    query_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    m_data = Column(Text, nullable=False)
    measurement_source_id = Column(Integer, ForeignKey('measurement_source.id'), primary_key=True)


class MeasurementModel(Base):
    __tablename__ = 'measurement'
    query_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    insert_ts = Column(Integer, nullable=False)
    m_data = Column(Float, nullable=False)
    measurement_source_id = Column(Integer, ForeignKey('measurement_source.id'), primary_key=True)
    sensor_item_id = Column(Integer, ForeignKey('sensor_item.id'), nullable=False)


class FileModel(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    path = Column(String, unique=True, index=True)

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
