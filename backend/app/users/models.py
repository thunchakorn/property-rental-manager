from typing import Any
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base, BaseMixin


class User(Base, BaseMixin):
    __tablename__ = "users_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(default=True)
