from typing import List, Dict
from pydantic import BaseModel


class SensorProperty(BaseModel):
    p_id: int
    name: str
    unit: str
    parameters: Dict[str, str]


class ActiveSensorsResponseItem(BaseModel):
    s_id: int
    parameters: Dict[str, str]
    s_type: str
    properties: List[SensorProperty]
