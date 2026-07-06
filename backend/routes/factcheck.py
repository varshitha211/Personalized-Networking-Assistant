from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession

from backend.database import get_db
from backend.schemas import FactCheckRequest, FactCheckResponse, WikipediaFactCheckResponse
from backend.services import fact_checker, history_logger

router = APIRouter(prefix="/api/factcheck", tags=["factcheck"])


@router.post("/", response_model=FactCheckResponse)
def verify_topic(req: FactCheckRequest, db: DBSession = Depends(get_db)):
    result = fact_checker.verify_topic(req.query)

    user = history_logger.get_or_create_user(db)
    event = history_logger.create_event_context(db, description=f"Fact check: {req.query}")
    session = history_logger.create_session(db, user_id=user.UserID, event_id=event.EventID)

    fc = history_logger.create_fact_check(
        db,
        session_id=session.SessionID,
        query=result["query"],
        status=result["status"],
        source_url=result.get("source_url", ""),
    )

    history_logger.create_log(
        db,
        action_type="FACT_CHECK",
        payload={"query": req.query, "status": result["status"]},
        session_id=session.SessionID,
    )

    return FactCheckResponse(
        query=result["query"],
        summary=result["summary"],
        source_url=result.get("source_url", ""),
        status=result["status"],
        fact_check_id=fc.FactCheckID,
    )


@router.get("/", response_model=list[WikipediaFactCheckResponse])
def list_fact_checks(db: DBSession = Depends(get_db)):
    from backend.models import WikipediaFactCheck
    checks = db.query(WikipediaFactCheck).order_by(WikipediaFactCheck.FactCheckID.desc()).all()
    return checks
