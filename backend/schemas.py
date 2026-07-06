from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserProfileCreate(BaseModel):
    BioText: str = ""
    currentEventCache: str = ""


class UserProfileResponse(BaseModel):
    UserID: int
    BioText: str
    currentEventCache: str

    class Config:
        from_attributes = True


class EventContextCreate(BaseModel):
    EventDescription: str
    AnalyzedThemes: str = ""


class EventContextResponse(BaseModel):
    EventID: int
    EventDescription: str
    AnalyzedThemes: str

    class Config:
        from_attributes = True


class NetworkingSessionCreate(BaseModel):
    UserID: int
    EventID: int


class NetworkingSessionResponse(BaseModel):
    SessionID: int
    UserID: int
    EventID: int
    SessionTimestamp: datetime

    class Config:
        from_attributes = True


class GenerateStartersRequest(BaseModel):
    event_description: str = Field(..., min_length=1, description="Description of the networking event")
    interests: str = Field("", description="Your personal interests or areas of expertise")


class GenerateStartersResponse(BaseModel):
    session_id: int
    starters: list[str]
    themes: list[str]


class StarterFeedbackRequest(BaseModel):
    starter_id: int
    feedback: int = Field(..., ge=-1, le=1, description="1 for thumbs up, -1 for thumbs down")


class GeneratedStarterResponse(BaseModel):
    StarterID: int
    SessionID: int
    StarterText: str
    ContextPromptUsed: str
    Feedback: Optional[int] = None

    class Config:
        from_attributes = True


class FactCheckRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Topic to fact-check on Wikipedia")


class FactCheckResponse(BaseModel):
    query: str
    summary: str
    source_url: str
    status: str
    fact_check_id: Optional[int] = None


class WikipediaFactCheckResponse(BaseModel):
    FactCheckID: int
    SessionID: int
    VerifiedQueryText: str
    VerificationStatus: str
    WikipediaSourceURL: str

    class Config:
        from_attributes = True


class LogEntryCreate(BaseModel):
    SessionID: Optional[int] = None
    ActionType: str
    PayloadJSON: str = "{}"


class LogEntryResponse(BaseModel):
    LogID: int
    SessionID: Optional[int]
    ActionType: str
    PayloadJSON: str
    Timestamp: datetime

    class Config:
        from_attributes = True


class SessionHistoryResponse(BaseModel):
    session_id: int
    timestamp: datetime
    event_description: str
    themes: str
    starters: list[GeneratedStarterResponse]
