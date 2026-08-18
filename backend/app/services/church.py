from app.models import Church
from app.repositories.church import ChurchRepository


class ChurchService:
    def __init__(self, repository: ChurchRepository) -> None:
        self.repository = repository

    def default_church(self) -> Church | None:
        return self.repository.get_by_name("ZION PRAYER TOWER")
