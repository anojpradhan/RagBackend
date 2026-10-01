from app.services.embedding_service import EmbeddingService
from app.services.rag_service import RAGService
from app.services.vector_service import VectorService

embedding_service = EmbeddingService()
vector_service = VectorService()

rag_service = RAGService(
    embedding_service=embedding_service,
    vector_service=vector_service,
)


question = "What does Palm Mind AI use PostgreSQL for?"

results = rag_service.retrieve(
    question=question,
    limit=5,
)

print("\n--- RETRIEVED RESULTS ---")

for index, result in enumerate(results, start=1):
    print(f"\nResult {index}")
    print("Score:", result.score)
    print("Payload:", result.payload)


context = rag_service.build_context(results)

print("\n--- CONTEXT ---")
print(context)
