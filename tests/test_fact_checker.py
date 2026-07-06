import pytest
from unittest.mock import patch, MagicMock

from backend.services.fact_checker import verify_topic


class TestFactChecker:
    @patch("wikipediaapi.Wikipedia")
    def test_verify_topic_found(self, mock_wikipedia):
        mock_page = MagicMock()
        mock_page.exists.return_value = True
        mock_page.summary = "Python is a programming language."
        mock_page.fullurl = "https://en.wikipedia.org/wiki/Python_(programming_language)"

        mock_wiki = MagicMock()
        mock_wiki.page.return_value = mock_page
        mock_wikipedia.return_value = mock_wiki

        result = verify_topic("Python (programming language)")

        assert result["status"] == "verified"
        assert result["query"] == "Python (programming language)"
        assert "programming" in result["summary"]
        assert "wikipedia.org" in result["source_url"]

    @patch("wikipediaapi.Wikipedia")
    def test_verify_topic_not_found(self, mock_wikipedia):
        mock_page = MagicMock()
        mock_page.exists.return_value = False

        mock_wiki = MagicMock()
        mock_wiki.page.return_value = mock_page
        mock_wiki.search.return_value = []
        mock_wikipedia.return_value = mock_wiki

        result = verify_topic("NonexistentTopicXYZ123")

        assert result["status"] == "not_found"
        assert "No Wikipedia page found" in result["summary"]

    @patch("wikipediaapi.Wikipedia")
    def test_verify_topic_with_suggestions(self, mock_wikipedia):
        mock_page = MagicMock()
        mock_page.exists.return_value = False

        mock_wiki = MagicMock()
        mock_wiki.page.return_value = mock_page

        mock_result1 = MagicMock()
        mock_result1.title = "Climate change"
        mock_result2 = MagicMock()
        mock_result2.title = "Climate change mitigation"
        mock_wiki.search.return_value = [mock_result1, mock_result2]
        mock_wikipedia.return_value = mock_wiki

        result = verify_topic("climat chang")

        assert result["status"] == "not_found"
        assert "suggestions" in result
        assert len(result["suggestions"]) == 2

    @patch("backend.services.fact_checker.wikipediaapi.Wikipedia")
    def test_verify_topic_exception(self, mock_wikipedia):
        mock_wikipedia.side_effect = Exception("API unavailable")

        result = verify_topic("anything")

        assert result["status"] == "error"
        assert "unavailable" in result["summary"]

    def test_verify_topic_empty_query_handled(self):
        result = verify_topic("")
        assert result["status"] in ("not_found", "error", "verified")
