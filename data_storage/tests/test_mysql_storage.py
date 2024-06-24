import pytest
from datetime import datetime
from data_storage.mysql_storage import MySQLStorage

from network_models.measurements_info import MeasurementsGet
from network_models.measurement_source_info import MeasurementSourceInfoGet

from pydantic_core._pydantic_core import ValidationError
from typing import List

import requests

from data_storage.orm import (
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


def test_add_measurement(session):
    storage = MySQLStorage()
    measurement = MeasurementsGet(
        m_data=1,
        sensor_item_id=1,
        measurement_source_id=1,
    )
    insert_ts = datetime.now()
    storage.add_measurement(measurement, insert_ts)

    result = session.query(MeasurementModel).filter_by(sensor_item_id=1).first()
    assert result is not None
    assert result.m_data == 1
    assert result.sensor_item_id == 1
    assert result.measurement_source_id == 1


def test_add_measurement_err_insert_ts(session):
    storage = MySQLStorage()
    measurement = MeasurementsGet(
        m_data=1,
        sensor_item_id=1,
        measurement_source_id=1,
    )
    insert_ts = None
    with pytest.raises(AttributeError) as excinfo:
        storage.add_measurement(measurement, insert_ts)


def test_add_measurement_err_m_data(session):
    storage = MySQLStorage()
    with pytest.raises(ValidationError) as excinfo:
        measurement = MeasurementsGet(
            m_data=None,
            sensor_item_id=1,
            measurement_source_id=1,
        )
        insert_ts = datetime.now()
        storage.add_measurement(measurement, insert_ts)


def test_add_measurement_err_sensor_item_id(session):
    storage = MySQLStorage()
    with pytest.raises(ValidationError) as excinfo:
        measurement = MeasurementsGet(
            m_data=1,
            sensor_item_id=None,
            measurement_source_id=1,
        )
        insert_ts = datetime.now()
        storage.add_measurement(measurement, insert_ts)


def test_add_measurement_err_measurement_source_id(session):
    storage = MySQLStorage()
    with pytest.raises(ValidationError) as excinfo:
        measurement = MeasurementsGet(
            m_data=1,
            sensor_item_id=1,
            measurement_source_id=None,
        )
        insert_ts = datetime.now()
        storage.add_measurement(measurement, insert_ts)


def test_get_last_three_measurements_for_sources(session):
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
    insert_ts = datetime.now()
    storage.add_measurement(measurement1, insert_ts)
    storage.add_measurement(measurement2, insert_ts)

    result = storage.get_last_three_measurements_for_sources([1])
    assert len(result) == 2
    assert result[0].m_data == 2
    assert result[1].m_data == 3


def test_get_last_three_measurements_for_sources_err(session):
    storage = MySQLStorage()
    result = storage.get_last_three_measurements_for_sources([6435])
    assert len(result) == 0


def test_get_measurements_sources(session):
    storage = MySQLStorage()
    result = storage.get_measurement_sources()
    assert len(result) == 8
    assert type(result) is list


def test_patch_sensor(session):
    storage = MySQLStorage()
    result = storage.toggle_sensor_activation(1, True)
    sensor = session.query(SensorItemModel).filter_by(id=1).first()
    assert sensor.is_active == True


def test_toggle_nonexistent_sensor_activation(session):
    storage = MySQLStorage()
    result = storage.toggle_sensor_activation(999999, True)
    sensor = session.query(SensorItemModel).filter_by(id=1).first()
    assert sensor.is_active == True


def test_successful_block_list_retrieval(session):
    storage = MySQLStorage()
    block = BlockModel(name="test", active=True)
    session.add(block)
    session.commit()

    list_blocks = storage.get_block_list(need_active=True)
    assert len(list_blocks) == 1
    assert list_blocks[0].name == "test"
    session.delete(block)
    session.commit()


def test_block_list_retrieval_with_activity_filter(session):
    storage = MySQLStorage()
    active_block = BlockModel(name="test1", active=True)
    inactive_block = BlockModel(name="test2", active=False)
    session.add_all([active_block, inactive_block])
    session.commit()

    list_blocks = storage.get_block_list(need_active=True)
    assert len(list_blocks) == 1
    assert list_blocks[0].name == "test1"
    session.delete(active_block)
    session.delete(inactive_block)
    session.commit()


def test_add_block_params(session):
    storage = MySQLStorage()
    block = BlockModel(name="test", active=True)
    session.add(block)
    session.commit()

    property_param = PropertyModel(name="test", unit="test")
    session.add(property_param)
    session.commit()

    model_params = {
        "name": "Test Model",
        "description": "Test Description",
        "type_model": "Test Type",
        "block_id": block.id,
        "file_path": r"C:\Users\boiko.k.v\Desktop\CarbonDigitalTwin\data_storage\README.md",
    }

    sensors = [
        {
            "measurement_source_id": 1,
            "sensor_item_id": 1,
        }
    ]

    properties = [property_param.id]
    print(f"TEST ADD BLOCK PARAMS")
    new_id = storage.add_block_params(
        model_params=model_params, sensors=sensors, properties=properties
    )
    session.commit()
    print(f"TEST ID {new_id}")
    assert new_id is not None
    added_model = session.query(ModelsModel).get(new_id)
    assert added_model.name == "Test Model"
    assert added_model.description == "Test Description"
    assert added_model.type == "Test Type"


@pytest.mark.parametrize(
    "missing_field", ["name", "description", "type_model", "file_path", "block_id"]
)
def test_block_parameter_addition_missing_fields(missing_field, session):
    storage = MySQLStorage()
    block = BlockModel(name="test3", active=True)
    session.add(block)
    session.commit()

    model_params = {
        "name": "Test Model",
        "description": "Test Description",
        "type_model": "Test Type",
        "block_id": block.id,
        "file_path": r"C:\Users\boiko.k.v\Desktop\CarbonDigitalTwin\data_storage\README.md",
    }
    del model_params[missing_field]

    sensors = [
        {
            "measurement_source_id": 1,
            "sensor_item_id": 1,
        }
    ]

    properties = [1]
    print(f"TEST ADD BLOCK PARAMS WITHOUT {missing_field}")

    with pytest.raises(KeyError) as excinfo:
        new_id = storage.add_block_params(
            model_params=model_params, sensors=sensors, properties=properties
        )
    session.commit()

    session.delete(block)
    session.commit()


def test_successful_block_activation_toggle(session):
    storage = MySQLStorage()
    block = BlockModel(name="test4", active=True)
    session.add(block)
    session.commit()

    storage.toggle_block(block.id)
    session.commit()
    assert session.get(BlockModel, block.id).active == False
    session.delete(block)
    session.commit()


def test_toggle_nonexistent_block_activation(session):
    storage = MySQLStorage()
    response = storage.toggle_block(99999)
    assert response["status_code"] == 404
