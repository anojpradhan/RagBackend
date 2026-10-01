from app.services.embedding_service import EmbeddingService


embedding_service = EmbeddingService()

text = "Palm Mind AI develops artificial intelligence solutions."

embedding = embedding_service.embed_text(text)

print("Embedding length:", len(embedding))
print("First 5 values:", embedding[:5])