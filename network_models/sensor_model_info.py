from pydantic import BaseModel


class SensorModelInfo(BaseModel):
    id: int
    name: str
    description: str
