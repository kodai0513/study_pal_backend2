class InvalidMultipleChoicesException(Exception):
    """
    回答が二つ以上ない時スローする例外
    """

    def __init__(self):
        super().__init__("Two or more answers are required.")
