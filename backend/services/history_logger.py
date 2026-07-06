import json
import logging
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session as DBSession

from backend.models import (
    UserProfile,
    EventContext,
    NetworkingSession,
    GeneratedStarter,
    WikipediaFactCheck,
    LogEntry,
)

logger = logging.getLogger(__name__)


def create_user(db: DBSession, bio_text: str = "", event_cache: str = "") -> UserProfile:
    user = UserProfile(BioText=bio_text, currentEventCache=event_cache)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: DBSession, user_id: int) -> Optional[UserProfile]:
    return db.query(UserProfile).filter(UserProfile.UserID == user_id).first()


def get_or_create_user(db: DBSession, bio_text: str = "") -> UserProfile:
    user = db.query(UserProfile).first()
    if user is None:
        user = create_user(db, bio_text=bio_text)
    return user


def create_event_context(db: DBSession, description: str, themes: str = "") -> EventContext:
    event = EventContext(EventDescription=description, AnalyzedThemes=themes)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def create_session(
    db: DBSession, user_id: int, event_id: int
) -> NetworkingSession:
    session = NetworkingSession(
        UserID=user_id,
        EventID=event_id,
        SessionTimestamp=datetime.now(timezone.utc),
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def create_starter(
    db: DBSession, session_id: int, starter_text: str, context_prompt: str = ""
) -> GeneratedStarter:
    starter = GeneratedStarter(
        SessionID=session_id,
        StarterText=starter_text,
        ContextPromptUsed=context_prompt,
    )
    db.add(starter)
    db.commit()
    db.refresh(starter)
    return starter


def create_fact_check(
    db: DBSession, session_id: int, query: str, status: str, source_url: str
) -> WikipediaFactCheck:
    fc = WikipediaFactCheck(
        SessionID=session_id,
        VerifiedQueryText=query,
        VerificationStatus=status,
        WikipediaSourceURL=source_url,
    )
    db.add(fc)
    db.commit()
    db.refresh(fc)
    return fc


def create_log(
    db: DBSession,
    action_type: str,
    payload: dict,
    session_id: Optional[int] = None,
) -> LogEntry:
    log = LogEntry(
        SessionID=session_id,
        ActionType=action_type,
        PayloadJSON=json.dumps(payload),
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_session_history(db: DBSession) -> list[dict]:
    sessions = (
        db.query(NetworkingSession)
        .order_by(NetworkingSession.SessionTimestamp.desc())
        .all()
    )
    result = []
    for s in sessions:
        event = db.query(EventContext).filter(EventContext.EventID == s.EventID).first()
        starters = (
            db.query(GeneratedStarter)
            .filter(GeneratedStarter.SessionID == s.SessionID)
            .all()
        )
        result.append({
            "session_id": s.SessionID,
            "timestamp": s.SessionTimestamp,
            "event_description": event.EventDescription if event else "",
            "themes": event.AnalyzedThemes if event else "",
            "starters": starters,
        })
    return result


def get_feedback_history(db: DBSession) -> list[GeneratedStarter]:
    return (
        db.query(GeneratedStarter)
        .filter(GeneratedStarter.Feedback.isnot(None))
        .order_by(GeneratedStarter.StarterID.desc())
        .all()
    )
