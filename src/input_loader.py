"""Multi-format user-story loading and normalization.

Supports plain text, markdown, and JSON inputs (bonus: multi-format support).
Whatever the format, the output is a single normalized string that combines the
user story with its acceptance criteria, ready to feed the analyst.
"""

import json
from pathlib import Path


class InputError(Exception):
    """Raised when input is missing, empty, or malformed."""


def _from_json(raw: str) -> str:
    """Accept a JSON object with a user_story and optional acceptance_criteria."""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InputError(f"Input looks like JSON but failed to parse: {exc}") from exc

    if isinstance(data, str):
        return data.strip()

    if not isinstance(data, dict):
        raise InputError("JSON input must be an object or a string.")

    story = data.get("user_story") or data.get("story") or ""
    criteria = data.get("acceptance_criteria") or data.get("criteria") or []

    parts = [str(story).strip()]
    if criteria:
        parts.append("\nAcceptance Criteria:")
        if isinstance(criteria, list):
            parts.extend(f"- {c}" for c in criteria)
        else:
            parts.append(str(criteria))
    normalized = "\n".join(p for p in parts if p).strip()
    if not normalized:
        raise InputError("JSON input did not contain a user story.")
    return normalized


def normalize_story(raw: str, fmt: str = "auto") -> str:
    """Normalize raw input text into a single story+criteria string.

    fmt: "auto" (default), "json", "text", or "markdown". text and markdown are
    treated identically since the LLM reads both as prose.
    """
    if raw is None or not str(raw).strip():
        raise InputError("Empty input: a user story is required.")

    raw = str(raw).strip()

    if fmt == "json" or (fmt == "auto" and raw[0] in "{["):
        return _from_json(raw)

    # text / markdown: pass through, trimmed.
    return raw


def load_story(source: str, fmt: str = "auto") -> str:
    """Load a story from a file path if it exists, otherwise treat as literal text."""
    path = Path(source)
    if path.exists() and path.is_file():
        raw = path.read_text(encoding="utf-8")
        if fmt == "auto":
            fmt = "json" if path.suffix.lower() == ".json" else "text"
        return normalize_story(raw, fmt)
    # Not a file: treat the argument itself as the story text.
    return normalize_story(source, fmt)
