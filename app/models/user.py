from sqlmodel import Field, Relationship

from app.models.base import Base


class User(Base, table=True):
    email: str = Field(max_length=255, unique=True)
    name: str = Field(max_length=255, unique=True, regex=r"^[a-zA-Z_0-9]+$")
    nick_name: str | None = Field(max_length=255, nullable=True)
    password: str
    
    articles: list["Article"] = Relationship(back_populates="user")
