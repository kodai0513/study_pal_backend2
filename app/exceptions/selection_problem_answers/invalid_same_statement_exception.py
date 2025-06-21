class InvalidSameStatementException(Exception):
    """
    同じ回答がある時スローする例外
    """

    def __init__(self):
        super().__init__("There is the same answer statement.")
