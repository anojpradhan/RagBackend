from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


embedding_service = EmbeddingService()
vector_service = VectorService()


query = "What does Palm Mind AI work with?"

query_embedding = embedding_service.embed_text(query)

results = vector_service.search(
    query_embedding=query_embedding,
    limit=3,
)


for result in results:
    print("Score:", result.score)
    print("Payload:", result.payload)
    print("-" * 50)