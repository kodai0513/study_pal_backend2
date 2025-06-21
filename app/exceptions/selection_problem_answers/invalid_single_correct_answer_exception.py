class InvalidSingleCorrectAnswerException(Exception):
    """
    単一の正解でない場合にスローする例外
    """

    def __init__(self):
        super().__init__(
            "Among multiple answers, only one correct answer is allowed."
        )
