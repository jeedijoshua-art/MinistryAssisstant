from app.services.assistant.tools.base_tool import BaseTool

class MockTool(BaseTool):
    def __init__(self, tool_name: str, tool_desc: str):
        self._name = tool_name
        self._desc = tool_desc
        
    @property
    def name(self) -> str:
        return self._name
        
    @property
    def description(self) -> str:
        return self._desc
        
    def execute(self, **kwargs) -> str:
        return f"[System Note: The {self.name} is currently a placeholder and will be fully implemented in Phase 4.]"

def get_sermon_tool():
    return MockTool("sermon_tool", "Generates sermon outlines and drafts.")

def get_prayer_tool():
    return MockTool("prayer_tool", "Generates contextual prayers.")

def get_devotional_tool():
    return MockTool("devotional_tool", "Generates devotionals.")

def get_poster_tool():
    return MockTool("poster_tool", "Generates church posters and social media graphics.")
