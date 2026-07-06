import logging

import wikipediaapi

logger = logging.getLogger(__name__)


def verify_topic(query: str) -> dict:
    try:
        user_agent = "PersonalizedNetworkingAssistant/1.0 (contact@example.com)"
        wiki = wikipediaapi.Wikipedia(user_agent, "en")
        page = wiki.page(query)
        if not page.exists():
            suggestions = _search_suggestions(query, wiki)
            return {
                "query": query,
                "summary": f"No Wikipedia page found for '{query}'.",
                "source_url": "",
                "status": "not_found",
                "suggestions": suggestions,
            }
        summary = page.summary[:500] if page.summary else "No summary available."
        source_url = page.fullurl
        return {
            "query": query,
            "summary": summary,
            "source_url": source_url,
            "status": "verified",
        }
    except Exception as e:
        logger.error(f"Wikipedia lookup failed: {e}")
        return {
            "query": query,
            "summary": f"Fact-checking service unavailable: {e}",
            "source_url": "",
            "status": "error",
        }


def _search_suggestions(query: str, wiki: wikipediaapi.Wikipedia) -> list[str]:
    try:
        search_results = wiki.search(query, limit=5)
        return [r.title for r in (search_results or [])]
    except Exception:
        return []
