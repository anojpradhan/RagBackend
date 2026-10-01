from pydantic import BaseModel


class DocumentResponse(BaseModel):
    filename: str
    file_type: str
    chunking_strategy: str
    chunks: list[str]