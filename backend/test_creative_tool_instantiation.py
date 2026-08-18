import asyncio
from app.services.assistant.tools.creative_tool import CreativeStudioTool
from app.services.assistant.tool_dispatcher import ToolDispatcher

class MockGemini:
    pass

class MockContentService:
    pass

class MockBibleService:
    pass

def test_instantiation():
    gemini = MockGemini()
    content = MockContentService()
    bible = MockBibleService()
    
    print("Instantiating CreativeStudioTool...")
    tool = CreativeStudioTool(gemini, content, bible)
    print(f"Tool instantiated successfully. Name: {tool.name}")
    
    print("Instantiating ToolDispatcher...")
    dispatcher = ToolDispatcher(gemini, None, None, None, None, tool, None)
    print("ToolDispatcher instantiated successfully.")
    
    print("Testing dispatch logic...")
    # Just asserting it doesn't crash on init
    assert dispatcher is not None
    assert tool.name == "creative_studio_tool"
    print("All tests passed.")
    
if __name__ == "__main__":
    test_instantiation()
