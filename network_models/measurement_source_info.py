from typing import Optional

from pydantic import BaseModel


class MeasurementSourceInfo(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    unit: str
