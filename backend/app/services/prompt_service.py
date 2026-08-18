class PromptService:
    def __init__(self):
        # In a full implementation, we'd fetch from config/db
        self.default_system_prompt = (
            "You are the ZTP Assistant, a helpful AI minister. "
            "You provide guidance, support, and theological insight based on the bible. "
            "Always be respectful, kind, and informative."
        )

    def get_system_prompt(self, module: str = "general") -> str:
        # We can implement fetching from DB or config later.
        # For now, return a configurable default.
        return self.default_system_prompt
