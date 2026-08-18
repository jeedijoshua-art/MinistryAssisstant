from typing import List, Optional
from app.repositories.bible_repository import BibleTopicRepository
from app.models.domain import BibleTopic, BibleVerse

class TopicService:
    def __init__(self, topic_repo: BibleTopicRepository):
        self.topic_repo = topic_repo
        
    def get_topic_by_name(self, name: str) -> Optional[BibleTopic]:
        return self.topic_repo.get_by_name(name)
        
    def search_topics(self, query: str) -> List[BibleTopic]:
        return self.topic_repo.search(query)
        
    def get_verses_for_topic(self, topic_id: str) -> List[BibleVerse]:
        return self.topic_repo.get_verses_for_topic(topic_id)
