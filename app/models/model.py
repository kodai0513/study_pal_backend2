from datetime import datetime
from typing import Optional

from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, Integer, Relationship

from app.models.study_pal_base import MYSQL_UUID, StudyPalBaseModel


class ArticleLike(StudyPalBaseModel, table=True):
    __tablename__ = "article_likes"  # type: ignore

    article_id: str = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("articles.id", ondelete="CASCADE"),
        ),
    )
    user_id: str | None = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    article: "Article" = Relationship(back_populates="article_likes")
    user: Optional["User"] = Relationship(back_populates="article_likes")


class Article(StudyPalBaseModel, table=True):
    __tablename__ = "articles"  # type: ignore

    page_id: int | None = Field(
        default=None,
        sa_column=Column(
            Integer, autoincrement=True, nullable=True, unique=True
        ),
    )
    description: str = Field(max_length=400)
    user_id: str = Field(
        default=None,
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )

    article_likes: list["ArticleLike"] = Relationship(
        back_populates="article", passive_deletes=True
    )
    user: "User" = Relationship(back_populates="articles")


class DescriptionProblem(StudyPalBaseModel, table=True):
    __tablename__ = "description_problems"  # type: ignore

    correct_statement: str = Field(max_length=255)
    statement: str = Field(max_length=1000)
    workbook_id: str = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("workbooks.id", ondelete="CASCADE"),
        ),
    )
    workbook_category_id: str | None = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("workbook_categories.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    workbook: "Workbook" = Relationship(back_populates="description_problems")
    workbook_category: Optional["WorkbookCategory"] = Relationship(
        back_populates="description_problems"
    )


class PermissionRole(StudyPalBaseModel, table=True):
    __tablename__ = "permission_roles"  # type: ignore

    permission_id: str | None = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("permissions.id"),
            primary_key=True,
        ),
    )
    role_id: str | None = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("roles.id"),
            primary_key=True,
        ),
    )


class Permission(StudyPalBaseModel, table=True):
    __tablename__ = "permissions"  # type: ignore

    name: str = Field(max_length=255)

    roles: list["Role"] = Relationship(
        back_populates="permissions", link_model=PermissionRole
    )


class Role(StudyPalBaseModel, table=True):
    __tablename__ = "roles"  # type: ignore

    name: str = Field(max_length=255)

    workbook_invitation_members: list["WorkbookInvitationMember"] = (
        Relationship(back_populates="role")
    )
    workbook_members: list["WorkbookMember"] = Relationship(
        back_populates="role"
    )
    permissions: list["Permission"] = Relationship(
        back_populates="roles", link_model=PermissionRole
    )


class SelectionProblemAnswer(StudyPalBaseModel, table=True):
    __tablename__ = "selection_problem_answers"  # type: ignore

    is_correct: bool
    selection_problem_id: str = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("selection_problems.id", ondelete="CASCADE"),
        ),
    )
    statement: str = Field(max_length=255)

    selection_problem: "SelectionProblem" = Relationship(
        back_populates="selection_problem_answers"
    )


class SelectionProblem(StudyPalBaseModel, table=True):
    __tablename__ = "selection_problems"  # type: ignore

    statement: str = Field(max_length=255)
    workbook_id: str = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("workbooks.id", ondelete="CASCADE"),
        ),
    )
    workbook_category_id: str | None = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("workbook_categories.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    selection_problem_answers: list["SelectionProblemAnswer"] = Relationship(
        back_populates="selection_problem", passive_deletes=True
    )
    workbook: "Workbook" = Relationship(back_populates="selection_problems")
    workbook_category: Optional["WorkbookCategory"] = Relationship(
        back_populates="selection_problems"
    )


class TrueOrFalseProblem(StudyPalBaseModel, table=True):
    __tablename__ = "true_or_false_problems"  # type: ignore

    is_correct: bool
    statement: str = Field(max_length=255)
    workbook_id: str = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("workbooks.id", ondelete="CASCADE"),
        ),
    )
    workbook_category_id: str | None = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("workbook_categories.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    workbook: "Workbook" = Relationship(
        back_populates="true_or_false_problems"
    )
    workbook_category: Optional["WorkbookCategory"] = Relationship(
        back_populates="true_or_false_problems"
    )


class User(StudyPalBaseModel, table=True):
    __tablename__ = "users"  # type: ignore

    email: str = Field(max_length=255, unique=True)
    name: str = Field(max_length=255, unique=True, regex=r"^[a-zA-Z_0-9]+$")
    nick_name: Optional[str] = Field(max_length=255, nullable=True)
    password: str

    articles: list["Article"] = Relationship(
        back_populates="user", passive_deletes=True
    )
    article_likes: list["ArticleLike"] = Relationship(back_populates="user")
    workbook_invitation_members: list["WorkbookInvitationMember"] = (
        Relationship(back_populates="user", passive_deletes=True)
    )
    workbook_members: list["WorkbookMember"] = Relationship(
        back_populates="user", passive_deletes=True
    )
    workbooks: list["Workbook"] = Relationship(back_populates="user")


class WorkbookCategoryClosure(StudyPalBaseModel, table=True):
    __tablename__ = "workbook_category_closures"  # type: ignore

    workbook_id: str = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("workbooks.id", ondelete="CASCADE"),
        ),
    )
    child_id: str = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("workbook_categories.id", ondelete="CASCADE"),
        ),
    )
    is_root: bool
    parent_id: str = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("workbook_categories.id", ondelete="CASCADE"),
        ),
    )
    position: int
    level: int


class WorkbookCategory(StudyPalBaseModel, table=True):
    __tablename__ = "workbook_categories"  # type: ignore

    name: str = Field(max_length=255)
    workbook_id: str = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("workbooks.id", ondelete="CASCADE"),
        ),
    )

    description_problems: list["DescriptionProblem"] = Relationship(
        back_populates="workbook_category"
    )
    selection_problems: list["SelectionProblem"] = Relationship(
        back_populates="workbook_category"
    )
    true_or_false_problems: list["TrueOrFalseProblem"] = Relationship(
        back_populates="workbook_category"
    )
    workbook: "Workbook" = Relationship(back_populates="workbook_categories")


class WorkbookInvitationMember(StudyPalBaseModel, table=True):
    __tablename__ = "workbook_invitation_members"  # type: ignore

    effective_at: datetime
    is_invited: bool = Field(default=False)
    role_id: str = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("roles.id", ondelete="RESTRICT"),
        ),
    )
    user_id: str = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("users.id", ondelete="CASCADE"),
        ),
    )
    workbook_id: str = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("workbooks.id", ondelete="CASCADE"),
        ),
    )

    role: "Role" = Relationship(back_populates="workbook_invitation_members")
    user: "User" = Relationship(back_populates="workbook_invitation_members")
    workbook: "Workbook" = Relationship(
        back_populates="workbook_invitation_members"
    )


class WorkbookMember(StudyPalBaseModel, table=True):
    __tablename__ = "workbook_members"  # type: ignore

    role_id: str = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("roles.id", ondelete="RESTRICT"),
        ),
    )
    user_id: str = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("users.id", ondelete="CASCADE"),
        ),
    )
    workbook_id: str = Field(
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("workbooks.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )

    role: "Role" = Relationship(back_populates="workbook_members")
    user: "User" = Relationship(back_populates="workbook_members")
    workbook: "Workbook" = Relationship(back_populates="workbook_members")


class Workbook(StudyPalBaseModel, table=True):
    __tablename__ = "workbooks"  # type: ignore

    user_id: str | None = Field(
        default=None,
        sa_column=Column(
            MYSQL_UUID,
            ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    description: Optional[str] = Field(max_length=400, nullable=True)
    is_public: bool = Field(default=False)
    title: str = Field(max_length=255)

    workbook_categories: list[WorkbookCategory] = Relationship(
        back_populates="workbook", passive_deletes=True
    )
    description_problems: list["DescriptionProblem"] = Relationship(
        back_populates="workbook", passive_deletes=True
    )
    workbook_invitation_members: list["WorkbookInvitationMember"] = (
        Relationship(back_populates="workbook")
    )
    workbook_members: list["WorkbookMember"] = Relationship(
        back_populates="workbook", passive_deletes=True
    )
    selection_problems: list["SelectionProblem"] = Relationship(
        back_populates="workbook", passive_deletes=True
    )
    true_or_false_problems: list["TrueOrFalseProblem"] = Relationship(
        back_populates="workbook", passive_deletes=True
    )
    user: Optional["User"] = Relationship(back_populates="workbooks")
