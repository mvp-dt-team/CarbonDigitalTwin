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
            query = """
			INSERT INTO measurement (query_id, insert_id, value, sensor_item_id)
			VALUES (%s, %s, %s, %s) 
			"""
            cursor.execute(query, (id, measurement_time, value, sensor_id))
            self.mysql_connection.commit()

    def get_sensors_info(self) -> Sequence[Sensor]:
        return super().get_sensors_info()
