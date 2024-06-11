from typing import Optional

from pydantic import BaseModel


class MeasurementSourceInfoGet(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    unit: str


class MeasurementSourceInfoPost(BaseModel):
    name: str
    description: Optional[str] = None
    unit: str
