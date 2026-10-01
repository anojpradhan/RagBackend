from app.llm.gemini import GeminiLLM
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
    ) -> None:
        self.embedding_service = embedding_service
        self.vector_service = vector_service
        self.llm = llm
        self.memory_service = memory_service

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

    def answer(
        self,
        session_id: str,
        question: str,
        limit: int = 5,
    ) -> str:

        # Load conversation history
        history = self.build_history(session_id)

        # Retrieve relevant documents
        results = self.retrieve(
            question=question,
            limit=limit,
        )

        # Build document context
        context = self.build_context(results)

        # Build prompt
        prompt = f"""
        You are a helpful AI assistant.
        Answer the user's question using the provided document context
        and conversation history.
        Rules:
        - Use the document context as the primary source of information.
        - Use conversation history to understand references and previous questions.
        - If the answer cannot be found in the document context, say that you don't have enough information.
        - Do not invent facts that are not supported by the context.
        - Keep the answer clear and concise.Conversation history:
        {history}
        Document context:
        {context}
        Current question:
        {question}
        Answer:
        """

        # Generate answer
        answer = self.llm.generate(prompt)

        # Save conversation
        self.memory_service.add_message(
            session_id=session_id,
            role="user",
            content=question,
        )

        self.memory_service.add_message(
            session_id=session_id,
            role="assistant",
            content=answer,
        )

        return answer
