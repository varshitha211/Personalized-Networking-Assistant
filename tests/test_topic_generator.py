import pytest
from unittest.mock import patch, MagicMock

from backend.services.topic_generator import generate_starters, _fallback_starters


class TestTopicGenerator:
    @patch("backend.services.topic_generator._get_generator")
    def test_generate_starters_returns_list(self, mock_gen, sample_event_description):
        mock_instance = MagicMock()
        mock_instance.return_value = [{"generated_text": "Have you explored how AI is reshaping urban sustainability?"}]
        mock_gen.return_value = mock_instance
        themes = ["technology", "climate change", "urban planning"]
        starters = generate_starters(sample_event_description, themes)
        assert isinstance(starters, list)
        assert len(starters) > 0

    @patch("backend.services.topic_generator._get_generator")
    def test_generate_starters_returns_up_to_three(self, mock_gen, sample_event_description):
        mock_instance = MagicMock()
        mock_instance.return_value = [{"generated_text": "What trends in tech excite you?"}]
        mock_gen.return_value = mock_instance
        themes = ["technology"]
        starters = generate_starters(sample_event_description, themes)
        assert len(starters) <= 3

    @patch("backend.services.topic_generator._get_generator", return_value=None)
    def test_generate_starters_fallback_on_no_pipeline(self, mock_gen, sample_event_description):
        themes = ["technology"]
        starters = generate_starters(sample_event_description, themes)
        assert len(starters) == 3

    @patch("backend.services.topic_generator._get_generator")
    def test_generate_starters_with_interests(self, mock_gen, sample_event_description):
        mock_instance = MagicMock()
        mock_instance.return_value = [{"generated_text": "I work on climate data science, what about you?"}]
        mock_gen.return_value = mock_instance
        themes = ["technology"]
        starters = generate_starters(sample_event_description, themes, interests="climate change")
        assert len(starters) > 0

    def test_fallback_starters_format(self, sample_event_description):
        themes = ["artificial intelligence"]
        starters = _fallback_starters(sample_event_description, themes, "")
        assert len(starters) == 3
        assert all(isinstance(s, str) and len(s) > 10 for s in starters)

    def test_fallback_contains_theme(self):
        themes = ["blockchain"]
        starters = _fallback_starters("Tech Conference", themes, "")
        assert any("blockchain" in s for s in starters)

    def test_empty_themes_uses_default(self):
        starters = _fallback_starters("Event", [], "")
        assert len(starters) == 3

    @patch("backend.services.topic_generator._get_generator")
    def test_generate_starters_string_output(self, mock_gen, sample_event_description):
        mock_instance = MagicMock()
        mock_instance.return_value = [{"generated_text": "How did you get into data science?"}]
        mock_gen.return_value = mock_instance
        themes = ["data science"]
        starters = generate_starters(sample_event_description, themes)
        for s in starters:
            assert isinstance(s, str)
