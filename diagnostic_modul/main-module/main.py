from classes import Model, Block, Sensor, Handler, STATUS
from typing import List, Dict, Union

class ModelEmulator(Model):
    def __init__(self, model_path: str, params: dict, version: str):
        super().__init__(model_path, params, version)
    
    def proccessing(self, data: any) -> Union[dict, int]:
        if data is not None:
            if self.status == STATUS.TRAIN.value:
                return {'type': 'train'}
            elif self.status == STATUS.PREDICT.value:
                return {'type': 'predict'}
        else:
            return 1




test_handler = Handler('main_db.db', 2)
model = ModelEmulator('./data/models/best.pt', {}, '0.0.1')
sensor = Sensor(0, 'VIDEO')
test_handler.add_block(model, [sensor])
test_handler.action()
