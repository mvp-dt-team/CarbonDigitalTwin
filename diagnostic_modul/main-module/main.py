from classes import Model, Block, Sensor, Handler, RandomForestModel
from typing import List, Dict, Union
import requests
import json

# class ModelEmulator(Model):
#     def __init__(self, model_path: str, params: dict, version: str):
#         super().__init__(model_path, params, version)
    
#     def proccessing(self, data: any) -> Union[dict, int]:
#         if data is not None:
#             if self.status == STATUS.TRAIN.value:
#                 return {'type': 'train'}
#             elif self.status == STATUS.PREDICT.value:
#                 return {'type': 'predict'}
#         else:
#             return 1


URL = 'localhost:8000'

test_handler = Handler(2, URL)

model = RandomForestModel('C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\random_forest_model.pkl', {}, '0.0.1', ['Elastic Modulus'])
measurement_source = json.loads(requests.get(f'http://{URL}/measurement_source').content)
units = []
for source in measurement_source:
    response = requests.get(f'http://{URL}/sensors_by_source?id={source["id"]}')
    units.append(json.loads(response.content))

sources = []

for i in range(len(units)):
    for j in range(len(units[i])):
        sources.append(Sensor(
            id=j,
            measurement_source_id=i,
            type_sensor='test',
            name=measurement_source[i]['name'],
            unit=measurement_source[i]['unit'],
            description=units[i][j]['description'],
            model_name=units[i][j]['model_name'],
            installation_time=units[i][j]['installation_time'],
            deactivation_time=units[i][j]['deactivation_time']
        ))

# print(sources)
test_handler.add_block(model, sources)
test_handler.action()
