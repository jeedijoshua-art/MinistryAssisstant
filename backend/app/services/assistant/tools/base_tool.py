from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    """Base class for all Assistant tools."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the tool."""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the tool does."""
        pass
        
    @abstractmethod
    def execute(self, **kwargs) -> str:
        """
        Executes the tool logic and returns a string 
        (usually markdown) to be appended to the conversation context.
        """
        pass
