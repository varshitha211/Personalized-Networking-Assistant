from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from backend.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    UserID = Column(Integer, primary_key=True, index=True)
    BioText = Column(Text, default="")
    currentEventCache = Column(Text, default="")

    sessions = relationship("NetworkingSession", back_populates="user")


class EventContext(Base):
    __tablename__ = "event_contexts"

    EventID = Column(Integer, primary_key=True, index=True)
    EventDescription = Column(Text, nullable=False)
    AnalyzedThemes = Column(Text, default="")

    sessions = relationship("NetworkingSession", back_populates="event")


class NetworkingSession(Base):
    __tablename__ = "networking_sessions"

    SessionID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey("user_profiles.UserID"), nullable=False)
    EventID = Column(Integer, ForeignKey("event_contexts.EventID"), nullable=False)
    SessionTimestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("UserProfile", back_populates="sessions")
    event = relationship("EventContext", back_populates="sessions")
    starters = relationship("GeneratedStarter", back_populates="session", cascade="all, delete-orphan")
    fact_checks = relationship("WikipediaFactCheck", back_populates="session", cascade="all, delete-orphan")
    logs = relationship("LogEntry", back_populates="session", cascade="all, delete-orphan")


class GeneratedStarter(Base):
    __tablename__ = "generated_starters"

    StarterID = Column(Integer, primary_key=True, index=True)
    SessionID = Column(Integer, ForeignKey("networking_sessions.SessionID"), nullable=False)
    StarterText = Column(Text, nullable=False)
    ContextPromptUsed = Column(Text, default="")
    Feedback = Column(Integer, nullable=True)

    session = relationship("NetworkingSession", back_populates="starters")


class WikipediaFactCheck(Base):
    __tablename__ = "wikipedia_fact_checks"

    FactCheckID = Column(Integer, primary_key=True, index=True)
    SessionID = Column(Integer, ForeignKey("networking_sessions.SessionID"), nullable=False)
    VerifiedQueryText = Column(String(500), nullable=False)
    VerificationStatus = Column(String(100), default="verified")
    WikipediaSourceURL = Column(Text, default="")

    session = relationship("NetworkingSession", back_populates="fact_checks")


class LogEntry(Base):
    __tablename__ = "log_entries"

    LogID = Column(Integer, primary_key=True, index=True)
    SessionID = Column(Integer, ForeignKey("networking_sessions.SessionID"), nullable=True)
    ActionType = Column(String(100), nullable=False)
    PayloadJSON = Column(Text, default="{}")
    Timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    session = relationship("NetworkingSession", back_populates="logs")
