from typing import Dict, List, Tuple

SUPPORTED_GENRES = {
    "pop", "rock", "hip-hop", "electronic", "jazz", "classical", "r&b", "lofi", "indie pop"
}

SUPPORTED_MOODS = {
    "happy", "sad", "calm", "energetic", "romantic", "angry", "chill"
}

def validate_query(query: str) -> Tuple[bool, str]:
    if query is None or not query.strip():
        return False, "Please enter a mood, artist, genre, or activity."
    if len(query.strip()) < 3:
        return False, "Your request is too short. Please provide a little more detail."
    return True, ""

def normalize_text(text: str) -> str:
    return text.strip().lower()

def build_fallback_response(message: str, confidence: float = 0.0) -> Dict:
    return {
        "status": "fallback",
        "message": message,
        "confidence": round(confidence, 2),
        "recommendations": [],
    }

def clamp_confidence(value: float) -> float:
    return max(0.0, min(1.0, round(value, 2)))