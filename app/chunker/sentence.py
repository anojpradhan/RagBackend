import re

from app.chunker.base import BaseChunker


class SentenceChunker(BaseChunker):
    def __init__(
        self,
        chunk_size: int = 500,
    ) -> None:
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())

        chunks: list[str] = []

        current_chunk = ""

        for sentence in sentences:
            if not sentence:
                continue
            candidate = (
                f"{current_chunk} {sentence}".strip() if current_chunk else sentence
            )

            if len(candidate) <= self.chunk_size:
                current_chunk= candidate

            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk)

        return chunks
