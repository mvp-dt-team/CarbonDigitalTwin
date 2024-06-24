import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from data_storage.orm import (
    Base,
    FileModel,
    ModelMappingModel,
    ModelsModel,
    PropertyModel,
    BlockModel,
    SensorModel,
    MeasurementSourceModel,
    SensorItemModel,
    SensorSourceMappingModel,
    SensorParamsModel,
    MeasurementModel,
    PredictionModel,
    RawDataModel,
)
from config_reader import config
from network_models.sensors_info import SensorInfoPost, SensorPropertyPost


# Функция для очистки базы данных
def clear_database(session):
    # Очистка базы данных после теста
    session.query(PredictionModel).delete()
    # session.query(ModelMappingModel).delete()
    session.query(MeasurementModel).delete()
    # session.query(RawDataModel).delete()
    # session.query(SensorParamsModel).delete()
    # session.query(SensorSourceMappingModel).delete()
    # session.query(SensorItemModel).delete()
    # session.query(SensorModel).delete()
    # session.query(BlockModel).delete()
    # session.query(ModelsModel).delete()
    # session.query(PropertyModel).delete()
    # session.query(FileModel).delete()
    # session.query(MeasurementSourceModel).delete()

    # Фиксируем изменения
    session.commit()


# Функция для создания начальных данных
def create_initial_data(session):
    # Добавляем начальные данные в базу
    measurement_source = MeasurementSourceModel(
        name="MSTEST1", description="Test measurement_source", units="Цельсии"
    )
    session.add(measurement_source)
    session.flush()  # Применяем изменения, чтобы получить id нового measurement_source

    sensor_model = SensorModel(name="SMTEST1", description="Test Sensor Model")
    session.add(sensor_model)
    session.flush()  # Применяем изменения, чтобы получить id нового sensor_model

    sensor = SensorInfoPost(
        parameters={},
        type="random",
        properties=[
            SensorPropertyPost(
                name="testProperty", parameters={}, measurement_source_id=1
            )
        ],
        is_active=True,
        description="Test",
        sensor_model_id=1,
    )

    new_sensor_item = SensorItemModel(
        sensor_id=sensor.sensor_model_id,
        is_active=True,
        sensor_type=sensor.type,
        addition_info=sensor.description,
    )
    session.add(new_sensor_item)
    session.flush()  # Применяем изменения, чтобы получить id нового sensor_item
    print("-" * 30, new_sensor_item.id)

    # Добавляем в sensor_source_mapping
    for prop in sensor.properties:
        new_sensor_source_mapping = SensorSourceMappingModel(
            measurement_source_id=prop.measurement_source_id,
            sensor_item_id=new_sensor_item.id,
        )
        session.add(new_sensor_source_mapping)

    session.commit()


@pytest.fixture(scope="session")
def engine():
    engine_url = f"mysql+pymysql://{config.USER}:{config.PASSWORD.get_secret_value()}@{config.HOST}:3306/{config.DATABASE}"
    return create_engine(engine_url)


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture(scope="function", autouse=True)
def setup_database(session):
    clear_database(session)  # Очистка базы данных перед тестом
    create_initial_data(session)  # Создание начальных данных перед тестом
    yield  # Здесь происходит выполнение самого теста
    clear_database(session)  # Очистка базы данных после теста
