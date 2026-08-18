from typing import List, Dict, Any
import json

class ExportService:
    @staticmethod
    def export_conversation(history: List[Dict[str, Any]], format: str = "markdown") -> str:
        """
        Exports conversation history to the specified format.
        Supported formats: markdown, json, text
        """
        if format.lower() == "json":
            return json.dumps(history, indent=2)
            
        elif format.lower() == "markdown":
            output = "# Conversation Export\n\n"
            for msg in history:
                role = "User" if msg["role"] == "user" else "Assistant"
                output += f"### {role}\n\n"
                output += f"{msg['content']}\n\n"
                output += "---\n\n"
            return output
            
        elif format.lower() == "text":
            output = "Conversation Export\n===================\n\n"
            for msg in history:
                role = "User" if msg["role"] == "user" else "Assistant"
                output += f"{role}: {msg['content']}\n\n"
            return output
            
        else:
            raise ValueError(f"Unsupported export format: {format}")
