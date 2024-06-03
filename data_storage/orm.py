from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, VARCHAR, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

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
    query_id = Column(Integer, primary_key=True, nullable=False)
    m_data = Column(Text, nullable=False)
    measurement_source_id = Column(Integer, ForeignKey('measurement_source.id'), primary_key=True)

class MeasurementModel(Base):
    __tablename__ = 'measurement'
    query_id = Column(Integer, primary_key=True, nullable=False)
    insert_ts = Column(Integer, nullable=False)
    m_data = Column(Float, nullable=False)
    measurement_source_id = Column(Integer, ForeignKey('measurement_source.id'), primary_key=True)
    sensor_item_id = Column(Integer, ForeignKey('sensor_item.id'), nullable=False)

# # Создание соединения с базой данных
# engine = create_engine('mysql+pymysql://username:password@host:port/dbname')

# # Создание всех таблиц заново
# Base.metadata.create_all(engine)

# # Создание сессии
# Session = sessionmaker(bind=engine)
# session = Session()

# # Пример добавления данных
# sensor = Sensor(name='Temperature Sensor', description='Measures temperature')
# session.add(sensor)
# session.commit()

# # Получение id добавленного сенсора
# sensor_id = sensor.id

# # Добавление SensorItem с указанием installation_date
# sensor_item = SensorItem(
#     sensor_id=sensor_id,
#     installation_date=datetime.now(),
#     is_active=True,
#     sensor_type='Temperature',
#     addition_info='Installed in lab'
# )
# session.add(sensor_item)
# session.commit()

# # Закрытие сессии
# session.close()
