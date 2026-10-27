"""Emotion detection wrapper for the Coursera Watson NLP emotion service."""
from __future__ import annotations

import os
from typing import Any

import requests

# Standard endpoint used by the Coursera Skills Network emotion-detection lab.
# Override EMOTION_API_URL if your lab provides a different endpoint.
EMOTION_API_URL = os.getenv(
    "EMOTION_API_URL",
    "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict?version=2022-04-07",
)
EMOTION_API_KEY = os.getenv("EMOTION_API_KEY", "")
MODEL_ID = os.getenv("EMOTION_MODEL_ID", "emotion_aggregated-workflow_lang_en_stock")
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def _empty_result() -> dict[str, Any]:
    return {**{name: None for name in EMOTIONS}, "dominant_emotion": None}


def emotion_detector(text_to_analyze: str) -> dict[str, Any]:
    """Return five emotion scores and the dominant emotion.

    Blank input and HTTP 400 return null values. Other HTTP/network/JSON errors
    raise RuntimeError so the Flask layer can show a user-friendly message.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return _empty_result()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "grpc-metadata-mm-model-id": MODEL_ID,
    }
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
        raise RuntimeError(
            "Could not connect to the Watson emotion service. Check your network "
            "connection and EMOTION_API_URL."
        ) from exc

    if response.status_code == 400:
        return _empty_result()
    if not response.ok:
        raise RuntimeError(
            f"Watson emotion service returned HTTP {response.status_code}: "
            f"{response.text[:300]}"
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise RuntimeError("Watson emotion service returned invalid JSON.") from exc

    try:
        raw = payload["emotionPredictions"][0]["emotion"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("Unexpected Watson response format; expected emotionPredictions.") from exc

    result: dict[str, Any] = {}
    for emotion in EMOTIONS:
        score = raw.get(emotion)
        result[emotion] = score if isinstance(score, (int, float)) else None

    scores = {
        emotion: score
        for emotion, score in result.items()
        if isinstance(score, (int, float))
    }
    result["dominant_emotion"] = max(scores, key=scores.get) if scores else None
    return result
