import time
from typing import List
from uuid import uuid4
from mysql.connector import connect

from sensors_module.property import Property
from sensors_module.sensor import Sensor
from network_models.active_sensors_response import ActiveSensorsResponseItem, SensorProperty


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

    def write_data(self, sensor: Sensor, property: Property, value):
        measurement_time = time.time()
        id = uuid4()
        sensor_id = sensor.id
        property_id = property.id
        with self.mysql_connection.cursor() as cursor:
            query = ('INSERT INTO measurement (query_id, insert_ts, m_data, sensor_item_id, measurement_source_id) '
                     'VALUES (%s, %s, %s, %s, %s)')
            cursor.execute(query, (id, measurement_time, value, sensor_id, property_id))
            self.mysql_connection.commit()
            cursor.close()

    def get_sensors_info(self) -> List[ActiveSensorsResponseItem]:
        with self.mysql_connection.cursor() as cursor:
            get_active_sensors_query = '''
                    SELECT id, sensor_type FROM sensor_item  
                            WHERE is_active = TRUE'''
            cursor.execute(get_active_sensors_query)
            sensors_data = cursor.fetchall()
            sensors: List[ActiveSensorsResponseItem] = []
            for raw_sensor in sensors_data:
                sensor_id = raw_sensor[0]
                sensor_type = raw_sensor[1]

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
                    property_parameters = {param_name: param_value for param_name, param_value, p_id in
                                           parameters if
                                           p_id == property_id}
                    props.append(SensorProperty(p_id=property_id, name=property_name, unit=property_units,
                                                parameters=property_parameters))

                sensors.append(ActiveSensorsResponseItem(s_id=sensor_id, parameters=sensor_parameters,
                                                         s_type=sensor_type, properties=props))
            return sensors
