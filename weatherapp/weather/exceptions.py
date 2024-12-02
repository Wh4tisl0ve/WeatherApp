class OpenWeatherApiError(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.__code = code

    @property
    def code(self) -> int:
        return self.__code

    @property
    def message(self) -> int:
        return self.args[0]

    def get_dict(self):
        return {
            "code": self.code,
            "message": self.message,
        }
