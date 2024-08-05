from datetime import datetime
from typing import List
from sqlalchemy import create_engine, desc
from functools import wraps
from sqlalchemy.orm import sessionmaker, Session
from orm import (
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

from network_models.measurement_source_info import (
    MeasurementSourceInfoGet,
    MeasurementSourceInfoPost,
)
from network_models.measurements_info import MeasurementsGet
from network_models.sensor_model_info import SensorModelInfoPost, SensorModelInfoGet
from network_models.sensors_info import SensorInfoGet, SensorInfoPost, SensorPropertyGet
from network_models.blocks import (
    ModelMappingGet,
    PropertyGet,
    MLModelGet,
    BlockModelGet,
    SensorBlockinfo,
    BlockModelPost,
    PropertyPost,
    PredictionGet,
    PredictionPost,
)


from yaml import load
from yaml.loader import SafeLoader
with open('config.yaml', 'r') as config_file:
    config = load(config_file, Loader=SafeLoader)

import logging
import os

logger = logging.getLogger("DataStorageModule")

UPLOAD_DIR = os.path.abspath("./uploads")


def sqlalchemy_session(engine_url):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Создание соединения с базой данных
            engine = create_engine(engine_url)
            session_current = sessionmaker(bind=engine)
            session = session_current()

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


class MySQLStorage:
    engine_url = f"mysql+pymysql://{config['USER']}:{config['PASSWORD']}@{config['HOST']}:3306/{config['DB']}"
    
    # FOR TESTING !
    # engine_url = f'sqlite:///app.db'
    # def close(self):
    #     self.mysql_connection.close()

    def __init__(self) -> None:
        logger.debug("module starting")

    @sqlalchemy_session(engine_url)
    def add_measurement(
        self, measurement: MeasurementsGet, insert_ts: datetime, session: Session
    ) -> None:
        measurement_new = MeasurementModel(
            insert_ts=int(insert_ts.timestamp()),
            m_data=measurement.m_data,
            sensor_item_id=measurement.sensor_item_id,
            measurement_source_id=measurement.measurement_source_id,
        )
        session.add(measurement_new)
        logger.info(
            f"Added measurement sensor_item_id = {measurement_new.sensor_item_id}, m_data = {measurement_new.m_data}"
        )

    @sqlalchemy_session(engine_url)
    def get_last_three_measurements_for_sources(
        self, measurement_source_ids: List[int], session: Session
    ) -> List[MeasurementsGet]:
        measurements = []
        for source_id in measurement_source_ids:
            result = (
                session.query(MeasurementModel)
                .filter(MeasurementModel.measurement_source_id == source_id)
                .order_by(desc(MeasurementModel.insert_ts))
                .limit(3)
                .all()
            )
            result = [
                MeasurementsGet(
                    m_data=result_data.m_data,
                    sensor_item_id=result_data.sensor_item_id,
                    measurement_source_id=result_data.measurement_source_id,
                    insert_ts=result_data.insert_ts,
                )
                for result_data in result
            ]
            measurements.extend(result)
            logger.info(f"Get measurements {measurements}")
        return measurements

    # MEASUREMENT SOURCE ########################

    @sqlalchemy_session(engine_url)
    def get_measurement_sources(
        self, session: Session
    ) -> List[MeasurementSourceInfoGet]:
        sources_data = session.query(MeasurementSourceModel).all()
        sources = [
            MeasurementSourceInfoGet(
                id=source.id,
                name=source.name,
                description=source.description,
                unit=source.units,
            )
            for source in sources_data
        ]
        logger.info(f"Get measurement sources {sources}")
        return sources

    @sqlalchemy_session(engine_url)
    def add_measurement_source(
        self, source: MeasurementSourceInfoPost, session: Session
    ) -> None:
        new_source = MeasurementSourceModel(
            name=source.name, description=source.description, units=source.unit
        )
        session.add(new_source)
        logger.info(f"Add measurement sources {new_source}")

    # SENSORS ##############
    @sqlalchemy_session(engine_url)
    def get_sensors_models(self, session) -> List[SensorModelInfoGet]:
        models_data = session.query(SensorModel).all()
        models = [
            SensorModelInfoGet(
                id=model.id, name=model.name, description=model.description
            )
            for model in models_data
        ]
        logger.info(f"Get sensors models {models}")
        return models

    @sqlalchemy_session(engine_url)
    def add_sensor_model(self, model: SensorModelInfoPost, session) -> None:
        new_model = SensorModel(name=model.name, description=model.description)
        session.add(new_model)
        logger.info(f"Add sensors model {new_model}")

    @sqlalchemy_session(engine_url)
    def get_sensors_info(self, need_active: bool, session) -> List[SensorInfoGet]:
        query = session.query(SensorItemModel)
        if need_active:
            query = query.filter(SensorItemModel.is_active == True)

        sensors_data = query.all()
        sensors: List[SensorInfoGet] = []

        for raw_sensor in sensors_data:
            sensor_id = raw_sensor.id
            sensor_type = raw_sensor.sensor_type
            is_active = raw_sensor.is_active
            addition_info = raw_sensor.addition_info
            model_id = raw_sensor.sensor_id

            parameters_query = (
                session.query(SensorParamsModel)
                .filter(SensorParamsModel.sensor_item_id == sensor_id)
                .all()
            )
            sensor_parameters = {
                param.param_name: param.param_value
                for param in parameters_query
                if param.property_id is None
            }

            properties_query = (
                session.query(
                    MeasurementSourceModel.id,
                    MeasurementSourceModel.name,
                    MeasurementSourceModel.units,
                )
                .join(
                    SensorSourceMappingModel,
                    MeasurementSourceModel.id
                    == SensorSourceMappingModel.measurement_source_id,
                )
                .filter(SensorSourceMappingModel.sensor_item_id == sensor_id)
                .all()
            )

            props: List[SensorPropertyGet] = []
            for property_id, property_name, property_units in properties_query:
                property_parameters = {
                    param.param_name: param.param_value
                    for param in parameters_query
                    if param.property_id == property_id
                }
                props.append(
                    SensorPropertyGet(
                        measurement_source_id=property_id,
                        name=property_name,
                        unit=property_units,
                        parameters=property_parameters,
                    )
                )

            sensors.append(
                SensorInfoGet(
                    id=sensor_id,
                    parameters=sensor_parameters,
                    type=sensor_type,
                    properties=props,
                    is_active=is_active,
                    description=addition_info,
                    sensor_model_id=model_id,
                )
            )

        logger.info(f"Getting sensors in the amount of {len(sensors)}")
        return sensors

    @sqlalchemy_session(engine_url)
    def add_sensor(self, sensor: SensorInfoPost, session):
        # Добавляем новый sensor_item
        new_sensor_item = SensorItemModel(
            sensor_id=sensor.sensor_model_id,
            is_active=True,
            sensor_type=sensor.type,
            addition_info=sensor.description,
        )
        session.add(new_sensor_item)
        session.flush()  # Применяем изменения, чтобы получить id нового sensor_item

        # Добавляем в sensor_source_mapping
        for prop in sensor.properties:
            new_sensor_source_mapping = SensorSourceMappingModel(
                measurement_source_id=prop.measurement_source_id,
                sensor_item_id=new_sensor_item.id,
            )
            session.add(new_sensor_source_mapping)

        # Добавляем в sensor_params
        for param_name, param_value in sensor.parameters.items():
            new_sensor_param = SensorParamsModel(
                sensor_item_id=new_sensor_item.id,
                property_id=None,
                param_name=param_name,
                param_value=param_value,
            )
            session.add(new_sensor_param)

        for prop in sensor.properties:
            for param_name, param_value in prop.parameters.items():
                new_sensor_param = SensorParamsModel(
                    sensor_item_id=new_sensor_item.id,
                    property_id=prop.measurement_source_id,
                    param_name=param_name,
                    param_value=param_value,
                )
                session.add(new_sensor_param)
        logger.info(f"Add new sensor {new_sensor_item}")

    @sqlalchemy_session(engine_url)
    def toggle_sensor_activation(self, sensor_item_id: int, is_active: bool, session):
        session.query(SensorItemModel).filter(
            SensorItemModel.id == sensor_item_id
        ).update({SensorItemModel.is_active: is_active})
        logger.info(f"Togled sensor status (id = {sensor_item_id})")
        return {"status": "ok"}

    ### MLMODULE

    @sqlalchemy_session(engine_url)
    def get_block_list(self, need_active: bool, session: Session):
        if need_active:
            blocks_data = (
                session.query(BlockModel).filter(BlockModel.active == need_active).all()
            )
        else:
            blocks_data = session.query(BlockModel).all()
        blocks = {}
        for block in blocks_data:
            model_list = (
                session.query(ModelsModel)
                .filter(ModelsModel.block_id == block.id)
                .all()
            )
            if len(model_list) > 0:
                block_model = model_list[-1]
                blocks[block] = [
                    ModelMappingGet(
                        measurement_source_id=x.measurement_source_id,
                        sensor_item_id=x.sensor_item_id,
                        model_id=x.model_id,
                        property_id=x.property_id,
                    )
                    for x in session.query(ModelMappingModel)
                    .filter(ModelMappingModel.model_id == block_model.id)
                    .all()
                ]
            else:
                blocks[block] = ModelMappingGet(
                    measurement_source_id=None,
                    sensor_item_id=None,
                    model_id=None,
                    property_id=None,
                )

        modelsmapping = []

        for block, content in blocks.items():
            if type(content) is not list:
                modelsmapping.append(
                    BlockModelGet(id=block.id, name=block.name, active=block.active)
                )
            else:
                sensors_set = set()
                for i in content:
                    sensors_set.add((i.measurement_source_id, i.sensor_item_id))
                sensors = [
                    SensorBlockinfo(
                        measurement_source_id=x[0],
                        sensor_item_id=x[1],
                    )
                    for x in sensors_set
                ]
                model_data = (
                    session.query(ModelsModel)
                    .filter(ModelsModel.id == content[0].model_id)
                    .first()
                )
                properties_ids = set([x.property_id for x in content])
                property_data = [
                    session.query(PropertyModel).filter(PropertyModel.id == x).first()
                    for x in properties_ids
                ]
                modelsmapping.append(
                    BlockModelGet(
                        id=block.id,
                        name=block.name,
                        sensors=sensors,
                        model=MLModelGet(
                            id=model_data.id,
                            name=model_data.name,
                            description=model_data.description,
                        ),
                        properties=[
                            PropertyGet(id=x.id, name=x.name, unit=x.unit)
                            for x in property_data
                        ],
                        active=block.active,
                    )
                )
        return modelsmapping

    @sqlalchemy_session(engine_url)
    def add_block_params(
        self,
        model_params: dict,
        sensors: List[dict],
        properties: List[int],
        session: Session,
    ):
        new_file = FileModel(
            description=model_params["description"], path=model_params["file_path"]
        )
        session.add(new_file)
        session.flush()

        new_model = ModelsModel(
            name=model_params["name"],
            description=model_params["description"],
            type=model_params["type_model"],
            file_id=new_file.id,
            block_id=model_params["block_id"],
        )
        session.add(new_model)
        session.flush()

        for sensor in sensors:
            for property in properties:
                model_map = ModelMappingModel(
                    measurement_source_id=sensor["measurement_source_id"],
                    sensor_item_id=sensor["sensor_item_id"],
                    model_id=new_model.id,
                    property_id=property,
                )
                session.add(model_map)

        logger.info(
            f"Add model, {len(sensors)} sensor and {len(properties)} properties to block"
        )
        return new_model.id

    @sqlalchemy_session(engine_url)
    def toggle_block(self, block_id: int, session):
        block = session.query(BlockModel).filter(BlockModel.id == block_id).first()
        if not block:
            return {"status_code": 404, "detail": "Block not found"}

        block.active = not block.active
        session.add(block)
        return {
            "status_code": 200,
            "detail": "Block toggled",
            "current_status": block.active,
        }

    @sqlalchemy_session(engine_url)
    def add_block(self, block_data: BlockModelPost, session: Session):
        block = BlockModel(name=block_data.name, active=True)
        session.add(block)
        session.flush()
        return {"status_code": 200, "id": block.id}

    # TODO Скорее всего не нужно
    # @sqlalchemy_session(engine_url)
    # def get_model_list(self, session):
    #     return session.query(AttachmentModel).filter(AttachmentModel.type == 'model').first()

    @sqlalchemy_session(engine_url)
    def get_model(self, model_id: int, session):
        model: ModelsModel = (
            session.query(ModelsModel).filter(ModelsModel.id == model_id).first()
        )
        if not model:
            return {"status_code": 404, "detail": "Model not found"}
        file: FileModel = (
            session.query(FileModel).filter(FileModel.id == model.file_id).first()
        )
        if not file:
            return {"status_code": 404, "detail": "Model file not found"}

        return {
            "status_code": 200,
            "detail": "Ok",
            "file_path": file.path,
            "name": model.name,
            "description": model.description,
        }

    @sqlalchemy_session(engine_url)
    def get_predictions(self, block_id: int, n_predictions: int, session: Session):
        if session.get(BlockModel, block_id) is None:
            return {
                "status_code": 404,
                "detail": "Блока не существует",
            }

        predictions_data = (
            session.query(PredictionModel)
            .filter(PredictionModel.block_id == block_id)
            .order_by(desc(PredictionModel.id))
            .limit(n_predictions)
            .all()
        )
        predictions = [
            PredictionGet(
                id=prediction.id,
                insert_ts=prediction.insert_ts,
                m_data=prediction.m_data,
                property_id=prediction.property_id,
                block_id=prediction.block_id,
            )
            for prediction in predictions_data
        ]
        return predictions

    @sqlalchemy_session(engine_url)
    def add_prediction(self, prediction: PredictionPost, insert_ts: datetime, session):
        pred = PredictionModel(
            insert_ts=int(insert_ts.timestamp()),
            m_data=prediction.m_data,
            property_id=prediction.property_id,
            block_id=prediction.block_id,
        )
        session.add(pred)

    @sqlalchemy_session(engine_url)
    def add_property(self, property_data: PropertyPost, session: Session):
        property = PropertyModel(name=property_data.name, unit=property_data.unit)
        session.add(property)
        session.flush()
        return {"status_code": 200, "added_id": property.id}

    @sqlalchemy_session(engine_url)
    def get_properties(self, session: Session):
        properties_data = session.query(PropertyModel).all()
        properties = [
            PropertyGet(id=property.id, name=property.name, unit=property.unit)
            for property in properties_data
        ]
        return properties

    # @sqlalchemy_session(engine_url)
    # def add_file(self, description: str, file_path: str, session: Session):
    #     new_file = FileModel(description=description, path=file_path)
    #     session.add(new_file)
    #     session.flush()
    #     logger.info(f"Add new file {new_file}")
    #     return new_file.id

    # @sqlalchemy_session(engine_url)
    # def add_model(self, name: str, description: str, type_model: str, block_id: int, file_path: str, session: Session):
    #     new_file = FileModel(description=description, path=file_path)
    #     session.add(new_file)
    #     session.flush()

    #     new_model = ModelsModel(name=name, description=description, type=type_model, file_id=new_file.id, block_id=block_id)
    #     session.add(new_model)
    #     session.flush()

    #     logger.info(f"Add new model {new_model}")
    #     return new_model.id
