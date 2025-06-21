from copy import deepcopy
from typing import cast

from sqlmodel import select

from app.db.session import SessionDep
from app.domain.services.selection_problem import (
    SelectionProblem as SelectionProblemProtocol,
)
from app.domain.services.selection_problem import (
    SelectionProblemService,
)
from app.exceptions.data_not_found_exception import DataNotFoundException
from app.models.model import SelectionProblem, SelectionProblemAnswer
from app.schemas.selection_problem import UpdateSelectionProblemReq
from app.usecases.selection_problems.dto import SelectionProblemDto


class UpdateCommand(UpdateSelectionProblemReq):
    selection_problem_id: str
    workbook_id: str


class UpdateAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: UpdateCommand) -> SelectionProblemDto:
        selection_problem_model = self._session.exec(
            select(SelectionProblem).where(
                SelectionProblem.id == command.selection_problem_id,
                SelectionProblem.workbook_id == command.workbook_id,
            )
        ).one_or_none()

        if selection_problem_model is None:
            raise DataNotFoundException("SelectionProblem")

        validated_command = deepcopy(command)
        validated_command.selection_problem_answers = [
            ans
            for ans in command.selection_problem_answers
            if not ans.is_delete
        ]
        SelectionProblemService.validate_multiple_choices(
            cast(SelectionProblemProtocol, validated_command)
        )

        SelectionProblemService.validate_single_correct_answer(
            cast(SelectionProblemProtocol, validated_command)
        )

        SelectionProblemService.validate_same_statement(
            cast(SelectionProblemProtocol, validated_command)
        )

        updated_selection_problem_model = SelectionProblem.update_by_id(
            command.selection_problem_id,
            self._session,
            command.model_dump(
                exclude_unset=True,
                exclude={"selection_problem_answers", "selection_problem_id"},
            ),
        )
        insert_answers = [
            answer
            for answer in command.selection_problem_answers
            if answer.id is None and not answer.is_delete
        ]
        update_answers = [
            answer
            for answer in command.selection_problem_answers
            if answer.id is not None and not answer.is_delete
        ]
        delete_answers = [
            answer
            for answer in command.selection_problem_answers
            if answer.is_delete and answer.id
        ]

        selection_problem_id_field = {
            "selection_problem_id": command.selection_problem_id
        }

        SelectionProblemAnswer.bulk_insert(
            [
                v.model_dump(exclude={"id", "is_delete"})
                | selection_problem_id_field
                for v in insert_answers
            ],
            self._session,
        )

        for answer in update_answers:
            SelectionProblemAnswer.update_by_id(
                cast(str, answer.id),
                self._session,
                answer.model_dump(
                    exclude_unset=True, exclude={"id", "is_delete"}
                ),
            )

        SelectionProblemAnswer.delete_by_ids(
            [cast(str, v.id) for v in delete_answers], self._session
        )
        self._session.commit()

        return SelectionProblemDto.model_validate(
            updated_selection_problem_model
        )
