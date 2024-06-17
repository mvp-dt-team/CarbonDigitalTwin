import pytest
from datetime import datetime
from data_storage.mysql_storage import MySQLStorage

from network_models.measurements_info import MeasurementsGet
from network_models.measurement_source_info import MeasurementSourceInfoGet

from pydantic_core._pydantic_core import ValidationError
from typing import List

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