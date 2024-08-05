from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class MeasurementsGet(BaseModel):
    m_data: float
    sensor_item_id: int
    measurement_source_id: int
    insert_ts: Optional[datetime] = None


class MeasurementsPost(BaseModel):
    insert_ts: datetime
    insert_values: List[MeasurementsGet]
