from dataclasses import dataclass, field
from typing import Optional

@dataclass
class MessageContext:
    question: Optional[str] = None
    processed_question: Optional[str] = None
    question_complexity: Optional[str] = None
    question_intent: Optional[str] = None
    retrieved_context: Optional[str] = None
    response: Optional[str] = None
    retrieved_doc_ids: Optional[list] = None
    is_cached: bool = False
    cached_response: Optional[str] = None
    layer_outputs: dict = field(default_factory=dict)
    metadata: Optional[dict] = field(default_factory=dict)
    history: Optional[list[dict]] = field(default_factory=list)