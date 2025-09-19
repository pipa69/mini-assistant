from pydantic import BaseModel
from typing import Optional, Dict, Any

class QueryRequest(BaseModel):
    user_id: Optional[str] = "anon"
    text: str

class QueryResponse(BaseModel):
    answer: str
    intent: Optional[str]
    confidence: float
    entities: Optional[Dict[str, Any]] = {}
