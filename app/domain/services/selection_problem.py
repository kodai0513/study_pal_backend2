from typing import Protocol, Sequence

from app.exceptions.selection_problem_answers.invalid_multiple_choices_exception import (  # noqa
    InvalidMultipleChoicesException,
)
from app.exceptions.selection_problem_answers.invalid_single_correct_answer_exception import (  # noqa
    InvalidSingleCorrectAnswerException,
)


class Answer(Protocol):
    is_correct: bool
    statement: str


class SelectionProblem(Protocol):
    selection_problem_answers: Sequence[Answer]


class SelectionProblemService:
    @staticmethod
    def validate_single_correct_answer(
        selection_problem: SelectionProblem,
    ) -> None:
        correct_count = sum(
            1
            for ans in selection_problem.selection_problem_answers
            if ans.is_correct
        )

        if correct_count != 1:
            raise InvalidSingleCorrectAnswerException

    @staticmethod
    def validate_multiple_choices(selection_problem: SelectionProblem) -> None:
        if len(selection_problem.selection_problem_answers) < 2:
            raise InvalidMultipleChoicesException
