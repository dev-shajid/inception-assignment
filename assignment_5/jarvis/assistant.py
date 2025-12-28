from jarvis.gemini_engine import GeminiEngine
from jarvis.prompt_controller import PromptController
from jarvis.memory import Memory

class Agent:
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.engine = GeminiEngine(api_key=api_key, model=model)
        self.prompt_controller = PromptController()
        self.memory = Memory()

    def respond(self, user_input: str, role: str) -> str:
        prompt = self.prompt_controller.build_prompt(
            user_input=user_input,
            memory=self.memory.get_history(),
            role=role
        )

        response = self.engine.generate(prompt)

        self.memory.add("user", user_input)
        self.memory.add("assistant", response)

        return response
    
    def respond_stream(self, user_input: str, role: str):
        prompt = self.prompt_controller.build_prompt(
            user_input=user_input,
            memory=self.memory.get_history(),
            role=role
        )

        full_response = ""
        stream = self.engine.generate_stream(prompt)
        
        for chunk in stream:
            full_response += chunk
            yield chunk

        self.memory.add("user", user_input)
        self.memory.add("assistant", full_response)
    
    def clear_memory(self):
        self.memory.clear()

    def get_history(self):
        return self.memory.get_history()