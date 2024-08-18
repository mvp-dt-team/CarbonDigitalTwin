from datetime import datetime
from typing import List
from sqlalchemy import desc
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
import asyncio
from sqlalchemy import update

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
    RelationBlockinfo,
)

import time
from yaml import load
from yaml.loader import SafeLoader

with open("config.yaml", "r") as config_file:
    config = load(config_file, Loader=SafeLoader)

import logging
import os

logger = logging.getLogger("DataStorageModule")

UPLOAD_DIR = os.path.abspath("./uploads")


def sqlalchemy_session(engine_url):
    engine = create_async_engine(engine_url)

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with AsyncSession(engine) as session:
                async with session.begin():
                    try:
                        # Передаем сессию как аргумент в функцию
                        result = await func(*args, session=session, **kwargs)
                        await session.commit()  # Явное подтверждение транзакции
                    except Exception as e:
                        await session.rollback()  # Откат в случае ошибки
                        raise
                    return result
        return wrapper
    return decorator


class MySQLStorage:
    engine_url = f"mysql+aiomysql://{config['USER']}:{config['PASSWORD']}@{config['HOST']}:3306/{config['DB']}"

    # FOR TESTING !
    # engine_url = f'sqlite:///app.db'
    # def close(self):
    #     self.mysql_connection.close()

    def __init__(self) -> None:
        logger.debug("module starting")

    @sqlalchemy_session(engine_url)
    async def add_measurement(
        self,
        measurement: MeasurementsGet,
        insert_ts: datetime,
        query_uuid: str,
        session: AsyncSession,
    ) -> None:
        measurement_new = MeasurementModel(
            query_id=query_uuid,
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
    async def get_last_three_measurements_for_sources(
        self, measurement_source_ids: List[int], session: AsyncSession
    ) -> List[MeasurementsGet]:
        measurements = []
        for source_id in measurement_source_ids:
            result = await session.execute(
            select(MeasurementModel)
            .where(MeasurementModel.measurement_source_id == source_id)
            .order_by(desc(MeasurementModel.insert_ts))
            .limit(3)
        )
            result_data = result.scalars().all()  # Получаем результат как объекты моделей
            measurements.extend([
                MeasurementsGet(
                    m_data=data.m_data,
                    sensor_item_id=data.sensor_item_id,
                    measurement_source_id=data.measurement_source_id,
                    insert_ts=data.insert_ts
                ) for data in result_data 
            ])
            logger.info(f"Get measurements {measurements}")
        return measurements

    # MEASUREMENT SOURCE ########################

    @sqlalchemy_session(engine_url)
    async def get_measurement_sources(
        self, session: AsyncSession
    ) -> List[MeasurementSourceInfoGet]:
        sources_data = await session.execute(
            select(MeasurementSourceModel)
        )
        sources_data = sources_data.scalars().all()
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
    async def add_measurement_source(
        self, source: MeasurementSourceInfoPost, session: AsyncSession
    ) -> None:
        new_source = MeasurementSourceModel(
            name=source.name, description=source.description, units=source.unit
        )
        session.add(new_source)
        logger.info(f"Add measurement sources {new_source}")

    # SENSORS ##############
    @sqlalchemy_session(engine_url)
    async def get_sensors_models(self, session) -> List[SensorModelInfoGet]:
        models_data = await session.execute(
            select(SensorModel)
            )
        models_data = models_data.scalars().all()
        models = [
            SensorModelInfoGet(
                id=model.id, name=model.name, description=model.description
            )
            for model in models_data
        ]
        logger.info(f"Get sensors models {models}")
        return models

    @sqlalchemy_session(engine_url)
    async def add_sensor_model(self, model: SensorModelInfoPost, session) -> None:
        new_model = SensorModel(name=model.name, description=model.description)
        session.add(new_model)
        logger.info(f"Add sensors model {new_model}")

    @sqlalchemy_session(engine_url)
    async def get_sensors_info(self, need_active: bool, session) -> List[SensorInfoGet]:
        if need_active:
            query = await session.execute(select(SensorItemModel).where(SensorItemModel.is_active == True))
        else:
            query = await session.execute(select(SensorItemModel))

        sensors_data = query.scalars().all()
        sensors: List[SensorInfoGet] = []

        for raw_sensor in sensors_data:
            sensor_id = raw_sensor.id
            sensor_type = raw_sensor.sensor_type
            is_active = raw_sensor.is_active
            addition_info = raw_sensor.addition_info
            model_id = raw_sensor.sensor_id

            parameters_query = await session.execute(
                select(SensorParamsModel)
                .where(SensorParamsModel.sensor_item_id == sensor_id)
            )
            parameters_query = parameters_query.scalars().all()
            sensor_parameters = {
                param.param_name: param.param_value
                for param in parameters_query
                if param.property_id is None
            }

            properties_query = await session.execute(
                select(
                    MeasurementSourceModel.id,
                    MeasurementSourceModel.name,
                    MeasurementSourceModel.units,
                )
                .join(
                    SensorSourceMappingModel,
                    MeasurementSourceModel.id == SensorSourceMappingModel.measurement_source_id,
                )
                .where(SensorSourceMappingModel.sensor_item_id == sensor_id)
            )

            # Извлечение всех строк результата
            properties_query = properties_query.fetchall()

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
    async def add_sensor(self, sensor: SensorInfoPost, session):
        # Добавляем новый sensor_item
        new_sensor_item = SensorItemModel(
            sensor_id=sensor.sensor_model_id,
            is_active=True,
            sensor_type=sensor.type,
            addition_info=sensor.description,
        )
        session.add(new_sensor_item)
        await session.flush()  # Применяем изменения, чтобы получить id нового sensor_item

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
    async def toggle_sensor_activation(self, sensor_item_id: int, is_active: bool, session):
        stmt = (
            update(SensorItemModel)
            .where(SensorItemModel.id == sensor_item_id)
            .values(is_active=is_active)
        )
        await session.execute(stmt)
        logger.info(f"Togled sensor status (id = {sensor_item_id})")
        return {"status": "ok"}

    ### MLMODULE

    @sqlalchemy_session(engine_url)
    async def get_block_list(self, need_active: bool, session: AsyncSession):
        if need_active:
            blocks_data = await session.execute(select(BlockModel).where(BlockModel.active == need_active))
        else:
            blocks_data = await session.execute(select(BlockModel))
        blocks_data = blocks_data.scalars().all()
        blocks = {}
        for block in blocks_data:
            model_list = await session.execute(select(ModelsModel).where(ModelsModel.block_id == block.id))
            model_list = model_list.scalars().all()
            if len(model_list) > 0:
                block_model = model_list[-1]
                querry_model_mapping_get = await session.execute(select(ModelMappingModel).where(ModelMappingModel.model_id == block_model.id))
                blocks[block] = [
                    ModelMappingGet(
                        source_type=x.source_type,
                        source_block_id=x.block_id,
                        source_property_id=x.property_source_id,
                        measurement_source_id=x.measurement_source_id,
                        sensor_item_id=x.sensor_item_id,
                        model_id=x.model_id,
                        property_id=x.property_id,
                    )
                    for x in querry_model_mapping_get.scalars().all()
                ]
            else:
                blocks[block] = ModelMappingGet(
                    source_type=None,
                    source_block_id=None,
                    source_property_id=None,
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
                # print(content)
                sensors_set = []
                for i in content:
                    if i.source_type == "sensor":
                        if (
                            i.measurement_source_id,
                            i.sensor_item_id,
                        ) not in sensors_set:
                            sensors_set.append(
                                (i.measurement_source_id, i.sensor_item_id)
                            )
                blocks_set = []
                for i in content:
                    if i.source_type == "block":
                        if (i.source_property_id, i.source_block_id) not in blocks_set:
                            blocks_set.append((i.source_property_id, i.source_block_id))
                # print(sensors_set)
                sensors = [
                    SensorBlockinfo(
                        measurement_source_id=x[0],
                        sensor_item_id=x[1],
                    )
                    for x in sensors_set
                ]
                relation_blocks = [
                    RelationBlockinfo(
                        source_property_id=x[0],
                        source_block_id=x[1],
                    )
                    for x in blocks_set
                ]

                stmt = select(ModelsModel).where(ModelsModel.id == content[0].model_id)
                result = await session.execute(stmt)
                model_data = result.scalars().first()

                properties_ids = []
                for i in content:
                    if i.property_id not in properties_ids:
                        properties_ids.append(i.property_id)

                async def fetch_property(session, property_id):
                    stmt = select(PropertyModel).where(PropertyModel.id == property_id)
                    result = await session.execute(stmt)
                    return result.scalars().first()

                property_data = await asyncio.gather(*[fetch_property(session, x) for x in properties_ids])
                modelsmapping.append(
                    BlockModelGet(
                        id=block.id,
                        name=block.name,
                        sensors=sensors,
                        relation_blocks=relation_blocks,
                        model=MLModelGet(
                            id=model_data.id,
                            name=model_data.name,
                            description=model_data.description,
                            type=model_data.type,
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
    async def add_block_params(
        self,
        model_params: dict,
        sensors: List[dict],
        source_blocks: List[dict],
        properties: List[int],
        session: AsyncSession,
    ):
        new_file = FileModel(
            description=model_params["description"],
            path=model_params["file_path"],
            filename=model_params["file_name"],
            filehash=model_params["file_hash"],
        )
        session.add(new_file)
        await session.flush()

        new_model = ModelsModel(
            name=model_params["name"],
            description=model_params["description"],
            type=model_params["type_model"],
            file_id=new_file.id,
            block_id=model_params["block_id"],
        )
        session.add(new_model)
        await session.flush()

        for sensor in sensors:
            for property in properties:
                model_map = ModelMappingModel(
                    measurement_source_id=sensor["measurement_source_id"],
                    sensor_item_id=sensor["sensor_item_id"],
                    source_type="sensor",
                    model_id=new_model.id,
                    property_id=property,
                )
                session.add(model_map)

        for block in source_blocks:
            for property in properties:
                model_map = ModelMappingModel(
                    property_source_id=block["source_property_id"],
                    block_id=block["source_block_id"],
                    source_type="block",
                    model_id=new_model.id,
                    property_id=property,
                )
                session.add(model_map)

        logger.info(
            f"Add model, {len(sensors)} sensor and {len(properties)} properties to block"
        )
        return new_model.id

    @sqlalchemy_session(engine_url)
    async def toggle_block(self, block_id: int, session):
        block = await session.execute(select(BlockModel).where(BlockModel.id == block_id))
        block = block.scalars().first()
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
    async def add_block(self, block_data: BlockModelPost, session: AsyncSession):
        block = BlockModel(name=block_data.name, active=True)
        session.add(block)
        await session.flush()
        return {"status_code": 200, "id": block.id}

    @sqlalchemy_session(engine_url)
    async def get_model(self, model_id: int, session):
        model = await session.execute(select(ModelsModel).where(ModelsModel.id == model_id))
        model: ModelsModel = model.scalars().first()
        if not model:
            return {"status_code": 404, "detail": "Model not found"}
        file = await session.execute(select(FileModel).where(FileModel.id == model.file_id))
        file: FileModel = file.scalars().first()
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
    async def check_model(self, model_id: int, session):
        model = await session.execute(select(ModelsModel).where(ModelsModel.id == model_id))
        model: ModelsModel = model.scalars().first()
        if not model:
            return {"status_code": 404, "detail": "Model not found"}
        file = await session.execute(select(FileModel).where(FileModel.id == model.file_id))
        file: FileModel = file.scalars().first()
        if not file:
            return {"status_code": 404, "detail": "Model file not found"}

        return {
            "status_code": 200,
            "detail": "Ok",
            "file_name": file.filename,
            "file_hash": file.filehash,
        }

    @sqlalchemy_session(engine_url)
    async def get_predictions(
        self, block_id: int, property_id: int, n_predictions: int, session: AsyncSession
    ):
        if await session.get(BlockModel, block_id) is None:
            return {
                "status_code": 404,
                "detail": "Блока не существует",
            }
        predictions_data = await session.execute(
            select(PredictionModel)
            .where(PredictionModel.block_id == block_id,
                   PredictionModel.property_id == property_id)
            .order_by(desc(PredictionModel.insert_ts))
            .limit(n_predictions)
            )
        predictions_data = predictions_data.scalars().all()
        predictions = [
            PredictionGet(
                query_id=prediction.query_id,
                insert_ts=prediction.insert_ts,
                m_data=prediction.m_data,
                property_id=prediction.property_id,
                block_id=prediction.block_id,
            )
            for prediction in predictions_data
        ]
        return predictions

    @sqlalchemy_session(engine_url)
    async def add_prediction(
        self, prediction: PredictionPost, insert_ts: datetime, query_uuid: str, session
    ):
        pred = PredictionModel(
            query_id=query_uuid,
            insert_ts=int(insert_ts.timestamp()),
            m_data=prediction.m_data,
            property_id=prediction.property_id,
            block_id=prediction.block_id,
        )
        session.add(pred)

    @sqlalchemy_session(engine_url)
    async def add_property(self, property_data: PropertyPost, session: AsyncSession):
        property = PropertyModel(name=property_data.name, unit=property_data.unit)
        session.add(property)
        await session.flush()
        return {"status_code": 200, "added_id": property.id}

    @sqlalchemy_session(engine_url)
    async def get_properties(self, session: AsyncSession):
        properties_data = await session.execute(select(PropertyModel))
        properties_data = properties_data.scalars().all()
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
