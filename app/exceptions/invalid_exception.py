class InvalidException(Exception):
    """
    不正値の場合にスローされる例外。
    """

    def __init__(self, message: str | None = None):
        super().__init__(message)
