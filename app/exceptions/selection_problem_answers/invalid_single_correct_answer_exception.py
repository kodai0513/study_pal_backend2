class InvalidSingleCorrectAnswerException(Exception):
    """
    単一の正解でない場合にスローする例外
    """

    def __init__(self):
        super().__init__(
            "There must be exactly one correct answer among the choices."
        )
