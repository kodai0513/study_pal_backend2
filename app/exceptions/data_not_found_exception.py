class DataNotFoundException(Exception):
    """
    データが見つからなかった場合にスローされる例外。

    通常は、指定されたIDや条件に一致するレコードが
    データベース等に存在しない場合に使用されます。

    使用例:
        if article is None:
            raise DataNotFoundException("Article")
    """

    def __init__(self, message: str | None = None):
        default_message = f"{message} not found."
        super().__init__(default_message)
