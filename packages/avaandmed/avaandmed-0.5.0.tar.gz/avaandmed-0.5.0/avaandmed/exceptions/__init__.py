class AvaandmedException(Exception):
    pass


class AvaandmedApiExcepiton(AvaandmedException):
    def __init__(self, status: int, uri: str, msg="", details: dict = None) -> None:
        self.status = status
        self.uri = uri
        self.msg = msg
        self.details = details

    def __str__(self) -> str:
        return f"""
            status: {self.status}
            url: {self.uri}
            message: {self.msg}
            details: {self.details}
        """
