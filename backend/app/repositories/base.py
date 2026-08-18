from typing import Any, Generic, Sequence, TypeVar
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class Repository(Generic[ModelT]):
    def __init__(self, session: Session, model: type[ModelT]) -> None:
        self.session = session
        self.model = model

    def get(self, entity_id: object) -> ModelT | None:
        return self.session.get(self.model, entity_id)

    def list(self, skip: int = 0, limit: int = 100, **kwargs: Any) -> Sequence[ModelT]:
        stmt = select(self.model).filter_by(**kwargs).offset(skip).limit(limit)
        return self.session.execute(stmt).scalars().all()

    def add(self, entity: ModelT) -> ModelT:
        try:
            self.session.add(entity)
            self.session.flush()
            return entity
        except Exception:
            self.session.rollback()
            raise

    def update(self, entity: ModelT) -> ModelT:
        try:
            self.session.flush()
            return entity
        except Exception:
            self.session.rollback()
            raise

    def delete(self, entity: ModelT) -> None:
        try:
            self.session.delete(entity)
            self.session.flush()
        except Exception:
            self.session.rollback()
            raise
