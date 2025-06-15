class DataNotFoundException(Exception):
    """
    データが見つからなかった場合にスローされる例外。
    """
    def __init__(self, message: str | None = None):
        default_message = f"{message} not found."
        super().__init__(default_message)
