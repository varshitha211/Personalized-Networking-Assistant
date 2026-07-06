import logging
from typing import Optional

from sqlalchemy.orm import Session as DBSession

from backend.models import GeneratedStarter

logger = logging.getLogger(__name__)


def record_feedback(
    db: DBSession, starter_id: int, feedback: int
) -> Optional[GeneratedStarter]:
    starter = db.query(GeneratedStarter).filter(GeneratedStarter.StarterID == starter_id).first()
    if not starter:
        logger.warning(f"Starter {starter_id} not found for feedback.")
        return None
    starter.Feedback = feedback
    db.commit()
    db.refresh(starter)
    logger.info(f"Feedback recorded for starter {starter_id}: {feedback}")
    return starter
