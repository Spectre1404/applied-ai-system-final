from typing import Dict, List, Tuple
from src.recommender import recommend_songs
from src.guardrails import validate_query, normalize_text, build_fallback_response, clamp_confidence

def infer_prefs_from_query(query: str) -> Dict:
    q = normalize_text(query)
    prefs = {
        "genre": "",
        "mood": "",
        "energy": 0.5,
        "valence": 0.5,
        "likes_acoustic": False,
        "preferred_decade": "",
        "preferred_mood_tags": [],
        "min_popularity": 0,
    }

    genre_map = {
        "pop": "pop",
        "rock": "rock",
        "hip hop": "hip-hop",
        "rap": "hip-hop",
        "lofi": "lofi",
        "chillhop": "lofi",
        "electronic": "electronic",
        "edm": "electronic",
        "jazz": "jazz",
        "classical": "classical",
        "r&b": "r&b",
        "indie pop": "indie pop",
    }
    mood_map = {
        "happy": "happy",
        "sad": "sad",
        "calm": "calm",
        "chill": "chill",
        "energetic": "energetic",
        "romantic": "romantic",
        "angry": "angry",
        "workout": "energetic",
        "study": "calm",
        "coding": "calm",
        "focus": "calm",
        "party": "energetic",
    }

    for key, value in genre_map.items():
        if key in q:
            prefs["genre"] = value
            break

    for key, value in mood_map.items():
        if key in q:
            prefs["mood"] = value
            break

    if any(word in q for word in ["upbeat", "workout", "gym", "party", "energetic"]):
        prefs["energy"] = 0.85
        prefs["valence"] = 0.75
    elif any(word in q for word in ["calm", "study", "focus", "coding", "chill", "late-night"]):
        prefs["energy"] = 0.35
        prefs["valence"] = 0.55
        prefs["likes_acoustic"] = True
    elif any(word in q for word in ["sad", "melancholy", "melancholic"]):
        prefs["energy"] = 0.25
        prefs["valence"] = 0.2

    if "2020" in q:
        prefs["preferred_decade"] = "2020s"
    elif "2010" in q:
        prefs["preferred_decade"] = "2010s"

    return prefs

def keyword_retrieve(query: str, songs: List[Dict], limit: int = 20) -> List[Dict]:
    q = normalize_text(query)
    tokens = [t for t in q.replace(",", " ").split() if t]
    scored = []
    for song in songs:
        text = " ".join([
            str(song.get("title", "")),
            str(song.get("artist", "")),
            str(song.get("genre", "")),
            str(song.get("mood", "")),
            " ".join(song.get("mood_tags", [])),
            str(song.get("release_decade", "")),
        ]).lower()
        hits = sum(1 for t in tokens if t in text)
        if hits > 0:
            scored.append((song, hits))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [song for song, _ in scored[:limit]]

def recommend_from_query(query: str, songs: List[Dict], k: int = 5, mode: str = "balanced") -> Dict:
    ok, msg = validate_query(query)
    if not ok:
        return build_fallback_response(msg, confidence=0.0)

    prefs = infer_prefs_from_query(query)
    retrieved = keyword_retrieve(query, songs, limit=30)

    if not retrieved:
        retrieved = songs[:]

    recommendations = recommend_songs(prefs, retrieved, k=k, mode=mode, diversity=True)

    if not recommendations:
        return build_fallback_response(
            "I could not find a strong match in the dataset. Try a clearer genre, mood, or artist.",
            confidence=0.2,
        )

    conf = 0.55
    if prefs["genre"]:
        conf += 0.15
    if prefs["mood"]:
        conf += 0.15
    if len(retrieved) < len(songs):
        conf += 0.1
    confidence = clamp_confidence(conf)

    explanation = []
    for song, score, reasons in recommendations:
        explanation.append({
            "title": song["title"],
            "artist": song["artist"],
            "score": score,
            "reasons": reasons,
        })

    return {
        "status": "ok",
        "query": query,
        "inferred_preferences": prefs,
        "retrieved_count": len(retrieved),
        "confidence": confidence,
        "recommendations": explanation,
    }
