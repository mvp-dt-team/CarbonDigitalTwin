class Model:
    def __init__(
        self,
        id: int,
        model_path: str,
    ):
        self.model_path = model_path
        self.id = id

    def __repr__(self) -> str:
        return self.id
