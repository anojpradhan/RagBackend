from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings
from app.llm.base import BaseLLM
from app.schemas.booking import BookingExtraction


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

    def generate(
        self,
        prompt: str,
    ) -> str:

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

    def extract_booking(
        self,
        conversation: str,
    ) -> BookingExtraction:

        prompt = f"""
        You are an interview booking assistant.
        Analyze the conversation below.
        Determine whether the user wants to book an interview.
        Extract the following information when explicitly provided:
        - name
        - email
        - interview date
        - interview time
        Rules:
        - Do not invent information.
        - Return null for information that is missing.
        - booking_requested must be true when the user is attempting
        to schedule an interview.
        - Information may be provided across multiple messages.
        - Use the entire conversation to understand the booking request.
        Conversation:
        {conversation}
        """
        try:
            model = self.primary_model.with_structured_output(BookingExtraction)

            return model.invoke(prompt)

        except Exception as primary_error:
            print(f"Primary Gemini booking extraction failed: {primary_error}")

            print("Trying fallback Gemini model...")

            try:
                model = self.fallback_model.with_structured_output(BookingExtraction)

                return model.invoke(prompt)

            except Exception as fallback_error:
                raise RuntimeError(
                    "Both Gemini models failed during booking extraction."
                ) from fallback_error

    @staticmethod
    def _extract_content(response) -> str:

        if isinstance(response.content, str):
            return response.content

        return "\n".join(
            block["text"]
            for block in response.content
            if isinstance(block, dict) and block.get("type") == "text"
        )
