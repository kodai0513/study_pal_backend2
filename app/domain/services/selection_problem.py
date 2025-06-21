from typing import Protocol, Sequence

from app.exceptions.selection_problem_answers.invalid_multiple_choices_exception import (  # noqa
    InvalidMultipleChoicesException,
)
from app.exceptions.selection_problem_answers.invalid_same_statement_exception import (  # noqa
    InvalidSameStatementException,
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
        """
        選択問題に正解が1つだけ設定されていることを検証する。
        """
        correct_count = sum(
            1
            for ans in selection_problem.selection_problem_answers
            if ans.is_correct
        )

        if correct_count != 1:
            raise InvalidSingleCorrectAnswerException

    @staticmethod
    def validate_multiple_choices(selection_problem: SelectionProblem) -> None:
        """
        選択肢が2つ以上あることを検証する。
        """
        if len(selection_problem.selection_problem_answers) < 2:
            raise InvalidMultipleChoicesException

    @staticmethod
    def validate_same_statement(selection_problem: SelectionProblem) -> None:
        """
        全ての選択肢の内容（statement）が重複していないことを検証する。
        """
        statement_counts: dict[str, int] = {}
        for v in selection_problem.selection_problem_answers:
            if v.statement in statement_counts:
                statement_counts[v.statement] += 1
            else:
                statement_counts[v.statement] = 1

        for v in statement_counts:
            if statement_counts[v] > 1:
                raise InvalidSameStatementException
