class ResponseFormatter:
    """
    Handles formatting of tool outputs and context injection for the LLM.
    """
    
    @staticmethod
    def format_tool_context(tool_name: str, tool_output: str) -> str:
        """
        Formats a tool's output to be injected into the LLM conversation stream.
        """
        return f"\n[SYSTEM TOOL CONTEXT - {tool_name}]\n{tool_output}\n[END TOOL CONTEXT]\n"

    @staticmethod
    def format_user_prompt_with_context(user_message: str, context: str) -> str:
        """
        Combines the user's message with the injected tool context.
        """
        return f"{context}\nUser: {user_message}"
