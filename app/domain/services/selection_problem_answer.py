from typing import Protocol, Sequence


class Answer(Protocol):
    is_correct: bool
    statement: str


class SelectionProblemAnswerService:
    @classmethod
    def has_only_one_correct_answer(cls, answers: Sequence[Answer]) -> bool:
        correct_count = sum(1 for ans in answers if ans.is_correct)
        return correct_count == 1
