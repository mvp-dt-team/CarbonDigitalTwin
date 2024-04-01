from typing import Optional

from pydantic import BaseModel


class SensorModelInfo(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
