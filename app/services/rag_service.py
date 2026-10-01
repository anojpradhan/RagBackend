from app.llm.gemini import GeminiLLM
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


class RAGService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_service: VectorService,
        llm: GeminiLLM,
    ) -> None:

        self.embedding_service = embedding_service
        self.vector_service = vector_service
        self.llm = llm

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

    def answer(
        self,
        question: str,
        limit: int = 5,
    ) -> str:
        results = self.retrieve(question=question, limit=limit)
        context = self.build_context(results)
        prompt = f""" You are helpful AI Assistant.
        Answer the user's question using the provided context. 
        Rules: 
        -Use the context as the primary source of information.
        -If the answer cannot be found in the context, say that you don't have enough information.
        - Do not invent facts that are not supported by the context.
        Context:
        {context}
        Question:
        {question}
        Answer: 
        """
        return self.llm.generate(prompt)
