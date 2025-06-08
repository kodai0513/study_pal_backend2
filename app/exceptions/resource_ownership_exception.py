class ResourceOwnershipException(Exception):
    """
    リソースの所有者が現在の操作ユーザーと一致しない場合にスローされる例外。

    この例外は、作成者（所有者）以外のユーザーがリソースを
    更新・削除などしようとしたときに使用されます。

    使用例:
        if resource.owner_id != current_user.id:
            raise ResourceOwnershipException("User")
    """

    def __init__(self, message: str | None = None):
        detail_message = f"{message} ownership mismatch."
        super().__init__(detail_message)
