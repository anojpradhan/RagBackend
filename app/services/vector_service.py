from uuid import uuid4

from qdrant_client import QdrantClient, models

from app.core.config import settings


class VectorService:
    def __init__(self) -> None:
        self.client = QdrantClient(url=settings.qdrant_url)

        self.collection_name = settings.qdrant_collection

    def create_collection(
        self,
        vector_size: int,
    ) -> None:

        if self.client.collection_exists(self.collection_name):
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE,
            ),
        )

    def search(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ):
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit,
        )
        return results.points

    def store_chunks(
        self,
        chunks: list[str],
        embeddings: list[list[float]],
        document_id: str,
        filename: str,
    ) -> None:

        points = []

        for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            points.append(
                models.PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload={
                        "document_id": document_id,
                        "filename": filename,
                        "chunk_index": index,
                        "text": chunk,
                    },
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True,
        )
