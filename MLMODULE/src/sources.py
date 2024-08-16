class Source:
    def __init__(
        self,
        measurement_source_id: int,
    ):
        self.measurement_source_id = measurement_source_id

    def __repr__(self) -> str:
        return self.measurement_source_id
