class CustomException(Exception):
    def __init__(self, text) -> None:
        self.value = text
        super().__init__(self.value)