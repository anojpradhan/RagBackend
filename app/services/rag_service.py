from datetime import date, time

from sqlalchemy.ext.asyncio import AsyncSession

from app.llm.gemini import GeminiLLM
from app.schemas.booking import BookingCreate
from app.services.booking_service import BookingService
from app.services.embedding_service import EmbeddingService
from app.services.memory_service import MemoryService
from app.services.vector_service import VectorService


class RAGService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_service: VectorService,
        llm: GeminiLLM,
        memory_service: MemoryService,
        booking_service: BookingService,
    ) -> None:
        self.embedding_service = embedding_service
        self.vector_service = vector_service
        self.llm = llm
        self.memory_service = memory_service
        self.booking_service = booking_service

    def retrieve(
        self,
        question: str,
        limit: int = 5,
    ):
        query_embedding = self.embedding_service.embed_text(question)

        return self.vector_service.search(
            query_embedding=query_embedding,
            limit=limit,
        )

    def build_context(
        self,
        results,
    ) -> str:
        context_parts = []

        for result in results:
            text = result.payload.get("text")

            if text:
                context_parts.append(text)

        return "\n\n".join(context_parts)

    def build_history(
        self,
        session_id: str,
    ) -> str:
        messages = self.memory_service.get_messages(session_id)

        if not messages:
            return "No previous conversation."

        history_parts = []

        for message in messages:
            role = message["role"]
            content = message["content"]

            history_parts.append(f"{role}: {content}")

        return "\n".join(history_parts)

    def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:
        self.memory_service.add_message(
            session_id=session_id,
            role=role,
            content=content,
        )

    def get_missing_booking_fields(
        self,
        booking_data: dict,
    ) -> list[str]:
        required_fields = [
            "name",
            "email",
            "interview_date",
            "interview_time",
        ]

        return [field for field in required_fields if not booking_data.get(field)]

    def booking_question(
        self,
        missing_fields: list[str],
    ) -> str:
        field = missing_fields[0]

        questions = {
            "name": "Sure. May I have your name?",
            "email": "What is your email address?",
            "interview_date": "What date would you like to schedule the interview?",
            "interview_time": "What time would you prefer for the interview?",
        }

        return questions[field]

    async def handle_booking(
        self,
        session_id: str,
        conversation: str,
        db: AsyncSession,
    ) -> str:

        extracted = self.llm.extract_booking(conversation)

        booking_data = self.memory_service.get_booking_data(session_id)

        extracted_data = extracted.model_dump(exclude_none=True)

        extracted_data.pop(
            "booking_requested",
            None,
        )

        # Store date/time as strings because Redis uses JSON.
        if "interview_date" in extracted_data:
            extracted_data["interview_date"] = str(extracted_data["interview_date"])

        if "interview_time" in extracted_data:
            extracted_data["interview_time"] = str(extracted_data["interview_time"])

        booking_data.update(extracted_data)

        if not extracted.booking_requested and not booking_data:
            return ""

        booking_data["booking_requested"] = True

        self.memory_service.set_booking_data(
            session_id=session_id,
            data=booking_data,
        )

        missing_fields = self.get_missing_booking_fields(booking_data)

        if missing_fields:
            return self.booking_question(missing_fields)

        booking_create = BookingCreate(
            name=booking_data["name"],
            email=booking_data["email"],
            interview_date=date.fromisoformat(booking_data["interview_date"]),
            interview_time=time.fromisoformat(booking_data["interview_time"]),
        )

        booking = await self.booking_service.create_booking(
            db,
            booking_create,
        )

        self.memory_service.clear_booking_data(session_id)

        return (
            "Your interview has been booked successfully. "
            f"Your interview is scheduled for "
            f"{booking.interview_date} at "
            f"{booking.interview_time}."
        )

    async def answer(
        self,
        session_id: str,
        question: str,
        db: AsyncSession,
        limit: int = 5,
    ) -> str:

        history = self.build_history(session_id)

        conversation = f"{history}\nuser: {question}"

        booking_data = self.memory_service.get_booking_data(session_id)

        booking_requested = bool(booking_data.get("booking_requested"))

        booking_keywords = [
            "book",
            "booking",
            "schedule",
            "interview",
        ]

        if booking_requested or any(
            word in question.lower() for word in booking_keywords
        ):
            booking_answer = await self.handle_booking(
                session_id=session_id,
                conversation=conversation,
                db=db,
            )

            if booking_answer:
                self.save_message(
                    session_id=session_id,
                    role="user",
                    content=question,
                )

                self.save_message(
                    session_id=session_id,
                    role="assistant",
                    content=booking_answer,
                )

                return booking_answer

        results = self.retrieve(
            question=question,
            limit=limit,
        )

        context = self.build_context(results)

        prompt = f"""
        You are a helpful AI assistant.
        Answer the user's question using the provided
        document context and conversation history.
        Rules:
        - Use the document context as the primary source of information.
        - Use conversation history to understand references and previous questions.
        - If the answer cannot be found in the document context, say that you don't have enough information.
        - Do not invent facts that are not supported by the context.
        - Keep the answer clear and concise.
        Conversation history:
        {history}
        Document context:
        {context}
        Current question:
        {question}
        Answer:
        """

        answer = self.llm.generate(prompt)

        self.save_message(
            session_id=session_id,
            role="user",
            content=question,
        )

        self.save_message(
            session_id=session_id,
            role="assistant",
            content=answer,
        )

        return answer
