from pydantic import BaseModel, Field
from typing import Optional, List


class Registration(BaseModel):
    registrationId: str
    userId: str
    eventId: str
    status: str  # "registered" or "waitlisted"
    registeredAt: str
    position: Optional[int] = None


class RegistrationRequest(BaseModel):
    userId: str = Field(..., min_length=1)


class RegistrationResponse(BaseModel):
    registrationId: str
    userId: str
    eventId: str
    status: str
    registeredAt: str
    position: Optional[int] = None
    message: str


class UserRegistrations(BaseModel):
    userId: str
    registrations: List[dict]


class EventRegistrations(BaseModel):
    eventId: str
    registered: List[dict]
    waitlisted: List[dict]
    counts: dict
