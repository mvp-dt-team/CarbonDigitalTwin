from dataclasses import dataclass
from typing import List

from pydantic import BaseModel


class Measurement(BaseModel):
    m_data: float
    sensor_item_id: int
    measurement_source_id: int


class InsertMeasurementsRequest(BaseModel):
    query_id: int
    insert_ts: str
    insert_values: List[Measurement]
