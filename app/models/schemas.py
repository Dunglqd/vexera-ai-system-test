from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FAQRequest(BaseModel):
    question: str
    user_id: Optional[str] = None

class FAQResponse(BaseModel):
    answer: str
    confidence: float
    source_question: Optional[str] = None
    processing_time: float

class BookingChangeRequest(BaseModel):
    booking_id: str
    new_departure_time: str
    reason: str
    user_id: str

class BookingChangeResponse(BaseModel):
    success: bool
    message: str
    new_booking_details: Optional[dict] = None

class ChatMessage(BaseModel):
    message: str
    timestamp: datetime
    user_id: Optional[str] = None
    message_type: str = "text"  # text, image, voice

class ChatResponse(BaseModel):
    response: str
    response_type: str = "text"
    confidence: float
    processing_time: float
