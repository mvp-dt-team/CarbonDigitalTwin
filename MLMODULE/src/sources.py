class Source:
    def __init__(self, source_point_id: int, source_id: int, source_type: str):
        self.source_point_id = source_point_id
        self.source_id = source_id
        self.source_type = source_type

    def __repr__(self) -> str:
        return f"{self.source_type} {self.source_id} {self.source_point_id}"
