import pytest
from unittest.mock import patch, MagicMock

from backend.services.event_analyzer import analyze_themes, DEFAULT_THEMES


class TestEventAnalyzer:
    @patch("backend.services.event_analyzer._get_pipeline")
    def test_analyze_themes_returns_list_of_strings(self, mock_pipeline, sample_event_description):
        mock_instance = MagicMock()
        mock_instance.return_value = {
            "labels": ["technology", "climate change", "urban planning", "sustainability", "innovation"],
            "scores": [0.85, 0.72, 0.68, 0.55, 0.42],
        }
        mock_pipeline.return_value = mock_instance
        themes = analyze_themes(sample_event_description)
        assert isinstance(themes, list)
        assert len(themes) > 0
        assert all(isinstance(t, str) for t in themes)

    @patch("backend.services.event_analyzer._get_pipeline")
    def test_analyze_themes_limited_to_three(self, mock_pipeline, sample_event_description):
        mock_instance = MagicMock()
        mock_instance.return_value = {
            "labels": ["a", "b", "c", "d", "e"],
            "scores": [0.9, 0.8, 0.7, 0.6, 0.5],
        }
        mock_pipeline.return_value = mock_instance
        themes = analyze_themes(sample_event_description)
        assert len(themes) <= 3

    @patch("backend.services.event_analyzer._get_pipeline")
    def test_analyze_themes_with_custom_labels(self, mock_pipeline):
        mock_instance = MagicMock()
        mock_instance.return_value = {
            "labels": ["sports", "music", "technology", "art"],
            "scores": [0.1, 0.85, 0.05, 0.0],
        }
        mock_pipeline.return_value = mock_instance
        custom_labels = ["sports", "music", "technology", "art"]
        themes = analyze_themes("Jazz music festival", candidate_labels=custom_labels)
        assert all(t in custom_labels for t in themes)
        assert "music" in themes

    @patch("backend.services.event_analyzer._get_pipeline", return_value=None)
    def test_analyze_themes_empty_description(self, mock_pipeline):
        themes = analyze_themes("")
        assert isinstance(themes, list)
        assert len(themes) <= 3

    @patch("backend.services.event_analyzer._get_pipeline", return_value=None)
    def test_analyze_themes_fallback_on_pipeline_failure(self, mock_pipeline):
        themes = analyze_themes("Some event description")
        assert themes == DEFAULT_THEMES[:3]

    @patch("backend.services.event_analyzer._get_pipeline", return_value=None)
    def test_analyze_themes_pipeline_exception(self, mock_pipeline):
        themes = analyze_themes("Some event")
        assert len(themes) == 3
        assert themes == DEFAULT_THEMES[:3]

    @patch("backend.services.event_analyzer._get_pipeline")
    def test_analyze_themes_deduplicates(self, mock_pipeline, sample_event_description):
        mock_instance = MagicMock()
        mock_instance.return_value = {
            "labels": ["tech", "climate", "urban", "tech"],
            "scores": [0.9, 0.8, 0.7, 0.6],
        }
        mock_pipeline.return_value = mock_instance
        themes = analyze_themes(sample_event_description, candidate_labels=["tech", "climate", "urban", "tech"])
        seen = set()
        for t in themes:
            assert t not in seen
            seen.add(t)
