import json

from anthropic import Anthropic

from app.config import get_settings

_client: Anthropic | None = None


def _get_client() -> Anthropic:
    global _client
    settings = get_settings()
    if not settings.anthropic_api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")
    if _client is None:
        _client = Anthropic(api_key=settings.anthropic_api_key)
    return _client


def ask_claude_json(prompt: str, max_tokens: int = 2000) -> dict:
    """
    Send a prompt that instructs Claude to respond with only a JSON object, and parse the
    result. Raises ValueError if the response isn't valid JSON — callers should catch that
    and return a 502 to the client rather than a raw 500.
    """
    client = _get_client()
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(block.text for block in response.content if block.type == "text").strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    return json.loads(text)
