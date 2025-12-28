import json
import os


class Memory:
    def __init__(self, file_path: str = "memory.json"):
        self.file_path = file_path
        self.messages = self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, indent=2)

    def add(self, role: str, message: str):
        self.messages.append({
            "role": role,
            "message": message
        })
        self._save()

    def get_history(self):
        return self.messages

    def clear(self):
        self.messages = []
        self._save()
