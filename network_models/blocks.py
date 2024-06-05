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
    sensors: List[SensorInfoGet]
    model: MLModelGet
    properties: List[PropertyGet]
    active: bool

class SensorBlockinfo(BaseModel):
    measurement_source_id: int
    sensor_item_id: int

class BlockModelPost(BaseModel):
	name: str
	sensors: List[SensorBlockinfo]
	model: int
	properties: List[int]
     
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