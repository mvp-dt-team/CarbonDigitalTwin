import time
from typing import Sequence
from uuid import uuid4
from modbus_to_sql.architecture_v1.data_storage_interface import DataStorage
from mysql.connector import connect

from modbus_to_sql.architecture_v1.modbus_sensor import ModbusSensor
from modbus_to_sql.architecture_v1.property import Property
from modbus_to_sql.architecture_v1.sensor import Sensor
from modbus_to_sql.architecture_v1.unit import get_unit_from_str


class MySQLStorage(DataStorage):

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

    def get_sensors_info(self) -> Sequence[Sensor]:
        with self.mysql_connection.cursor() as cursor:
            get_active_sensors_query = '''
                    SELECT item.id, cp.param_value FROM sensor_item item 
                            JOIN digital_twin_database.connection_params cp 
                            ON item.id = cp.sensor_item_id 
                            WHERE is_active = TRUE AND cp.param_name = 'type' '''
            cursor.execute(get_active_sensors_query)
            sensors_data = cursor.fetchall()
            sensors: list[Sensor] = []
            for raw_sensor in sensors_data:
                get_properties_query = '''
                        SELECT source.id, source.name, source.units FROM measurement_source source 
                              JOIN digital_twin_database.sensor_source_mapping ssm 
                              ON source.id = ssm.measurement_source_id
                              WHERE ssm.sensor_item_id=%s
                              '''
                cursor.execute(get_properties_query, (raw_sensor[0],))
                raw_properties = cursor.fetchall()
                properties: list[Property] = []
                for property in raw_properties:
                    units = get_unit_from_str(property[2])
                    properties.append(Property(property[0], property[1], units))

                sensor_type = raw_sensor[1]
                if sensor_type == 'modbus':
                    get_address_query = '''
                    SELECT param_value FROM connection_params 
                    WHERE sensor_item_id=%s AND param_name='address'
                    '''
                    cursor.execute(get_address_query, (raw_sensor[0],))
                    modbus_address = cursor.fetchall()[0]  # todo add validation
                    sensors.append(ModbusSensor('modbus', raw_sensor[0], properties, modbus_address))
            return sensors
