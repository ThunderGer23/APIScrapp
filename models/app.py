from typing import Optional
from pydantic import BaseModel

class FileModel(BaseModel):
    id: Optional[str]
    name: str
    data: bytes