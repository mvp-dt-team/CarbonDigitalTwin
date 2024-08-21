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

# Тесты для функций добавления данных

async def initial(async_db_session: AsyncSession):
    pass


@pytest.mark.asyncio
async def test_add_measurement(async_db_session):
    """Тест на добавление измерения в БД"""
    session = await async_db_session.__anext__()
    storage = MySQLStorage()
    measurement = MeasurementsGet(
        m_data=1,
        sensor_item_id=1,
        measurement_source_id=1,
    )
    insert_ts = datetime.now()
    await storage.add_measurement(measurement, insert_ts, query_uuid=str(uuid.uuid4()))

    result = await session.execute(select(MeasurementModel).where(MeasurementModel.sensor_item_id==1))
    result = result.scalars().first()
    await session.close()

    assert result is not None
    assert result.m_data == 1
    assert result.sensor_item_id == 1
    assert result.measurement_source_id == 1


@pytest.mark.asyncio
async def test_add_measurement_err_insert_ts(async_db_session):
    """Тест на добавление измерения в БД без вставки времени"""
    storage = MySQLStorage()
    measurement = MeasurementsGet(
        m_data=1,
        sensor_item_id=1,
        measurement_source_id=1,
    )
    insert_ts = None
    with pytest.raises(AttributeError) as excinfo:
        await storage.add_measurement(measurement, insert_ts, query_uuid=str(uuid.uuid4()))


@pytest.mark.asyncio
async def test_add_measurement_err_m_data(async_db_session):
    """Тест на добавление измерения в БД без вставки данных измерения"""
    storage = MySQLStorage()
    with pytest.raises(ValidationError) as excinfo:
        measurement = MeasurementsGet(
            m_data=None,
            sensor_item_id=1,
            measurement_source_id=1,
        )
        insert_ts = datetime.now()
        await storage.add_measurement(measurement, insert_ts, query_uuid=str(uuid.uuid4()))


@pytest.mark.asyncio
async def test_add_measurement_err_sensor_item_id(async_db_session):
    """Тест на добавление измерения в БД без вставки ID датчика"""
    storage = MySQLStorage()
    with pytest.raises(ValidationError) as excinfo:
        measurement = MeasurementsGet(
            m_data=1,
            sensor_item_id=None,
            measurement_source_id=1,
        )
        insert_ts = datetime.now()
        await storage.add_measurement(measurement, insert_ts, query_uuid=str(uuid.uuid4()))

@pytest.mark.asyncio
async def test_add_measurement_err_measurement_source_id(async_db_session):
    """Тест на добавление измерения в БД без вставки ID точки измерения"""
    storage = MySQLStorage()
    with pytest.raises(ValidationError) as excinfo:
        measurement = MeasurementsGet(
            m_data=1,
            sensor_item_id=1,
            measurement_source_id=None,
        )
        insert_ts = datetime.now()
        await storage.add_measurement(measurement, insert_ts, query_uuid=str(uuid.uuid4()))


@pytest.mark.asyncio
async def test_get_last_three_measurements_for_sources(async_db_session):
    """Тест на получения последних трех измерений из БД"""
    storage = MySQLStorage()
    session = await async_db_session.__anext__()
    
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
    insert_ts = datetime.now()
    await storage.add_measurement(measurement1, insert_ts)
    await storage.add_measurement(measurement2, insert_ts)

    result = await storage.get_last_three_measurements_for_sources([1])
    await session.close()
    assert len(result) == 2
    assert result[0].m_data == 2
    assert result[1].m_data == 3


# def test_get_last_three_measurements_for_sources_err(session):
#     """Тест на получения последних трех измерений из БД"""
#     storage = MySQLStorage()
#     result = storage.get_last_three_measurements_for_sources([6435])
#     assert len(result) == 0


# def test_get_measurements_sources(session):
#     """Тест на получения всех источников измерений из БД"""
#     storage = MySQLStorage()
#     result = storage.get_measurement_sources()
#     assert len(result) == 8
#     assert type(result) is list


# def test_patch_sensor(session):
#     """Тест на изменение состояния датчика"""
#     storage = MySQLStorage()
#     result = storage.toggle_sensor_activation(1, True)
#     sensor = session.query(SensorItemModel).filter_by(id=1).first()
#     assert sensor.is_active == True


# def test_toggle_nonexistent_sensor_activation(session):
#     """Тест на изменение состояния несуществующего датчика"""
#     storage = MySQLStorage()
#     result = storage.toggle_sensor_activation(999999, True)
#     sensor = session.query(SensorItemModel).filter_by(id=1).first()
#     assert sensor.is_active == True


# def test_successful_block_list_retrieval(session):
#     """Тест получение списка блоков из БД"""
#     storage = MySQLStorage()
#     block = BlockModel(name="test", active=True)
#     session.add(block)
#     session.commit()

#     list_blocks = storage.get_block_list(need_active=True)
#     assert len(list_blocks) == 1
#     assert list_blocks[0].name == "test"
#     session.delete(block)
#     session.commit()


# def test_block_list_retrieval_with_activity_filter(session):
#     """Тест получение списка блоков из БД с фильтром активности"""
#     storage = MySQLStorage()
#     active_block = BlockModel(name="test1", active=True)
#     inactive_block = BlockModel(name="test2", active=False)
#     session.add_all([active_block, inactive_block])
#     session.commit()

#     list_blocks = storage.get_block_list(need_active=True)
#     assert len(list_blocks) == 1
#     assert list_blocks[0].name == "test1"
#     session.delete(active_block)
#     session.delete(inactive_block)
#     session.commit()


# def test_add_block_params(session):
#     """Тест на добавление параметров к блоку"""
#     storage = MySQLStorage()
#     block = BlockModel(name="test", active=True)
#     session.add(block)
#     session.commit()

#     property_param = PropertyModel(name="test", unit="test")
#     session.add(property_param)
#     session.commit()

#     model_params = {
#         "name": "Test Model",
#         "description": "Test Description",
#         "type_model": "Test Type",
#         "block_id": block.id,
#         "file_path": r"C:\Users\boiko.k.v\Desktop\CarbonDigitalTwin\data_storage\README.md",
#     }

#     sensors = [
#         {
#             "measurement_source_id": 1,
#             "sensor_item_id": 1,
#         }
#     ]

#     properties = [property_param.id]
#     print(f"TEST ADD BLOCK PARAMS")
#     new_id = storage.add_block_params(
#         model_params=model_params, sensors=sensors, properties=properties
#     )
#     session.commit()
#     print(f"TEST ID {new_id}")
#     assert new_id is not None
#     added_model = session.query(ModelsModel).get(new_id)
#     assert added_model.name == "Test Model"
#     assert added_model.description == "Test Description"
#     assert added_model.type == "Test Type"


# @pytest.mark.parametrize(
#     "missing_field", ["name", "description", "type_model", "file_path", "block_id"]
# )
# def test_block_parameter_addition_missing_fields(missing_field, session):
#     f"""Тест на добавление параметров к блоку без поля {missing_field}"""
#     storage = MySQLStorage()
#     block = BlockModel(name="test3", active=True)
#     session.add(block)
#     session.commit()

#     model_params = {
#         "name": "Test Model",
#         "description": "Test Description",
#         "type_model": "Test Type",
#         "block_id": block.id,
#         "file_path": r"C:\Users\boiko.k.v\Desktop\CarbonDigitalTwin\data_storage\README.md",
#     }
#     del model_params[missing_field]

#     sensors = [
#         {
#             "measurement_source_id": 1,
#             "sensor_item_id": 1,
#         }
#     ]

#     properties = [1]

#     with pytest.raises(KeyError) as excinfo:
#         new_id = storage.add_block_params(
#             model_params=model_params, sensors=sensors, properties=properties
#         )
#     session.commit()

#     session.delete(block)
#     session.commit()


# def test_successful_block_activation_toggle(session):
#     """Тест на изменение состояния блока"""
#     storage = MySQLStorage()
#     block = BlockModel(name="test4", active=True)
#     session.add(block)
#     session.commit()

#     storage.toggle_block(block.id)
#     session.commit()
#     assert session.get(BlockModel, block.id).active == False
#     session.delete(block)
#     session.commit()


# def test_toggle_nonexistent_block_activation(session):
#     """Тест на изменение состояния несуществующего блока"""
#     storage = MySQLStorage()
#     response = storage.toggle_block(99999)
#     assert response["status_code"] == 404


# def test_successful_retrieval_of_model_by_id(session):
#     """Тест на успешное получение модели по ее ID из БД"""
#     storage = MySQLStorage()
#     block = BlockModel(name="test5", active=True)
#     session.add(block)
#     session.commit()
#     new_file = FileModel(
#         description="description",
#         path=r"C:\Users\boiko.k.v\Desktop\CarbonDigitalTwin\data_storage\README.md",
#     )
#     session.add(new_file)
#     session.commit()
#     model = ModelsModel(
#         name="test_model",
#         description="Test description",
#         type="test_type",
#         block_id=block.id,
#         file_id=new_file.id,
#     )
#     session.add(model)
#     session.commit()

#     response = storage.get_model(model.id)
#     assert response["status_code"] == 200


# def test_retrieval_of_model_with_nonexistent_id(session):
#     """Тест на получение несуществующей модели по ее ID из БД"""
#     storage = MySQLStorage()
#     response = storage.get_model(999999)
#     assert response["status_code"] == 404


# def test_successful_retrieval_of_predictions_by_block(session):
#     """Тест на успешное получение предсказаний для определенного блока из БД"""
#     storage = MySQLStorage()
#     block = BlockModel(name="test6", active=True)
#     session.add(block)
#     session.commit()

#     property_param = PropertyModel(name="test", unit="test")
#     session.add(property_param)
#     session.commit()

#     prediction = PredictionModel(
#         block_id=block.id,
#         insert_ts=datetime.utcnow().timestamp(),
#         m_data=1,
#         property_id=property_param.id,
#     )
#     session.add(prediction)
#     session.commit()

#     response = storage.get_predictions(block.id, 10)
#     assert type(response) is list
#     assert len(response) == 1


# def test_retrieval_of_predictions_for_nonexistent_block(session):
#     """Тест на успешное получение предсказаний для несуществующего блока из БД"""
#     storage = MySQLStorage()

#     response = storage.get_predictions(99999, 10)
#     assert type(response) is dict
#     assert response["status_code"] == 404


# def test_successful_addition_of_new_prediction(session):
#     """Тест на добавление предсказания в БД"""
#     storage = MySQLStorage()
#     block = BlockModel(name="test6", active=True)
#     session.add(block)
#     session.commit()

#     property_param = PropertyModel(name="test", unit="test")
#     session.add(property_param)
#     session.commit()

#     new_prediction = PredictionPost(
#         m_data=1, property_id=property_param.id, block_id=block.id
#     )
#     storage.add_prediction(insert_ts=datetime.utcnow(), prediction=new_prediction)
#     session.commit()
#     predictions = session.query(PredictionModel).filter_by(block_id=block.id).all()

#     assert len(predictions) == 1
#     assert predictions[-1].m_data == 1


# @pytest.mark.parametrize("missing_field", ["m_data", "property_id", "block_id"])
# def test_addition_of_prediction_with_missing_fields(missing_field, session):
#     f"""Тест на добавление предсказания в БД без поля f{missing_field}"""
#     new_prediction_model = {
#         "block_id": 1,
#         "time_inserted": str(datetime.utcnow()),
#         "m_data": "some_data",
#         "property_id": 1,
#     }
#     del new_prediction_model[missing_field]

#     with pytest.raises(KeyError) as excinfo:
#         new_prediction = PredictionPost(
#             m_data=new_prediction_model["m_data"],
#             property_id=new_prediction_model["property_id"],
#             block_id=new_prediction_model["block_id"],
#         )


# @pytest.mark.models
# def test_successful_addition_of_new_property(session):
#     """Тест на успешное добавление свойств в БД"""
#     storage = MySQLStorage()
#     property_data = PropertyPost(name="test1", unit="test1")
#     new_property = storage.add_property(property_data=property_data)
#     session.commit()

#     assert new_property["status_code"] == 200
#     assert session.get(PropertyModel, new_property["added_id"]) is not None


# @pytest.mark.models
# def test_successful_retrieval_of_all_properties(session):
#     """Тест на успешное получения списка свойств из БД"""
#     storage = MySQLStorage()
#     prop = PropertyModel(name="test_property", unit="unit")
#     session.add(prop)
#     session.commit()

#     response = storage.get_properties()
#     assert type(response) is list
#     assert len(response) > 0
#     assert response[-1].name == "test_property"
