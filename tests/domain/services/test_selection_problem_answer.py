from typing import cast

import pytest

from app.domain.services.selection_problem import (
    SelectionProblem as SelectionProblemProtocol,
)
from app.domain.services.selection_problem import (
    SelectionProblemService,
)
from app.exceptions.selection_problem_answers.invalid_multiple_choices_exception import (  # noqa
    InvalidMultipleChoicesException,
)
from app.exceptions.selection_problem_answers.invalid_single_correct_answer_exception import (  # noqa
    InvalidSingleCorrectAnswerException,
)


class Answer:
    def __init__(self, is_correct: bool, statement: str):
        self.is_correct = is_correct
        self.statement = statement


class SelectionProblem:
    def __init__(self, answers: list[Answer]) -> None:
        self.selection_problem_answers = answers


def test_validate_single_correct_answer_答えが一つだけの時検証に成功する():
    problem = cast(
        SelectionProblemProtocol,
        SelectionProblem([Answer(True, "A"), Answer(False, "B")]),
    )
    SelectionProblemService.validate_single_correct_answer(problem)


def test_validate_single_correct_answer_答えが複数ある時検証に失敗する():
    problem_with_no_correct = SelectionProblem(
        [Answer(False, "A"), Answer(False, "B")]
    )
    problem_with_multiple_correct = SelectionProblem(
        [Answer(True, "A"), Answer(True, "B")]
    )

    for problem in (problem_with_no_correct, problem_with_multiple_correct):
        with pytest.raises(InvalidSingleCorrectAnswerException):
            SelectionProblemService.validate_single_correct_answer(
                cast(SelectionProblemProtocol, problem)
            )


def test_validate_multiple_choices_選択肢が2つ以上ある時検証に成功する():
    problem = cast(
        SelectionProblemProtocol,
        SelectionProblem([Answer(True, "A"), Answer(False, "B")]),
    )
    # 選択肢が2つ以上なので例外は出ないはず
    SelectionProblemService.validate_multiple_choices(problem)


def test_validate_multiple_choices_選択肢が1つ以下の時検証に失敗する():
    problem_with_one_choice = SelectionProblem([Answer(True, "A")])
    problem_with_no_choice = SelectionProblem([])

    for problem in (problem_with_one_choice, problem_with_no_choice):
        with pytest.raises(InvalidMultipleChoicesException):
            SelectionProblemService.validate_multiple_choices(
                cast(SelectionProblemProtocol, problem)
            )
