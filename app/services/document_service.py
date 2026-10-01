from pathlib import Path

import fitz
from fastapi import UploadFile

from app.chunker.factory import get_chunker


class DocumentService:
    async def extract_text(self, file: UploadFile) -> str:
        filename = file.filename or ""
        extension = Path(filename).suffix.lower()

        if extension == ".txt":
            return await self._extract_txt(file)
        if extension == ".pdf":
            return await self._extract_pdf(file)

        raise ValueError("Unspported file type")

    def chunk_text(self, text: str, strategy: str) -> list[str]:
        chunker = get_chunker(strategy)
        return chunker.chunk(text)

    async def _extract_txt(self, file: UploadFile) -> str:
        content = await file.read()
        return content.decode("utf-8")

    async def _extract_pdf(self, file: UploadFile) -> str:
        content = await file.read()
        document = fitz.open(stream=content, filetype="pdf")
        text = "\n".join(page.get_text() for page in document)
        document.close()
        return text
