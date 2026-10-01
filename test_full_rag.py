from app.llm.gemini import GeminiLLM
from app.services.embedding_service import EmbeddingService
from app.services.rag_service import RAGService
from app.services.vector_service import VectorService

embedding_service = EmbeddingService()
vector_service = VectorService()
llm = GeminiLLM()

rag_service = RAGService(
    embedding_service=embedding_service,
    vector_service=vector_service,
    llm=llm,
)


question = "What does PostgreSQL store?"

answer = rag_service.answer(
    question=question,
    limit=5,
)

print("\n--- QUESTION ---")
print(question)

print("\n--- ANSWER ---")
print(answer)
