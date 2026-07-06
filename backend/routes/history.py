from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession

from backend.database import get_db
from backend.schemas import SessionHistoryResponse, GeneratedStarterResponse, LogEntryResponse
from backend.services import history_logger

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("/sessions", response_model=list[SessionHistoryResponse])
def get_sessions_history(db: DBSession = Depends(get_db)):
    return history_logger.get_session_history(db)


@router.get("/feedback", response_model=list[GeneratedStarterResponse])
def get_feedback_history(db: DBSession = Depends(get_db)):
    return history_logger.get_feedback_history(db)


@router.get("/logs", response_model=list[LogEntryResponse])
def get_logs(db: DBSession = Depends(get_db)):
    from backend.models import LogEntry
    logs = db.query(LogEntry).order_by(LogEntry.Timestamp.desc()).limit(50).all()
    return logs
