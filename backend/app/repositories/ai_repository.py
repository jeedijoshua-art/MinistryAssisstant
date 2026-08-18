from app.repositories.base import Repository
from app.models.domain import AIUsage, PromptHistory

class AIUsageRepository(Repository[AIUsage]):
    def __init__(self, session):
        super().__init__(session, AIUsage)

class PromptHistoryRepository(Repository[PromptHistory]):
    def __init__(self, session):
        super().__init__(session, PromptHistory)
