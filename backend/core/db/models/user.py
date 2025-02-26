from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import select

from core.db.models.base import Base
from core.db.models.base import vector, latent_vector
from core.db.session import get_session


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str]
    first_name: Mapped[str]
    surname: Mapped[str]
    preference: Mapped[vector]
    latent_preference: Mapped[Optional[latent_vector]]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "surname": self.surname,
            "preference": self.preference,
            "latent_preference": self.latent_preference,
        }

    def to_safe_dict(self) -> dict:
        """Depersonalized json serializable data."""
        safe_dict = {
            "id": self.id,
            "preference": self.preference.tolist(),
        }
        if self.latent_preference:
            safe_dict["latent_preference"] = self.latent_preference.tolist()
        return safe_dict


def get_user_by_id(
    user_id: str, _session: Optional[Session] = None
) -> Optional[User]:
    with get_session(_session) as session:
        statement = select(User).where(User.id == user_id)
        return session.scalar(statement)
