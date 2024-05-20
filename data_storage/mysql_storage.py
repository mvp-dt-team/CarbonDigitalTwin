from datetime import datetime
from typing import List
from mysql.connector import connect

from network_models.measurement_source_info import MeasurementSourceInfo
from network_models.measurements_info import Measurement
from network_models.sensor_model_info import SensorModelInfo
from network_models.sensors_info import SensorInfo, SensorProperty


class MySQLStorage():

    def close(self):
        self.mysql_connection.close()

    def __init__(self, host: str, password: str, user: str, database: str) -> None:
        self.host = host
        self.password = password
        self.user = user
        self.database = database

        self.mysql_connection = connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def add_measurement(self, measurement: Measurement, query_id: int, insert_ts: datetime) -> None:
        with self.mysql_connection.cursor() as cursor:
            query = ('INSERT INTO measurement (query_id, insert_ts, m_data, sensor_item_id, measurement_source_id) '
                     'VALUES (%s, %s, %s, %s, %s)')
            cursor.execute(query, (
                query_id, int(insert_ts.timestamp()), measurement.m_data, measurement.sensor_item_id,
                measurement.measurement_source_id))
            self.mysql_connection.commit()
            cursor.close()

    def get_last_three_measurements_for_sources(self, measurement_source_ids: List[int]) -> List[Measurement]:
        measurements = []
        with self.mysql_connection.cursor() as cursor:
            for source_id in measurement_source_ids:
                query = ('''
                    SELECT insert_ts, m_data, sensor_item_id, measurement_source_id FROM measurement 
                    WHERE measurement_source_id = %s 
                    ORDER BY insert_ts DESC 
                    LIMIT 3
                ''')
                cursor.execute(query, (source_id,))
                result = cursor.fetchall()
                measurements.extend(
                    [Measurement(insert_ts=measurement[0], m_data=measurement[1], sensor_item_id=measurement[2],
                                 measurement_source_id=measurement[3]) for measurement in result])
        return measurements

    # MEASUREMENT SOURCE ########################

    def get_measurement_sources(self) -> List[MeasurementSourceInfo]:
        with self.mysql_connection.cursor() as cursor:
            query = '''SELECT id, name, description, units FROM measurement_source'''
            cursor.execute(query)
            sources_data = cursor.fetchall()
            sources: List[MeasurementSourceInfo] = []
            for raw_info in sources_data:
                item = MeasurementSourceInfo(id=raw_info[0], name=raw_info[1], description=raw_info[2],
                                             unit=raw_info[3])
                sources.append(item)
            cursor.close()
            return sources

    def add_measurement_source(self, source: MeasurementSourceInfo) -> None:
        with self.mysql_connection.cursor() as cursor:
            query = '''INSERT INTO measurement_source (name, description, units) VALUES (%s, %s, %s)'''
            cursor.execute(query, (source.name, source.description, source.unit))
            self.mysql_connection.commit()
            cursor.close()

    # SENSORS ##############
    def get_sensors_models(self) -> List[SensorModelInfo]:
        with self.mysql_connection.cursor() as cursor:
            query = '''SELECT id, name, description FROM sensor'''
            cursor.execute(query)
            models_data = cursor.fetchall()
            models: List[SensorModelInfo] = []
            for raw_info in models_data:
                item = SensorModelInfo(id=raw_info[0], name=raw_info[1], description=raw_info[2])
                models.append(item)
            cursor.close()
            return models

    def add_sensor_model(self, model: SensorModelInfo) -> None:
        with self.mysql_connection.cursor() as cursor:
            query = '''INSERT INTO sensor (name, description) VALUES (%s, %s)'''
            cursor.execute(query, (model.name, model.description))
            self.mysql_connection.commit()
            cursor.close()

    def get_sensors_info(self, is_active: bool) -> List[SensorInfo]:
        with self.mysql_connection.cursor() as cursor:
            get_active_sensors_query = '''
                    SELECT id, sensor_type, is_active, addition_info FROM sensor_item  
                            WHERE is_active = true''' # TODO Изменил на True, так как далее в коде никакой параметр не передается, но это и не нужно, раз нам нужно получать все активные датчики
            get_all_sensors_query = "SELECT id, sensor_type, is_active, addition_info FROM sensor_item"
            cursor.execute(get_active_sensors_query if is_active else get_all_sensors_query)
            sensors_data = cursor.fetchall()
            sensors: List[SensorInfo] = []
            for raw_sensor in sensors_data:
                sensor_id = raw_sensor[0]
                sensor_type = raw_sensor[1]
                is_active = raw_sensor[2]
                addition_info = raw_sensor[3]

                get_parameters_query = '''
                                SELECT param_name, param_value, property_id FROM sensor_params 
                                WHERE sensor_item_id=%s
                                '''
                cursor.execute(get_parameters_query, (sensor_id,))
                parameters = cursor.fetchall()
                sensor_parameters = {param_name: param_value for param_name, param_value, property_id in parameters if
                                     property_id is None}

                get_properties_query = '''
                                        SELECT source.id, source.name, source.units FROM measurement_source source 
                                              JOIN digital_twin_database.sensor_source_mapping ssm 
                                              ON source.id = ssm.measurement_source_id
                                              WHERE ssm.sensor_item_id=%s
                                              '''
                cursor.execute(get_properties_query, (sensor_id,))
                raw_properties = cursor.fetchall()
                props: List[SensorProperty] = []
                for raw_property in raw_properties:
                    property_id = raw_property[0]
                    property_name = raw_property[1]
                    property_units = raw_property[2]
                    property_parameters = {param_name: param_value for param_name, param_value, id in
                                           parameters if
                                           id == property_id}
                    props.append(
                        SensorProperty(measurement_source_id=property_id, name=property_name, unit=property_units,
                                       parameters=property_parameters))

                sensors.append(SensorInfo(id=sensor_id, parameters=sensor_parameters,
                                          type=sensor_type, properties=props, is_active=is_active,
                                          description=addition_info))
            cursor.close()
            return sensors

    def add_sensor(self, sensor: SensorInfo):
        with self.mysql_connection.cursor() as cursor:

            # Добавление экземпляра датчика в таблицу
            query = '''INSERT INTO sensor_item (sensor_id, 
                                                is_active, 
                                                sensor_type, 
                                                addition_info) VALUES (%s, %s, %s, %s)'''
            cursor.execute(query, (sensor.sensor_model_id, True, sensor.type, sensor.description))
            
            # Получение ID экземпляра датчика из таблицы sensor_item
            sensor_item_id = cursor.lastrowid

            # Связка этого экземпляра с источником измерения
            query = '''INSERT INTO sensor_source_mapping (measurement_source_id, sensor_item_id) 
                        VALUES (%s, %s)'''
            values = [(prop.measurement_source_id, sensor_item_id) for prop in sensor.properties]
            cursor.executemany(query, values)

            # Вставка параметров для датчика
            query = '''INSERT INTO sensor_params (sensor_item_id, property_id, param_name, param_value) 
                        VALUES (%s, %s, %s, %s)'''
            values = [(sensor_item_id, None, param_name, sensor.parameters[param_name])
                      for param_name in sensor.parameters]
            
            # Вставка измеряемых свойств для датчика
            for prop in sensor.properties:
                values.extend([(sensor_item_id, prop.measurement_source_id, param_name, prop.parameters[param_name])
                               for param_name in prop.parameters])
            cursor.executemany(query, values)

    def toggle_sensor_activation(self, sensor_item_id: int, is_active: bool):
        with self.mysql_connection.cursor() as cursor:
            update_query = "UPDATE sensor_item SET is_active = %s WHERE id = %s"
            cursor.execute(update_query, (is_active, sensor_item_id))
            self.mysql_connection.commit()
