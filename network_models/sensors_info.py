from typing import List, Dict, Optional
from pydantic import BaseModel


class SensorProperty(BaseModel):
    name: str
    unit: str
    parameters: Dict[str, str]
    measurement_source_id: int


class SensorInfoPost(BaseModel):
    id: Optional[int] = None
    parameters: Dict[str, str]
    type: str
    properties: List[SensorProperty]
    is_active: Optional[bool] = None
    description: Optional[str] = None
    sensor_model_id: Optional[int] = None

class SensorInfoGet(BaseModel):
    parameters: Dict[str, str]
    type: str
    properties: List[SensorProperty]
    is_active: Optional[bool] = None
    description: Optional[str] = None
    sensor_model_id: Optional[int] = None