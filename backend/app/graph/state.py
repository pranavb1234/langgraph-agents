from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class Flight(BaseModel):
    airline: str
    price: float
    depart_time: str
    arrive_time: str

class Hotel(BaseModel):
    name: str
    rating: float
    price: float
    location: str

class Trip(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    depart_date: Optional[str] = None
    return_date: Optional[str] = None
    budget: Optional[float] = None

class ConversationState(BaseModel):
    user_message: str = ""
    trip: Trip = Trip()
    flights: List[Flight] = []
    hotels: List[Hotel] = []
    reply: str = ""        # Final message to user
    active_task: Optional[str] = None
