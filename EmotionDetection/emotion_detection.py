"""Emotion detection wrapper around the Watson NLP emotion model API.

Set EMOTION_API_URL to the service endpoint supplied in your Coursera lab.
The endpoint is intentionally configurable because lab environments may use
slightly different URLs.
"""
from __future__ import annotations

import os
from typing import Any

import requests

EMOTION_API_URL = os.getenv("EMOTION_API_URL", "")
EMOTION_API_KEY = os.getenv("EMOTION_API_KEY", "")
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze: str) -> dict[str, Any]:
    """Return five emotion scores and the dominant emotion.

    The Coursera Watson NLP lab uses a text input and returns a JSON payload
    containing emotion predictions. Configure EMOTION_API_URL to the exact
    endpoint from your lab before calling this function.

    HTTP 400 is treated as invalid input and returns a null-valued structure.
    Other non-success responses raise an informative RuntimeError.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return {**{name: None for name in EMOTIONS}, "dominant_emotion": None}
    if not EMOTION_API_URL:
        raise RuntimeError(
            "EMOTION_API_URL is not configured. Set it to the Watson NLP "
            "emotion endpoint provided by your Coursera lab."
        )

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if EMOTION_API_KEY:
        headers["Authorization"] = f"Bearer {EMOTION_API_KEY}"

    try:
        response = requests.post(
            EMOTION_API_URL,
            json={"raw_document": {"text": text_to_analyze}},
            headers=headers,
            timeout=20,
        )
    except requests.RequestException as exc:
        raise RuntimeError(f"Emotion service request failed: {exc}") from exc

    if response.status_code == 400:
        return {**{name: None for name in EMOTIONS}, "dominant_emotion": None}
    if not response.ok:
        raise RuntimeError(
            f"Emotion service returned HTTP {response.status_code}: {response.text[:300]}"
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise RuntimeError("Emotion service returned invalid JSON") from exc

    # Support the common Watson NLP response shape and the Coursera lab's
    # simplified shape. Verify the exact payload against your lab response.
    predictions = payload.get("emotionPredictions", [])
    if predictions:
        raw = predictions[0].get("emotion", {})
    else:
        raw = payload.get("emotion", payload.get("emotions", {}))
    if not isinstance(raw, dict):
        raise RuntimeError("Unexpected emotion response format")

    result: dict[str, Any] = {name: raw.get(name) for name in EMOTIONS}
    available = {name: score for name, score in result.items() if isinstance(score, (int, float))}
    result["dominant_emotion"] = max(available, key=available.get) if available else None
    return result
