import logging
from typing import Optional

logger = logging.getLogger(__name__)

_pipeline = None


def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        try:
            from transformers import pipeline
            _pipeline = pipeline(
                "zero-shot-classification",
                model="distilbert-base-uncased",
                device=-1,
            )
            logger.info("DistilBERT zero-shot pipeline loaded.")
        except Exception as e:
            logger.error(f"Failed to load DistilBERT: {e}")
            _pipeline = None
    return _pipeline


DEFAULT_THEMES = [
    "technology",
    "climate change",
    "urban planning",
    "artificial intelligence",
    "healthcare",
    "finance",
    "education",
    "sustainability",
    "data science",
    "blockchain",
    "cybersecurity",
    "leadership",
    "innovation",
    "policy",
    "social impact",
]


def analyze_themes(event_description: str, candidate_labels: Optional[list[str]] = None) -> list[str]:
    pipe = _get_pipeline()
    if pipe is None:
        logger.warning("DistilBERT pipeline unavailable; returning default themes.")
        return DEFAULT_THEMES[:3]

    labels = candidate_labels or DEFAULT_THEMES
    try:
        result = pipe(event_description, candidate_labels=labels)
        scores = result["scores"]
        labels_out = result["labels"]
        combined = list(zip(scores, labels_out))
        combined.sort(key=lambda x: x[0], reverse=True)
        top_themes = [label for _, label in combined[:3]]
        logger.info(f"Themes extracted: {top_themes}")
        return top_themes
    except Exception as e:
        logger.error(f"Theme extraction failed: {e}")
        return DEFAULT_THEMES[:3]
