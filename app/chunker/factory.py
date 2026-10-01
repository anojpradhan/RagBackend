from app.chunker.base import BaseChunker
from app.chunker.recursive import RecursiveChunker
from app.chunker.sentence import SentenceChunker
from app.schemas.chunking import ChunkingStrategy


def get_chunker(strategy: ChunkingStrategy) -> BaseChunker:

    if strategy == ChunkingStrategy.RECURSIVE:
        return RecursiveChunker()

    if strategy == ChunkingStrategy.SENTENCE:
        return SentenceChunker()

    raise ValueError(f"Unsupported chunking strategy: {strategy}")
