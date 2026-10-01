from qdrant_client import QdrantClient

from app.core.config import settings

client = QdrantClient(url=settings.qdrant_url)

print(client.get_collections())
