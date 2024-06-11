from typing import List, Dict, Optional
from pydantic import BaseModel


class SensorPropertyGet(BaseModel):
    name: str
    unit: str
    parameters: Dict[str, str]
    measurement_source_id: int


class SensorPropertyPost(BaseModel):
    name: str
    parameters: Dict[str, str]
    measurement_source_id: int


class SensorInfoPost(BaseModel):
    parameters: Dict[str, str]
    type: str
    properties: List[SensorPropertyPost]
    is_active: Optional[bool] = None
    description: Optional[str] = None
    sensor_model_id: Optional[int] = None


class SensorInfoGet(BaseModel):
    id: Optional[int] = None
    parameters: Dict[str, str]
    type: str
    properties: List[SensorPropertyGet]
    is_active: Optional[bool] = None
    description: Optional[str] = None
    sensor_model_id: Optional[int] = None
