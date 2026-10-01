from app.llm.gemini import GeminiLLM
from app.services.embedding_service import EmbeddingService
from app.services.memory_service import MemoryService
from app.services.rag_service import RAGService
from app.services.vector_service import VectorService

embedding_service = EmbeddingService()
vector_service = VectorService()
llm = GeminiLLM()
memory_service = MemoryService()

rag_service = RAGService(
    embedding_service=embedding_service,
    vector_service=vector_service,
    llm=llm,
    memory_service=memory_service,
)
