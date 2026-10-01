from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document


class DocumentRepository:
    async def create(
        self,
        db: AsyncSession,
        *,
        filename: str,
        file_type: str,
        chunking_strategy: str,
        chunk_count: int,
    ) -> Document:
        document = Document(
            filename=filename,
            file_type=file_type,
            chunking_strategy=chunking_strategy,
            chunk_count=chunk_count,
        )

        db.add(document)

        await db.commit()
        await db.refresh(document)

        return document
