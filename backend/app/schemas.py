from pydantic import BaseModel
from typing import List, Any

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    flights: List[Any] = []
    hotels: List[Any] = []
