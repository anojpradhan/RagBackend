from app.chunker.base import BaseChunker
from app.chunker.recursive import RecursiveChunker
from app.chunker.sentence import SentenceChunker


def get_chunker(strategy: str) -> BaseChunker:

    if strategy == "recursive":
        return RecursiveChunker()

    if strategy == "sentence":
        return SentenceChunker()

    raise ValueError(f"Unsupported chunking strategy: {strategy}")
