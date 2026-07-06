from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from backend.database import get_db
from backend.schemas import (
    NetworkingSessionResponse,
    SessionHistoryResponse,
)
from backend.services import history_logger

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


@router.get("/", response_model=list[NetworkingSessionResponse])
def list_sessions(db: DBSession = Depends(get_db)):
    from backend.models import NetworkingSession
    sessions = db.query(NetworkingSession).order_by(NetworkingSession.SessionTimestamp.desc()).all()
    return sessions


@router.get("/{session_id}", response_model=NetworkingSessionResponse)
def get_session(session_id: int, db: DBSession = Depends(get_db)):
    from backend.models import NetworkingSession
    session = db.query(NetworkingSession).filter(NetworkingSession.SessionID == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get("/{session_id}/history", response_model=SessionHistoryResponse)
def get_session_history(session_id: int, db: DBSession = Depends(get_db)):
    from backend.models import NetworkingSession, EventContext, GeneratedStarter
    session = db.query(NetworkingSession).filter(NetworkingSession.SessionID == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    event = db.query(EventContext).filter(EventContext.EventID == session.EventID).first()
    starters = db.query(GeneratedStarter).filter(GeneratedStarter.SessionID == session.SessionID).all()
    return SessionHistoryResponse(
        session_id=session.SessionID,
        timestamp=session.SessionTimestamp,
        event_description=event.EventDescription if event else "",
        themes=event.AnalyzedThemes if event else "",
        starters=starters,
    )
