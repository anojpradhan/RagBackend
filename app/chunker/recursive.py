from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.chunker.base import BaseChunker


class RecursiveChunker(BaseChunker):
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50) -> None:
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def chunk(self, text: str) -> list[str]:
        return self.splitter.split_text(text)
