from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Measurement(BaseModel):
    m_data: float
    sensor_item_id: int
    measurement_source_id: int
    insert_ts: Optional[datetime] = None


class MeasurementsInfo(BaseModel):
    query_id: int
    insert_ts: datetime
    insert_values: List[Measurement]
