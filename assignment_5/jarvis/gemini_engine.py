from google import genai

class GeminiEngine:
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        if not api_key:
            raise ValueError("Missing Gemini API key")

        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            return f"⚠️ Gemini error: {str(e)}"

    def generate_stream(self, prompt: str):
        try:
            response = self.client.models.generate_content_stream(
                model=self.model,
                contents=prompt
            )
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"⚠️ Gemini error: {str(e)}"
