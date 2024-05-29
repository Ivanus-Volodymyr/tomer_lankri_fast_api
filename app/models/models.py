import uuid
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class IDBase(Base):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )


class User(IDBase):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(300))
    posts: Mapped[list["Post"] | None] = relationship("Post", back_populates="owner")


class Post(IDBase):
    __tablename__ = "posts"

    text: Mapped[str] = mapped_column(String(500))
    owner_id: Mapped[UUID | None] = mapped_column(
        CHAR(36), ForeignKey("users.id", ondelete="SET NULL")
    )
    owner: Mapped["User"] = relationship("User", back_populates="posts")
