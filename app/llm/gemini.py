from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings
from app.llm.base import BaseLLM


class GeminiLLM(BaseLLM):
    def __init__(self) -> None:
        self.model = ChatGoogleGenerativeAI(
            model="gemini-3.8-flash",
            google_api_key=settings.google_api_key,
            temperature=0,
        )

    def generate(self, prompt: str) -> str:
        response = self.model.invoke(prompt)
        if isinstance(response.content, str):
            return response.content
        return "\n".join(
            block["text"] for block in response.content if block.get("type") == "text"
        )
