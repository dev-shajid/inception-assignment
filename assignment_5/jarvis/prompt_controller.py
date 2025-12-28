class PromptController:
    def __init__(self):
        self.system_prompt = (
            "You are JARVIS, a smart, professional, and helpful personal AI assistant. "
            "You answer clearly, accurately, and efficiently."
        )

        self.role_prompts = {
            "Tutor": (
                "You are acting as a Tutor. Explain concepts step by step with examples."
            ),
            "Coder": (
                "You are acting as a Coding Assistant. Be concise and code-focused."
            ),
            "Mentor": (
                "You are acting as a Career Mentor. Give realistic and actionable advice."
            ),
        }

    def build_prompt(self, user_input: str, memory: list, role: str) -> str:
        role_prompt = self.role_prompts.get(role, "")

        history = ""
        for msg in memory:
            history += f"{msg['role'].capitalize()}: {msg['message']}\n"

        prompt = f"""
SYSTEM:
{self.system_prompt}

ROLE:
{role_prompt}

CONVERSATION HISTORY:
{history}

USER:
{user_input}

ASSISTANT:
"""
        return prompt.strip()
