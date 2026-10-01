from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

embedding_service = EmbeddingService()
vector_service = VectorService()


chunks = [
    "Palm Mind AI develops artificial intelligence solutions.",
    "The company works with machine learning and RAG systems.",
    "Artificial intelligence can be used to build intelligent applications.",
]


embeddings = embedding_service.embed_documents(chunks)

print("Number of chunks:", len(chunks))
print("Number of embeddings:", len(embeddings))
print("Embedding dimension:", len(embeddings[0]))


vector_service.create_collection(vector_size=len(embeddings[0]))

vector_service.store_chunks(
    chunks=chunks,
    embeddings=embeddings,
    filename="test.txt",
)

print("Chunks stored successfully.")
