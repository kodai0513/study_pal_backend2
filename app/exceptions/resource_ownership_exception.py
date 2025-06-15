class ResourceOwnershipException(Exception):
    """
    リソースの所有者が現在の操作ユーザーと一致しない場合にスローされる例外。
    """

    def __init__(self, message: str | None = None):
        detail_message = f"{message} ownership mismatch."
        super().__init__(detail_message)
