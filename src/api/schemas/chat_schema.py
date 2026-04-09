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
    generation_time: Optional[float] = None
    input_tokens_est: Optional[int] = None