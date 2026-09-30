from pydantic import BaseModel


class DocumentResponse(BaseModel):
    filename: str
    file_type: str
    text: str
