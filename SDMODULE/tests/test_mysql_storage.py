import pytest
from datetime import datetime
from src.mysql_storage import MySQLStorage
import asyncio

from src.network_models.measurements_info import MeasurementsGet
from src.network_models.measurement_source_info import MeasurementSourceInfoGet
from src.network_models.blocks import PredictionPost, PropertyPost

from pydantic_core._pydantic_core import ValidationError
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
import requests
import uuid
import os

from src.orm import (
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
)

from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
# Тесты для функций добавления данных

from yaml import load
from yaml.loader import SafeLoader
from sqlalchemy.future import select
from sqlalchemy import update, delete

with open("config.yaml", "r") as config_file:
    config = load(config_file, Loader=SafeLoader)
                  
DATABASE_URL = f"mysql+aiomysql://{config['USER']}:{config['PASSWORD']}@{config['HOST']}:3306/{config['DB']}"
# Создание асинхронного движка и фабрики сессий
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,

)


@pytest.mark.asyncio
async def test_add_measurement():
    """Тест на добавление измерения в БД"""
    os.environ["TESTING"] = "True"
    
    await engine.dispose()
    async with AsyncSessionLocal() as session:
        
        
        await session.execute(delete(PredictionModel))
        await session.execute(delete(ModelMappingModel))
        await session.execute(delete(ModelsModel))
        await session.execute(delete(FileModel))
        await session.execute(delete(PropertyModel))
        await session.execute(delete(BlockModel))
        await session.execute(delete(MeasurementModel))
        await session.commit()
    async with AsyncSessionLocal() as session:
        storage = MySQLStorage()
        measurement = MeasurementsGet(
            m_data=1,
            sensor_item_id=1,
            measurement_source_id=1,
        )
        insert_ts = datetime.now()
        await storage.add_measurement(measurement, insert_ts, query_uuid=str(uuid.uuid4()), session=session)
        await session.commit()
        
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(MeasurementModel).where(MeasurementModel.sensor_item_id==1))
        result = result.scalars().first()
        assert result is not None
        assert result.m_data == 1
        assert result.sensor_item_id == 1
        assert result.measurement_source_id == 1
    
    del os.environ["TESTING"]
    await engine.dispose()


@pytest.mark.asyncio
async def test_add_measurement_err_insert_ts():
    """Тест на добавление измерения в БД без вставки времени"""
    os.environ["TESTING"] = "True"
    
    await engine.dispose()
    async with AsyncSessionLocal() as session:
        await session.execute(delete(MeasurementModel))
        await session.execute(delete(PredictionModel))
        await session.commit()
        
    async with AsyncSessionLocal() as session:
        storage = MySQLStorage()
        measurement = MeasurementsGet(
            m_data=1,
            sensor_item_id=1,
            measurement_source_id=1,
        )
        insert_ts = None
        with pytest.raises(AttributeError) as excinfo:
            await storage.add_measurement(measurement, insert_ts, query_uuid=str(uuid.uuid4()), session=session)
            await session.commit()
    
    del os.environ["TESTING"]
    await engine.dispose()



@pytest.mark.asyncio
async def test_add_measurement_err_m_data():
    """Тест на добавление измерения в БД без вставки данных измерения"""
    os.environ["TESTING"] = "True"
    
    await engine.dispose()
    async with AsyncSessionLocal() as session:
        await session.execute(delete(MeasurementModel))
        await session.execute(delete(PredictionModel))
        await session.commit()
        
    async with AsyncSessionLocal() as session:
        storage = MySQLStorage()
        with pytest.raises(ValidationError) as excinfo:
            measurement = MeasurementsGet(
                m_data=None,
                sensor_item_id=1,
                measurement_source_id=1,
            )
            insert_ts = datetime.now()
            await storage.add_measurement(measurement, insert_ts, query_uuid=str(uuid.uuid4()), session=session)
            await session.commit()
    del os.environ["TESTING"]
    await engine.dispose()



@pytest.mark.asyncio
async def test_add_measurement_err_sensor_item_id():
    """Тест на добавление измерения в БД без вставки ID датчика"""
    os.environ["TESTING"] = "True"
    
    await engine.dispose()
    async with AsyncSessionLocal() as session:
        await session.execute(delete(MeasurementModel))
        await session.execute(delete(PredictionModel))
        await session.commit()
    
    async with AsyncSessionLocal() as session:
        storage = MySQLStorage()
        with pytest.raises(ValidationError) as excinfo:
            measurement = MeasurementsGet(
                m_data=1,
                sensor_item_id=None,
                measurement_source_id=1,
            )
            insert_ts = datetime.now()
            await storage.add_measurement(measurement, insert_ts, query_uuid=str(uuid.uuid4()), session=session)
            await session.commit()
            
    del os.environ["TESTING"]
    await engine.dispose()


@pytest.mark.asyncio
async def test_add_measurement_err_measurement_source_id():
    """Тест на добавление измерения в БД без вставки ID точки измерения"""
    os.environ["TESTING"] = "True"
    
    await engine.dispose()
    async with AsyncSessionLocal() as session:
        await session.execute(delete(MeasurementModel))
        await session.execute(delete(PredictionModel))
        await session.commit()
        
    async with AsyncSessionLocal() as session:
        storage = MySQLStorage()
        with pytest.raises(ValidationError) as excinfo:
            measurement = MeasurementsGet(
                m_data=1,
                sensor_item_id=1,
                measurement_source_id=None,
            )
            insert_ts = datetime.now()
            await storage.add_measurement(measurement, insert_ts, query_uuid=str(uuid.uuid4()), session=session)
            await session.commit()
    
    del os.environ["TESTING"]
    await engine.dispose()


@pytest.mark.asyncio
async def test_get_last_three_measurements_for_sources():
    """Тест на получения последних трех измерений из БД"""
    os.environ["TESTING"] = "True"
    
    await engine.dispose()
    async with AsyncSessionLocal() as session:
        await session.execute(delete(MeasurementModel))
        await session.execute(delete(PredictionModel))
        await session.commit()
    
    storage = MySQLStorage()      
    measurement1 = MeasurementsGet(
        m_data=2,
        sensor_item_id=1,
        measurement_source_id=1,
    )
    measurement2 = MeasurementsGet(
        m_data=3,
        sensor_item_id=1,
        measurement_source_id=1,
    )
    insert_ts1 = datetime.now()

    async with AsyncSessionLocal() as session:
            await storage.add_measurement(measurement1, insert_ts1, query_uuid=str(uuid.uuid4()), session=session)
            await session.commit()
    
    insert_ts2 = datetime.now()
    
    async with AsyncSessionLocal() as session:        
            await storage.add_measurement(measurement2, insert_ts2, query_uuid=str(uuid.uuid4()), session=session)
            await session.commit()
    
    async with AsyncSessionLocal() as session:       
            result = await storage.get_last_three_measurements_for_sources([1], session=session)
    
    assert len(result) == 2
    assert result[0].m_data == 3 or result[0].m_data == 2
    
    await engine.dispose()
    del os.environ["TESTING"]

@pytest.mark.asyncio
async def test_get_last_three_measurements_for_sources_err():
    """Тест на получения последних трех измерений из БД"""
    os.environ["TESTING"] = "True"
    
    await engine.dispose()
    async with AsyncSessionLocal() as session:
        await session.execute(delete(MeasurementModel))
        await session.execute(delete(PredictionModel))
        await session.commit()

    
    storage = MySQLStorage()
    async with AsyncSessionLocal() as session:
        result = await storage.get_last_three_measurements_for_sources([6435], session=session)

    assert len(result) == 0
    
    await engine.dispose()
    del os.environ["TESTING"]


@pytest.mark.asyncio
async def test_get_measurements_sources():
    """Тест на получения всех источников измерений из БД"""
    os.environ["TESTING"] = "True"
    
    await engine.dispose()
    async with AsyncSessionLocal() as session:
        await session.execute(delete(MeasurementModel))
        await session.execute(delete(PredictionModel))
        await session.commit()
    
    storage = MySQLStorage()
    async with AsyncSessionLocal() as session:
        result = await storage.get_measurement_sources(session=session)
        result_real = await session.execute(select(MeasurementSourceModel))
        result_real = result_real.scalars().all()
    assert len(result) == len(result_real)
    assert type(result) is list
    
    await engine.dispose()
    del os.environ["TESTING"]


@pytest.mark.asyncio
async def test_patch_sensor():
    """Тест на изменение состояния датчика"""
    
    os.environ["TESTING"] = "True"
    await engine.dispose()
    async with AsyncSessionLocal() as session:
        await session.execute(delete(MeasurementModel))
        await session.execute(delete(PredictionModel))
        await session.commit()
        
    storage = MySQLStorage()
    async with AsyncSessionLocal() as session:
        await storage.toggle_sensor_activation(1, False, session=session)
        await session.commit()
        result = await session.execute(select(SensorItemModel).where(SensorItemModel.id==1))
        
    sensor = result.scalars().first()

    assert sensor.is_active == False
    
    await engine.dispose()
    del os.environ["TESTING"]

@pytest.mark.asyncio
async def test_successful_block_list_retrieval():
    
    """Тест получение списка блоков из БД"""
    os.environ["TESTING"] = "True"
    await engine.dispose()

    async with AsyncSessionLocal() as session:
        await session.execute(delete(MeasurementModel))
        await session.execute(delete(PredictionModel))
        await session.commit()
    
    storage = MySQLStorage()
    async with AsyncSessionLocal() as session:
        block = BlockModel(name="test", active=True)
        session.add(block)
        await session.commit()
        
    async with AsyncSessionLocal() as session:
        list_blocks = await storage.get_block_list(need_active=True, session=session)
        
    assert len(list_blocks) == 1
    assert list_blocks[0].name == "test"
    async with AsyncSessionLocal() as session:
        await session.execute(delete(BlockModel))
        await session.commit()
    
    await engine.dispose()
    del os.environ["TESTING"]


@pytest.mark.asyncio
async def test_block_list_retrieval_with_activity_filter():
    
    """Тест получение списка блоков из БД с фильтром активности"""
    os.environ["TESTING"] = "True"
    await engine.dispose()
    
    storage = MySQLStorage()
    active_block = BlockModel(name="test1", active=True)
    inactive_block = BlockModel(name="test2", active=False)
    async with AsyncSessionLocal() as session:
        session.add_all([active_block, inactive_block])
        await session.commit()
        
    async with AsyncSessionLocal() as session:
        list_blocks = await storage.get_block_list(need_active=True, session=session)
    
    assert len(list_blocks) == 1
    assert list_blocks[0].name == "test1"
    async with AsyncSessionLocal() as session:
        await session.execute(delete(BlockModel))
        await session.commit()
    
    await engine.dispose()
    del os.environ["TESTING"]


@pytest.mark.asyncio
async def test_add_block_params():
    """Тест на добавление параметров к блоку"""
    os.environ["TESTING"] = "True"
    await engine.dispose()
    
    storage = MySQLStorage()
    block = BlockModel(name="test", active=True)
    block2 = BlockModel(name="test2", active=True)
    async with AsyncSessionLocal() as session:
        session.add(block)
        session.add(block2)
        await session.commit()

    property_param = PropertyModel(name="test", unit="test")
    async with AsyncSessionLocal() as session:
        session.add(property_param)
        await session.commit()

    
    model_params = {
        "name": "Test Model",
        "description": "Test Description",
        "type_model": "Test Type",
        "block_id": block.id,
        "file_path": "uploads/test_asyncaws.py",
        "file_name": 'tesfsdft',
        "file_hash": 'afasfashfgf'
    }

    sensors = [
        {
            "measurement_source_id": 1,
            "sensor_item_id": 1,
        }
    ]

    properties = [property_param.id]
    async with AsyncSessionLocal() as session:
        new_id = await storage.add_block_params(
            model_params=model_params, sensors=sensors, properties=properties, source_blocks=[], session=session
        )
        await session.commit()
    print(f"TEST ID {new_id}")
    assert new_id is not None
    await engine.dispose()
    async with AsyncSessionLocal() as session:
        added_model = await session.execute(select(ModelsModel).where(ModelsModel.id==new_id))
    added_model = added_model.scalars().first()
    assert added_model.name == "Test Model"
    assert added_model.description == "Test Description"
    assert added_model.type == "Test Type"
    
    async with AsyncSessionLocal() as session:
        await session.execute(delete(PredictionModel))
        await session.execute(delete(ModelMappingModel))
        await session.execute(delete(ModelsModel))
        await session.execute(delete(FileModel))
        await session.execute(delete(PropertyModel))
        await session.execute(delete(BlockModel))
        await session.execute(delete(MeasurementModel))
        await session.commit()
    
    await engine.dispose()
    del os.environ["TESTING"]

@pytest.mark.asyncio
async def test_successful_block_activation_toggle():
    """Тест на изменение состояния блока"""
    os.environ["TESTING"] = "True"
    await engine.dispose()
    
    storage = MySQLStorage()
    block = BlockModel(name="test4", active=True)
    async with AsyncSessionLocal() as session:
        session.add(block)
        await session.commit()

    async with AsyncSessionLocal() as session:
        await storage.toggle_block(block.id, session=session)
        await session.commit()
    async with AsyncSessionLocal() as session:    
        get_block = await session.execute(select(BlockModel).where(BlockModel.id==block.id))
    get_block = get_block.scalars().first()
    assert get_block.active == False
    
    async with AsyncSessionLocal() as session:
        await session.execute(delete(PredictionModel))
        await session.execute(delete(ModelMappingModel))
        await session.execute(delete(ModelsModel))
        await session.execute(delete(FileModel))
        await session.execute(delete(PropertyModel))
        await session.execute(delete(BlockModel))
        await session.execute(delete(MeasurementModel))
        await session.commit()
    
    await engine.dispose()
    del os.environ["TESTING"]

@pytest.mark.asyncio
async def test_toggle_nonexistent_block_activation():
    os.environ["TESTING"] = "True"
    await engine.dispose()
    """Тест на изменение состояния несуществующего блока"""
    storage = MySQLStorage()
    async with AsyncSessionLocal() as session:
        response = await storage.toggle_block(99999, session=session)
    assert response["status_code"] == 404
    
    async with AsyncSessionLocal() as session:
        await session.execute(delete(PredictionModel))
        await session.execute(delete(ModelMappingModel))
        await session.execute(delete(ModelsModel))
        await session.execute(delete(FileModel))
        await session.execute(delete(PropertyModel))
        await session.execute(delete(BlockModel))
        await session.execute(delete(MeasurementModel))
        await session.commit()
    
    await engine.dispose()
    del os.environ["TESTING"]


@pytest.mark.asyncio
async def test_successful_retrieval_of_model_by_id():
    """Тест на успешное получение модели по ее ID из БД"""
    os.environ["TESTING"] = "True"
    await engine.dispose()
    
    storage = MySQLStorage()
    block = BlockModel(name="test5", active=True)
    async with AsyncSessionLocal() as session:
        session.add(block)
        await session.commit()
    new_file = FileModel(
        description="description",
        path=r"C:\Users\boiko.k.v\Desktop\Carbon-Digital-Twin\SDMODULE\tests\conftest.py",
        filename='test',
        filehash='gawfawf'
    )
    async with AsyncSessionLocal() as session:
        session.add(new_file)
        await session.commit()
        
    model = ModelsModel(
        name="test_model",
        description="Test description",
        type="test_type",
        block_id=block.id,
        file_id=new_file.id
    )
    async with AsyncSessionLocal() as session:
        session.add(model)
        await session.commit()

    async with AsyncSessionLocal() as session:
        response = await storage.get_model(model.id, session=session)
    assert response["status_code"] == 200
    
    async with AsyncSessionLocal() as session:
        await session.execute(delete(PredictionModel))
        await session.execute(delete(ModelMappingModel))
        await session.execute(delete(ModelsModel))
        await session.execute(delete(FileModel))
        await session.execute(delete(PropertyModel))
        await session.execute(delete(BlockModel))
        await session.execute(delete(MeasurementModel))
        await session.commit()
    
    await engine.dispose()
    del os.environ["TESTING"]


@pytest.mark.asyncio
async def test_retrieval_of_model_with_nonexistent_id():
    """Тест на получение несуществующей модели по ее ID из БД"""
    os.environ["TESTING"] = "True"
    await engine.dispose()
    
    storage = MySQLStorage()
    async with AsyncSessionLocal() as session:
        response = await storage.get_model(999999, session=session)
    assert response["status_code"] == 404
    
    await engine.dispose()
    del os.environ["TESTING"]


@pytest.mark.asyncio
async def test_successful_retrieval_of_predictions_by_block():
    """Тест на успешное получение предсказаний для определенного блока из БД"""
    os.environ["TESTING"] = "True"
    await engine.dispose()
    
    storage = MySQLStorage()
    block = BlockModel(name="test6", active=True)
    async with AsyncSessionLocal() as session:
        session.add(block)
        await session.commit()

    property_param = PropertyModel(name="test", unit="test")
    async with AsyncSessionLocal() as session:
        session.add(property_param)
        await session.commit()

    prediction = PredictionModel(
        query_id=str(uuid.uuid4()),
        block_id=block.id,
        insert_ts=datetime.utcnow().timestamp(),
        m_data=1,
        property_id=property_param.id,
    )
    async with AsyncSessionLocal() as session:
        session.add(prediction)
        await session.commit()

    async with AsyncSessionLocal() as session:
        response = await storage.get_predictions(block.id, property_param.id, 1, session=session)
    assert type(response) is list
    assert len(response) == 1
    
    async with AsyncSessionLocal() as session:
        await session.execute(delete(PredictionModel))
        await session.execute(delete(ModelMappingModel))
        await session.execute(delete(ModelsModel))
        await session.execute(delete(FileModel))
        await session.execute(delete(PropertyModel))
        await session.execute(delete(BlockModel))
        await session.execute(delete(MeasurementModel))
        await session.commit()
    
    await engine.dispose()
    del os.environ["TESTING"]


@pytest.mark.asyncio
async def test_retrieval_of_predictions_for_nonexistent_block():
    """Тест на успешное получение предсказаний для несуществующего блока из БД"""
    os.environ["TESTING"] = "True"
    await engine.dispose()
    storage = MySQLStorage()
    async with AsyncSessionLocal() as session:
        response = await storage.get_predictions(99999, 10, 1, session=session)
    assert type(response) is dict
    assert response["status_code"] == 404
    
    await engine.dispose()
    del os.environ["TESTING"]

@pytest.mark.asyncio
async def test_successful_addition_of_new_prediction():
    """Тест на добавление предсказания в БД"""
    os.environ["TESTING"] = "True"
    await engine.dispose()
    
    storage = MySQLStorage()
    block = BlockModel(name="test6", active=True)
    async with AsyncSessionLocal() as session:
        session.add(block)
        await session.commit()

    property_param = PropertyModel(name="test", unit="test")
    async with AsyncSessionLocal() as session:
        session.add(property_param)
        await session.commit()

    new_prediction = PredictionPost(
        m_data=1, property_id=property_param.id, block_id=block.id
    )
    async with AsyncSessionLocal() as session:
        await storage.add_prediction(insert_ts=datetime.utcnow(), prediction=new_prediction, query_uuid=str(uuid.uuid4()), session=session)
        await session.commit()
        predictions = await session.execute(select(PredictionModel).where(PredictionModel.block_id==block.id))
    
    predictions = predictions.scalars().all()

    assert len(predictions) == 1
    assert predictions[-1].m_data == 1
    
    async with AsyncSessionLocal() as session:
        await session.execute(delete(PredictionModel))
        await session.execute(delete(ModelMappingModel))
        await session.execute(delete(ModelsModel))
        await session.execute(delete(FileModel))
        await session.execute(delete(PropertyModel))
        await session.execute(delete(BlockModel))
        await session.execute(delete(MeasurementModel))
        await session.commit()
    
    await engine.dispose()
    del os.environ["TESTING"]


@pytest.mark.asyncio
async def test_successful_addition_of_new_property():
    """Тест на успешное добавление свойств в БД"""
    os.environ["TESTING"] = "True"
    await engine.dispose()
    
    storage = MySQLStorage()
    property_data = PropertyPost(name="test1", unit="test1")
    async with AsyncSessionLocal() as session:
        new_property = await storage.add_property(property_data=property_data, session=session)

    assert new_property["status_code"] == 200
    async with AsyncSessionLocal() as session:
        property_check = await session.execute(select(PropertyModel).where(PropertyModel.id==new_property['added_id']))
    assert property_check.scalars().first() is not None
    
    async with AsyncSessionLocal() as session:
        await session.execute(delete(PredictionModel))
        await session.execute(delete(ModelMappingModel))
        await session.execute(delete(ModelsModel))
        await session.execute(delete(FileModel))
        await session.execute(delete(PropertyModel))
        await session.execute(delete(BlockModel))
        await session.execute(delete(MeasurementModel))
        await session.commit()
    
    await engine.dispose()
    del os.environ["TESTING"]


@pytest.mark.asyncio
async def test_successful_retrieval_of_all_properties():
    """Тест на успешное получения списка свойств из БД"""
    os.environ["TESTING"] = "True"
    await engine.dispose()
    storage = MySQLStorage()
    prop = PropertyModel(name="test_property", unit="unit")
    async with AsyncSessionLocal() as session:
        session.add(prop)
        await session.commit()

    async with AsyncSessionLocal() as session:
        response = await storage.get_properties(session=session)
    assert type(response) is list
    assert len(response) > 0
    assert response[-1].name == "test_property"
    
    async with AsyncSessionLocal() as session:
        await session.execute(delete(PredictionModel))
        await session.execute(delete(ModelMappingModel))
        await session.execute(delete(ModelsModel))
        await session.execute(delete(FileModel))
        await session.execute(delete(PropertyModel))
        await session.execute(delete(BlockModel))
        await session.execute(delete(MeasurementModel))
        await session.commit()
    
    await engine.dispose()
    del os.environ["TESTING"]
