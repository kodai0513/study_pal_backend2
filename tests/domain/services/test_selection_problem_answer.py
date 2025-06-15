import pytest

from app.domain.services.selection_problem_answer import (
    SelectionProblemAnswerService,
)


class DummyAnswer:
    def __init__(self, is_correct: bool, statement: str):
        self.is_correct = is_correct
        self.statement = statement


@pytest.mark.parametrize(
    "answers, expected",
    [
        ([DummyAnswer(False, "A"), DummyAnswer(False, "B")], False),
        ([DummyAnswer(True, "A"), DummyAnswer(False, "B")], True),
        ([DummyAnswer(True, "A"), DummyAnswer(True, "B")], False),
    ],
)
def test_has_only_one_correct_answer(
    answers: list[DummyAnswer], expected: bool
):
    assert (
        SelectionProblemAnswerService.has_only_one_correct_answer(answers)
        == expected
    )
