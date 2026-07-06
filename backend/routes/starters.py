from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from backend.database import get_db
from backend.schemas import (
    GenerateStartersRequest,
    GenerateStartersResponse,
    StarterFeedbackRequest,
    GeneratedStarterResponse,
)
from backend.services import event_analyzer, topic_generator, history_logger, feedback_logger

router = APIRouter(prefix="/api/starters", tags=["starters"])


@router.post("/generate", response_model=GenerateStartersResponse)
def generate_starters(req: GenerateStartersRequest, db: DBSession = Depends(get_db)):
    themes = event_analyzer.analyze_themes(req.event_description)
    if req.interests:
        themes = list(dict.fromkeys(themes + [t.strip() for t in req.interests.split(",") if t.strip()]))

    starters = topic_generator.generate_starters(req.event_description, themes, req.interests)

    user = history_logger.get_or_create_user(db, bio_text=req.interests)
    event = history_logger.create_event_context(db, description=req.event_description, themes=", ".join(themes))
    session = history_logger.create_session(db, user_id=user.UserID, event_id=event.EventID)

    starter_objects = []
    for s in starters:
        obj = history_logger.create_starter(db, session_id=session.SessionID, starter_text=s, context_prompt=req.event_description[:100])
        starter_objects.append(obj)

    history_logger.create_log(
        db,
        action_type="STARTERS_GENERATED",
        payload={"event_description": req.event_description, "themes": themes, "starter_count": len(starters)},
        session_id=session.SessionID,
    )

    return GenerateStartersResponse(
        session_id=session.SessionID,
        starters=[s.StarterText for s in starter_objects],
        themes=themes,
    )


@router.post("/feedback", response_model=GeneratedStarterResponse)
def submit_feedback(req: StarterFeedbackRequest, db: DBSession = Depends(get_db)):
    starter = feedback_logger.record_feedback(db, req.starter_id, req.feedback)
    if starter is None:
        raise HTTPException(status_code=404, detail="Starter not found")
    history_logger.create_log(
        db,
        action_type="FEEDBACK_SUBMITTED",
        payload={"starter_id": req.starter_id, "feedback": req.feedback},
        session_id=starter.SessionID,
    )
    return starter


@router.get("/session/{session_id}", response_model=list[GeneratedStarterResponse])
def get_session_starters(session_id: int, db: DBSession = Depends(get_db)):
    from backend.models import GeneratedStarter
    starters = db.query(GeneratedStarter).filter(GeneratedStarter.SessionID == session_id).all()
    return starters
