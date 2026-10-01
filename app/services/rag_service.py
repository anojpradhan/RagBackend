from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


class RAGService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_service: VectorService,
    ) -> None:

        self.embedding_service = embedding_service
        self.vector_service = vector_service

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
