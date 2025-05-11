import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy import DateTime, Column

class Base(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.now, nullable=False,
        sa_column_kwargs={'onupdate': datetime.now})
