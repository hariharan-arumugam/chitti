"""Tamil speech in and out, using Sarvam AI's REST API.

Lesson 2: speech-to-text (STT) and text-to-speech (TTS) are just HTTP calls.
Audio goes up, text comes back; text goes up, audio comes back.
Docs: https://docs.sarvam.ai
"""
import base64
import json
import os

import requests

SARVAM_URL = "https://api.sarvam.ai"

# Lesson 2b: "keyterms" tell the ears which words to expect. Short, colloquial
# words like சாப்டீங்களா are the hardest to catch, so we list them here.
# Up to 50 terms. Add any word Chitti keeps mishearing.
KEYTERMS = [
    "சாப்டீங்களா",
    "என்ன பண்றீங்க",
    "மாத்திரை",
    "மூட்டு வலி",
    "நெஞ்சு வலி",
    "தூக்கம் வரல",
    "போர் அடிக்குது",
    "சிட்டி",
]


def _headers() -> dict:
    return {"api-subscription-key": os.environ["SARVAM_API_KEY"]}


def speech_to_text(wav_bytes: bytes) -> str:
    """Turn a short Tamil recording (under 30 seconds) into Tamil text."""
    response = requests.post(
        f"{SARVAM_URL}/speech-to-text",
        headers=_headers(),
        files={"file": ("speech.wav", wav_bytes, "audio/wav")},
        data={
            "model": "saaras:v4",
            "language_code": "ta-IN",
            "keyterms": json.dumps(KEYTERMS, ensure_ascii=False),
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["transcript"]


def text_to_speech(text: str) -> bytes:
    """Turn Tamil text into spoken audio (WAV bytes)."""
    response = requests.post(
        f"{SARVAM_URL}/text-to-speech",
        headers=_headers(),
        json={
            "text": text[:2500],
            "language_code": "ta-IN",
            "model": "bulbul:v3",
            "speaker": "kavitha",  # try others: see the speaker list in the README
            "pace": 0.9,  # a little slower than normal, kinder for elders
        },
        timeout=30,
    )
    response.raise_for_status()
    return base64.b64decode("".join(response.json()["audios"]))
