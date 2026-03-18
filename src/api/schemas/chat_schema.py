from typing import Optional
from pydantic import BaseModel


class ChatRequestDTO(BaseModel):
    message: str


class ChatResponseDTO(BaseModel):
    response: str
    intent: str
    complexity: str
    is_cached: bool = False
    layer_outputs: dict = {}
    context: Optional[str] = None
