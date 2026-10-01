from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings
from app.llm.base import BaseLLM


class GeminiLLM(BaseLLM):
    def __init__(self) -> None:

        self.primary_model = ChatGoogleGenerativeAI(
            model=settings.gemini_primary_model,
            google_api_key=settings.google_api_key,
            temperature=0,
        )

        self.fallback_model = ChatGoogleGenerativeAI(
            model=settings.gemini_fallback_model,
            google_api_key=settings.google_api_key,
            temperature=0,
        )

    def generate(self, prompt: str) -> str:

        try:
            response = self.primary_model.invoke(prompt)

            return self._extract_content(response)

        except Exception as primary_error:
            print(f"Primary Gemini model failed: {primary_error}")

            print("Trying fallback Gemini model...")

            try:
                response = self.fallback_model.invoke(prompt)

                return self._extract_content(response)

            except Exception as fallback_error:
                raise RuntimeError("Both Gemini models failed.") from fallback_error

    @staticmethod
    def _extract_content(response) -> str:

        if isinstance(response.content, str):
            return response.content

        return "\n".join(
            block["text"]
            for block in response.content
            if isinstance(block, dict) and block.get("type") == "text"
        )
