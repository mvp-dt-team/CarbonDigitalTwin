from classes import Model, Block, Sensor, Handler, RandomForestModel
from typing import List, Dict, Union
import requests
import json
# from config_reader import config

URL = 'localhost:5000'

test_handler = Handler(polling_interval=2, url=URL)

blocks_info = response = requests.get(f'http://{URL}/blocks?need_active=true')

model = RandomForestModel(r'C:\Users\boiko.k.v\Desktop\CarbonDigitalTwin\diagnostic_modul\random_forest_model.pkl', {}, '0.0.1', ['Elastic Modulus']) # Требуется доработка модуля хранения
measurement_source = json.loads(requests.get(f'http://{URL}/measurement_source').content)
print(measurement_source)
units = []
for source in measurement_source:
    response = requests.get(f'http://{URL}/sensors_by_source?id={source["id"]}')
    units.append(json.loads(response.content))

# sources = [
#     Sensor(
#         id=6,
#         measurement_source_id=4,
#         type_sensor='random',
#         name='press1',
#         unit='Pa',
#         description='press1'
#     ),
#     Sensor(
#         id=7,
#         measurement_source_id=5,
#         type_sensor='random',
#         name='temp1',
#         unit='C',
#         description='temp1'
#     ),
#     Sensor(
#         id=8,
#         measurement_source_id=6,
#         type_sensor='random',
#         name='hum',
#         unit='Precent',
#         description='hum'
#     ),
#     Sensor(
#         id=9,
#         measurement_source_id=7,
#         type_sensor='random',
#         name='temp2',
#         unit='C',
#         description='temp2'
#     ),
#     Sensor(
#         id=10,
#         measurement_source_id=8,
#         type_sensor='random',
#         name='press2',
#         unit='Pa',
#         description='press2'
#     ),
# ]
# print(measurement_source)
# for i in range(len(units)):
#     for j in range(len(units[i])):
#         sources.append(Sensor(
#             id=j,
#             measurement_source_id=i,
#             type_sensor='test',
#             name=measurement_source[i]['name'],
#             unit=measurement_source[i]['unit'],
#             description=units[i][j]['description'],
#             model_name=units[i][j]['model_name'],
#             installation_time=units[i][j]['installation_time'],
#             deactivation_time=units[i][j]['deactivation_time']
#         ))

# # print(sources)
test_handler.add_block(model, sources)
test_handler.action()
