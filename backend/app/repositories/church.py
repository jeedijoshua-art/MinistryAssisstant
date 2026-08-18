from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Church
from app.repositories.base import Repository


class ChurchRepository(Repository[Church]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Church)

    def get_by_name(self, name: str) -> Church | None:
        return self.session.scalar(select(Church).where(Church.name == name))
