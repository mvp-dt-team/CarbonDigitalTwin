from typing import Optional, List

from datetime import datetime

from pydantic import BaseModel

from .sensors_info import SensorInfoGet

from fastapi import FastAPI, File, Body, UploadFile, Request
from pydantic import BaseModel, model_validator
from typing import Optional, List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json

class PropertyGet(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    unit: str

class MLModelGet(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None

class BlockModelGet(BaseModel):
    id: int
    name: str
    sensors: List[SensorInfoGet] = None 
    model: MLModelGet = None 
    properties: List[PropertyGet] = None 
    active: bool

class SensorBlockinfo(BaseModel):
    measurement_source_id: int
    sensor_item_id: int

class BlockModelPost(BaseModel):
	name: str
	# sensors: List[SensorBlockinfo]
	# model: Optional[int] = None
	# properties: List[int]
     
class PredictionGet(BaseModel):
    insert_ts: int
    m_data: float
    property_id: int
    block_id: int

class PredictionPost(BaseModel):
    insert_ts: datetime
    insert_values: List[PredictionGet]

class AttachmentGet(BaseModel):
    name: str
    description: str
    type: str

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class AttachmentPost(BaseModel):
    insert_values: List[AttachmentGet]

class PropertyPost(BaseModel):
    name: str
    unit: str

class PropertyGet(BaseModel):
    id: int
    name: str
    unit: str

class ModelMappingGet(BaseModel):
    measurement_source_id: Optional[int] = None
    sensor_item_id: Optional[int] = None
    model_id: Optional[int] = None
    property_id: Optional[int] = None