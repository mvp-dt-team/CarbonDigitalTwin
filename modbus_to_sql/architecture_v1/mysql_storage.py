import time
from typing import Sequence
from uuid import uuid4
from modbus_to_sql.architecture_v1.data_storage_interface import DataStorage
from mysql.connector import connect, Error

from modbus_to_sql.architecture_v1.property import Property
from modbus_to_sql.architecture_v1.sensor import Sensor


class MySQLStorage(DataStorage):

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
        with self.mysql_connection.cursor() as cursor:
            query = 'INSERT INTO measurement (query_id, insert_ts, m_data, sensor_item_id) VALUES (%s, %s, %s, %s)'
            cursor.execute(query, (id, measurement_time, value, sensor_id))
            self.mysql_connection.commit()
            cursor.close()

    def get_sensors_info(self) -> Sequence[Sensor]:
        with self.mysql_connection.cursor() as cursor:
            query = '''
                    SELECT item.id, cp.param_value FROM sensor_item item 
                            JOIN digital_twin_database.connection_params cp 
                            ON item.id = cp.sensor_item_id 
                            WHERE is_active = TRUE AND cp.param_name = 'type' '''
            cursor.execute(query)
            sensors_data = cursor.fetchall()
            for raw_sensor in sensors_data:
                query = '''
                        SELECT source.id, source.name, source.units FROM measurement_source source 
                              JOIN digital_twin_database.sensor_source_mapping ssm 
                              ON source.id = ssm.measurement_source_id
                              WHERE ssm.sensor_item_id=%s
                              '''
                cursor.execute(query, (raw_sensor[0],))
                parameters = cursor.fetchall()
                # todo add sensor constructor depends on sensor_type
