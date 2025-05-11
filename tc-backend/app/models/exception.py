class NotFoundException(Exception):
    """Exception raised when a resource is not found."""

    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code
