import logging
import re

logger = logging.getLogger(__name__)

_generator = None


def _get_generator():
    global _generator
    if _generator is None:
        try:
            from transformers import pipeline
            _generator = pipeline(
                "text-generation",
                model="gpt2",
                device=-1,
            )
            logger.info("GPT-2 text-generation pipeline loaded.")
        except Exception as e:
            logger.error(f"Failed to load GPT-2: {e}")
            _generator = None
    return _generator


def generate_starters(event_description: str, themes: list[str], interests: str = "") -> list[str]:
    gen = _get_generator()
    if gen is None:
        logger.warning("GPT-2 pipeline unavailable; returning fallback starters.")
        return _fallback_starters(event_description, themes, interests)

    themes_str = ", ".join(themes)
    interests_str = f" I am interested in {interests}." if interests else ""

    prompts = [
        f"A conversation starter at a {themes_str} networking event:",
        f"At a conference about {event_description[:60]}, I could ask:",
        f"Talking to someone interested in {themes_str}:",
    ]

    starters = []
    for prompt in prompts:
        try:
            full_prompt = prompt + interests_str
            result = gen(
                full_prompt,
                max_new_tokens=40,
                num_return_sequences=1,
                temperature=0.8,
                top_p=0.9,
                do_sample=True,
                pad_token_id=50256,
            )
            text = result[0]["generated_text"]
            cleaned = _clean_starter(text, full_prompt)
            if cleaned and len(cleaned) > 15:
                starters.append(cleaned)
        except Exception as e:
            logger.warning(f"Generation failed for prompt: {e}")

    if not starters:
        return _fallback_starters(event_description, themes, interests)

    while len(starters) < 3:
        starters.append(_fallback_starters(event_description, themes, interests)[len(starters) % 3])

    return starters[:3]


def _clean_starter(text: str, prompt: str) -> str:
    cleaned = text.replace(prompt, "").strip()
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = cleaned.strip('.,;:!?')
    return cleaned.strip()


def _fallback_starters(event_description: str, themes: list[str], interests: str) -> list[str]:
    theme = themes[0] if themes else "this topic"
    return [
        f"What excites you most about {theme} in the context of {event_description[:50]}?",
        f"How did you first get involved with {theme}?",
        f"What trends in {theme} do you think will be most impactful in the next few years?",
    ]
