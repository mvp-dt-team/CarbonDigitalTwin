from datetime import datetime
from typing import List
from mysql.connector import connect
from sqlalchemy import create_engine, desc
from functools import wraps
from sqlalchemy.orm import sessionmaker, Session
from data_storage.orm import SensorModel, MeasurementSourceModel, SensorItemModel, SensorSourceMappingModel, SensorParamsModel, RawDataModel, MeasurementModel

from network_models.measurement_source_info import MeasurementSourceInfo
from network_models.measurements_info import Measurement
from network_models.sensor_model_info import SensorModelInfo
from network_models.sensors_info import SensorInfo, SensorProperty

from config_reader import config

def sqlalchemy_session(engine_url):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Создание соединения с базой данных
            engine = create_engine(engine_url)
            Session = sessionmaker(bind=engine)
            session = Session()

            try:
                # Вызов функции с передачей сессии в качестве аргумента
                result = func(*args, session=session, **kwargs)
                session.commit()  # Фиксация всех изменений в базе данных
                return result
            except Exception as e:
                session.rollback()  # Отмена всех изменений в случае ошибки
                raise e
            finally:
                session.close()  # Закрытие сессии после завершения работы

        return wrapper
    return decorator


class MySQLStorage():
    engine_url = f'mysql+pymysql://{config.USER}:{config.PASSWORD.get_secret_value()}@{config.HOST}:3306/{config.DATABASE}'
    def close(self):
        self.mysql_connection.close()

    def __init__(self) -> None:
        pass
    @sqlalchemy_session(engine_url)
    def add_measurement(self, measurement: Measurement, query_id: int, insert_ts: datetime, session: Session) -> None:
            measurement_new = MeasurementModel(
                query_id=query_id,
                insert_ts=int(insert_ts.timestamp()),
                m_data=measurement.m_data,
                sensor_item_id=measurement.sensor_item_id,
                measurement_source_id=measurement.measurement_source_id
            )
            session.add(measurement_new)

    @sqlalchemy_session(engine_url)
    def get_last_three_measurements_for_sources(self, measurement_source_ids: List[int], session: Session) -> List[Measurement]:
        measurements = []
        for source_id in measurement_source_ids:
            result = session.query(MeasurementModel)\
                            .filter(MeasurementModel.measurement_source_id == source_id)\
                            .order_by(desc(MeasurementModel.insert_ts))\
                            .limit(3)\
                            .all()
            result = [Measurement(m_data=result_data.m_data, sensor_item_id=result_data.sensor_item_id, measurement_source_id=result_data.measurement_source_id, insert_ts=result_data.insert_ts) for result_data in result]
            measurements.extend(result)
        return measurements

    # MEASUREMENT SOURCE ########################

    @sqlalchemy_session(engine_url)
    def get_measurement_sources(self, session: Session) -> List[MeasurementSourceInfo]:
        sources_data = session.query(MeasurementSourceModel).all()
        sources = [
            MeasurementSourceInfo(
                id=source.id,
                name=source.name,
                description=source.description,
                unit=source.units
            ) for source in sources_data
        ]
        return sources

    @sqlalchemy_session(engine_url)
    def add_measurement_source(self, source: MeasurementSourceInfo, session: Session) -> None:
        new_source = MeasurementSourceModel(
            name=source.name,
            description=source.description,
            units=source.unit
        )
        session.add(new_source)


    # SENSORS ##############
    @sqlalchemy_session(engine_url)
    def get_sensors_models(self, session) -> List[SensorModelInfo]:
        models_data = session.query(SensorModel).all()
        models = [
            SensorModelInfo(
                id=model.id,
                name=model.name,
                description=model.description
            ) for model in models_data
        ]
        return models

    @sqlalchemy_session(engine_url)
    def add_sensor_model(self, model: SensorModelInfo, session) -> None:
        new_model = SensorModel(
            name=model.name,
            description=model.description
        )
        session.add(new_model)


    @sqlalchemy_session(engine_url)
    def get_sensors_info(self, need_active: bool, session) -> List[SensorInfo]:
        query = session.query(SensorItemModel)
        if need_active:
            query = query.filter(SensorItemModel.is_active == True)
        
        sensors_data = query.all()
        sensors: List[SensorInfo] = []

        for raw_sensor in sensors_data:
            sensor_id = raw_sensor.id
            sensor_type = raw_sensor.sensor_type
            is_active = raw_sensor.is_active
            addition_info = raw_sensor.addition_info
            model_id = raw_sensor.sensor_id

            parameters_query = session.query(SensorParamsModel).filter(SensorParamsModel.sensor_item_id == sensor_id).all()
            sensor_parameters = {param.param_name: param.param_value for param in parameters_query if param.property_id is None}

            properties_query = session.query(MeasurementSourceModel.id, MeasurementSourceModel.name, MeasurementSourceModel.units)\
                                    .join(SensorSourceMappingModel, MeasurementSourceModel.id == SensorSourceMappingModel.measurement_source_id)\
                                    .filter(SensorSourceMappingModel.sensor_item_id == sensor_id)\
                                    .all()
            
            props: List[SensorProperty] = []
            for property_id, property_name, property_units in properties_query:
                property_parameters = {param.param_name: param.param_value for param in parameters_query if param.property_id == property_id}
                props.append(SensorProperty(measurement_source_id=property_id, name=property_name, unit=property_units, parameters=property_parameters))

            sensors.append(SensorInfo(id=sensor_id, parameters=sensor_parameters, type=sensor_type, properties=props, is_active=is_active, description=addition_info, sensor_model_id=model_id))
        
        return sensors


    @sqlalchemy_session(engine_url)
    def add_sensor(self, sensor: SensorInfo, session):
        # Добавляем новый sensor_item
        new_sensor_item = SensorItemModel(
            sensor_id=sensor.sensor_model_id,
            is_active=True,
            sensor_type=sensor.type,
            addition_info=sensor.description
        )
        session.add(new_sensor_item)
        session.flush()  # Применяем изменения, чтобы получить id нового sensor_item

        # Добавляем в sensor_source_mapping
        for prop in sensor.properties:
            new_sensor_source_mapping = SensorSourceMappingModel(
                measurement_source_id=prop.measurement_source_id,
                sensor_item_id=new_sensor_item.id
            )
            session.add(new_sensor_source_mapping)

        # Добавляем в sensor_params
        for param_name, param_value in sensor.parameters.items():
            new_sensor_param = SensorParamsModel(
                sensor_item_id=new_sensor_item.id,
                property_id=None,
                param_name=param_name,
                param_value=param_value
            )
            session.add(new_sensor_param)

        for prop in sensor.properties:
            for param_name, param_value in prop.parameters.items():
                new_sensor_param = SensorParamsModel(
                    sensor_item_id=new_sensor_item.id,
                    property_id=prop.measurement_source_id,
                    param_name=param_name,
                    param_value=param_value
                )
                session.add(new_sensor_param)

    @sqlalchemy_session(engine_url)
    def toggle_sensor_activation(self, sensor_item_id: int, is_active: bool, session):
        session.query(SensorItemModel).filter(SensorItemModel.id == sensor_item_id).update({SensorItemModel.is_active: is_active})
