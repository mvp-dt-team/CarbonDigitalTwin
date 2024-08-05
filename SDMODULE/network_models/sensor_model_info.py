from typing import Optional

from pydantic import BaseModel


class SensorModelInfoPost(BaseModel):
    name: str
    description: str


class SensorModelInfoGet(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
