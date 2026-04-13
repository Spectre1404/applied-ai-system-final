from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Song:
    """Represents a song and its attributes. Required by tests/test_recommender.py"""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: float = 0.0
    release_decade: str = "2020s"
    mood_tags: List[str] = field(default_factory=list)
    explicit_language: bool = False
    key: str = "C"


@dataclass
class UserProfile:
    """Represents a user's taste preferences. Required by tests/test_recommender.py"""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    preferred_decade: str = ""
    preferred_mood_tags: List[str] = field(default_factory=list)
    min_popularity: float = 0.0


# ---------------------------------------------------------------------------
# Neighbor Maps
# ---------------------------------------------------------------------------

GENRE_NEIGHBORS = {
    "pop":        ["indie pop", "dance pop", "electropop"],
    "rock":       ["indie rock", "alternative", "classic rock"],
    "hip-hop":    ["rap", "trap", "r&b"],
    "electronic": ["edm", "house", "techno", "synth-pop"],
    "jazz":       ["blues", "soul", "bossa nova"],
    "classical":  ["orchestral", "acoustic"],
    "r&b":        ["soul", "hip-hop", "funk"],
    "lofi":       ["indie pop", "chillhop", "ambient"],
    "indie pop":  ["pop", "lofi", "folk"],
}

MOOD_NEIGHBORS = {
    "happy":      ["energetic", "uplifting", "euphoric"],
    "sad":        ["melancholic", "somber", "nostalgic"],
    "calm":       ["relaxed", "peaceful", "chill"],
    "energetic":  ["happy", "intense", "hype"],
    "romantic":   ["sensual", "calm", "dreamy"],
    "angry":      ["intense", "aggressive"],
    "chill":      ["calm", "relaxed", "peaceful"],
}

DECADE_ORDER = ["1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]

SCORING_MODES = {
    "balanced":      {"genre": 2.0, "mood": 1.5, "energy": 1.0, "valence": 0.5, "acousticness": 0.5},
    "genre_first":   {"genre": 4.0, "mood": 0.5, "energy": 0.5, "valence": 0.25, "acousticness": 0.25},
    "mood_first":    {"genre": 0.5, "mood": 3.0, "energy": 1.0, "valence": 1.0, "acousticness": 0.5},
    "energy_focused":{"genre": 1.0, "mood": 0.5, "energy": 3.0, "valence": 0.5, "acousticness": 0.5},
    "vibe_match":    {"genre": 1.5, "mood": 2.0, "energy": 1.5, "valence": 1.5, "acousticness": 0.5},
}


# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with typed values."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mood_tags_raw = row.get("mood_tags", "")
            mood_tags = [t.strip() for t in mood_tags_raw.strip('"').split(",") if t.strip()]
            songs.append({
                "id":               int(row["id"]),
                "title":            row["title"],
                "artist":           row["artist"],
                "genre":            row["genre"],
                "mood":             row["mood"],
                "energy":           float(row["energy"]),
                "tempo_bpm":        int(row["tempo_bpm"]),
                "valence":          float(row["valence"]),
                "danceability":     float(row["danceability"]),
                "acousticness":     float(row["acousticness"]),
                "popularity":       float(row.get("popularity", 50)),
                "release_decade":   row.get("release_decade", "2020s"),
                "mood_tags":        mood_tags,
                "explicit_language": row.get("explicit_language", "false").lower() == "true",
                "key":              row.get("key", "C"),
            })
    return songs


# ---------------------------------------------------------------------------
# Challenge 1: Advanced Feature Scoring
# ---------------------------------------------------------------------------

def score_advanced_features(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score 5 advanced features: popularity, decade, mood tags, explicit filter, musical key."""
    score = 0.0
    reasons = []

    # Feature 1: Popularity boost (max 0.5)
    popularity = song.get("popularity", 50)
    min_pop = user_prefs.get("min_popularity", 0)
    if popularity >= min_pop:
        pop_score = round((popularity / 100) * 0.5, 2)
        score += pop_score
        reasons.append(f"popularity score (+{pop_score})")

    # Feature 2: Release decade match (max 1.0)
    preferred_decade = user_prefs.get("preferred_decade", "")
    song_decade = song.get("release_decade", "")
    if preferred_decade and song_decade == preferred_decade:
        score += 1.0
        reasons.append(f"decade match {song_decade} (+1.0)")
    elif preferred_decade and preferred_decade in DECADE_ORDER and song_decade in DECADE_ORDER:
        pref_idx = DECADE_ORDER.index(preferred_decade)
        song_idx = DECADE_ORDER.index(song_decade)
        closeness = 1 - abs(pref_idx - song_idx) / len(DECADE_ORDER)
        decade_score = round(closeness * 0.5, 2)
        score += decade_score
        reasons.append(f"nearby decade {song_decade} (+{decade_score})")

    # Feature 3: Mood tags overlap (max 1.5, +0.5 per matching tag)
    preferred_tags = set(user_prefs.get("preferred_mood_tags", []))
    song_tags = set(song.get("mood_tags", []))
    matching_tags = preferred_tags & song_tags
    if matching_tags:
        tag_score = round(min(len(matching_tags) * 0.5, 1.5), 2)
        score += tag_score
        reasons.append(f"mood tags match {sorted(matching_tags)} (+{tag_score})")

    # Feature 4: Explicit content penalty (-1.0 if user prefers clean)
    prefers_clean = user_prefs.get("prefers_clean", False)
    if prefers_clean and song.get("explicit_language", False):
        score -= 1.0
        reasons.append("explicit content penalty (-1.0)")

    # Feature 5: Musical key affinity (max 0.5)
    user_mood = user_prefs.get("mood", "")
    song_key = song.get("key", "")
    minor_keys = ["Am", "Em", "Dm", "Bm", "Cm", "Fm", "Gm"]
    major_keys = ["C", "G", "D", "A", "F", "Bb", "Eb", "F#"]
    if user_mood in ["sad", "angry", "melancholic"] and song_key in minor_keys:
        score += 0.5
        reasons.append(f"minor key match {song_key} (+0.5)")
    elif user_mood in ["happy", "energetic", "romantic"] and song_key in major_keys:
        score += 0.5
        reasons.append(f"major key match {song_key} (+0.5)")

    return round(score, 2), reasons


# ---------------------------------------------------------------------------
# Challenge 2: Mode-Aware Scoring (Strategy Pattern)
# ---------------------------------------------------------------------------

def score_song_with_mode(user_prefs: Dict, song: Dict, mode: str = "balanced") -> Tuple[float, List[str]]:
    """Score a song using a named scoring mode that adjusts feature weights."""
    weights = SCORING_MODES.get(mode, SCORING_MODES["balanced"])
    score = 0.0
    reasons = [f"[mode: {mode}]"]

    user_genre = user_prefs.get("genre", "")
    song_genre = song["genre"]
    if song_genre == user_genre:
        pts = weights["genre"]
        score += pts
        reasons.append(f"genre match (+{pts})")
    elif song_genre in GENRE_NEIGHBORS.get(user_genre, []):
        pts = round(weights["genre"] * 0.5, 2)
        score += pts
        reasons.append(f"similar genre (+{pts})")

    user_mood = user_prefs.get("mood", "")
    song_mood = song["mood"]
    if song_mood == user_mood:
        pts = weights["mood"]
        score += pts
        reasons.append(f"mood match (+{pts})")
    elif song_mood in MOOD_NEIGHBORS.get(user_mood, []):
        pts = round(weights["mood"] * 0.5, 2)
        score += pts
        reasons.append(f"close mood (+{pts})")

    user_energy = user_prefs.get("energy", 0.5)
    energy_score = round(weights["energy"] * (1 - abs(user_energy - song["energy"])), 2)
    score += energy_score
    reasons.append(f"energy proximity (+{energy_score})")

    user_valence = user_prefs.get("valence", 0.5)
    valence_score = round(weights["valence"] * (1 - abs(user_valence - song["valence"])), 2)
    score += valence_score
    reasons.append(f"valence proximity (+{valence_score})")

    likes_acoustic = user_prefs.get("likes_acoustic", False)
    if likes_acoustic and song["acousticness"] >= 0.6:
        score += weights["acousticness"]
        reasons.append(f"acoustic match (+{weights['acousticness']})")
    elif not likes_acoustic and song["acousticness"] < 0.4:
        score += weights["acousticness"]
        reasons.append(f"electronic match (+{weights['acousticness']})")

    adv_score, adv_reasons = score_advanced_features(user_prefs, song)
    score += adv_score
    reasons.extend(adv_reasons)

    return round(score, 2), reasons


# ---------------------------------------------------------------------------
# Base score_song (used by OOP Recommender and tests)
# ---------------------------------------------------------------------------

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song using balanced mode. Returns (score, reasons)."""
    return score_song_with_mode(user_prefs, song, mode="balanced")


# ---------------------------------------------------------------------------
# Challenge 3: Diversity Penalty
# ---------------------------------------------------------------------------

def apply_diversity_penalty(
    scored: List[Tuple[Dict, float, List[str]]],
    max_per_artist: int = 2,
    max_per_genre: int = 2,
    penalty: float = 1.5,
) -> List[Tuple[Dict, float, List[str]]]:
    """Penalize songs whose artist or genre already appears too often in top results."""
    artist_counts: Dict[str, int] = {}
    genre_counts: Dict[str, int] = {}
    result = []
    for song, score, reasons in scored:
        artist = song["artist"]
        genre = song["genre"]
        new_score = score
        new_reasons = reasons[:]
        if artist_counts.get(artist, 0) >= max_per_artist:
            new_score = round(new_score - penalty, 2)
            new_reasons.append(f"diversity penalty: artist '{artist}' (-{penalty})")
        if genre_counts.get(genre, 0) >= max_per_genre:
            new_score = round(new_score - penalty, 2)
            new_reasons.append(f"diversity penalty: genre '{genre}' (-{penalty})")
        artist_counts[artist] = artist_counts.get(artist, 0) + 1
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
        result.append((song, new_score, new_reasons))
    return sorted(result, key=lambda x: x[1], reverse=True)


# ---------------------------------------------------------------------------
# Challenge 4: ASCII Table Output
# ---------------------------------------------------------------------------

def format_recommendations_table(
    recommendations: List[Tuple[Dict, float, str]],
    profile_name: str,
) -> str:
    """Format recommendations as a readable ASCII table with rank, title, score, and reasons."""
    col = {"rank": 4, "title": 22, "artist": 18, "score": 7, "reasons": 50}
    div = "+" + "+".join("-" * (w + 2) for w in col.values()) + "+"

    def row(rank, title, artist, score, reasons):
        return (
            f"| {str(rank):<{col['rank']}} "
            f"| {title[:col['title']]:<{col['title']}} "
            f"| {artist[:col['artist']]:<{col['artist']}} "
            f"| {str(score):<{col['score']}} "
            f"| {reasons[:col['reasons']]:<{col['reasons']}} |"
        )

    lines = [
        f"\n🎵 Profile: {profile_name}",
        div,
        row("#", "Title", "Artist", "Score", "Reasons"),
        div,
    ]
    for i, (song, score, reasons) in enumerate(recommendations, 1):
        lines.append(row(i, song["title"], song["artist"], f"{score:.2f}", reasons))
    lines.append(div)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Core Recommend Function
# ---------------------------------------------------------------------------

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
    diversity: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """Score all songs, optionally apply diversity penalty, sort descending, return top k."""
    scored = []
    for song in songs:
        score, reasons = score_song_with_mode(user_prefs, song, mode=mode)
        scored.append((song, score, reasons))

    ranked = sorted(scored, key=lambda x: x[1], reverse=True)

    if diversity:
        ranked = apply_diversity_penalty(ranked)

    return [(song, score, ", ".join(reasons)) for song, score, reasons in ranked[:k]]


# ---------------------------------------------------------------------------
# OOP Recommender (required by tests/test_recommender.py)
# ---------------------------------------------------------------------------

class Recommender:
    """OOP implementation of the recommendation logic. Required by tests/test_recommender.py"""

    def __init__(self, songs: List[Song]):
        """Initialize the recommender with a list of Song objects."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score and rank all songs for the given user profile, returning the top k Song objects."""
        user_prefs = {
            "genre":               user.favorite_genre,
            "mood":                user.favorite_mood,
            "energy":              user.target_energy,
            "likes_acoustic":      user.likes_acoustic,
            "valence":             0.5,
            "preferred_decade":    user.preferred_decade,
            "preferred_mood_tags": user.preferred_mood_tags,
            "min_popularity":      user.min_popularity,
        }
        scored = []
        for song in self.songs:
            song_dict = {
                "genre":            song.genre,
                "mood":             song.mood,
                "energy":           song.energy,
                "valence":          song.valence,
                "acousticness":     song.acousticness,
                "popularity":       song.popularity,
                "release_decade":   song.release_decade,
                "mood_tags":        song.mood_tags,
                "explicit_language": song.explicit_language,
                "key":              song.key,
            }
            score, _ = score_song(user_prefs, song_dict)
            scored.append((song, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended to the user."""
        user_prefs = {
            "genre":               user.favorite_genre,
            "mood":                user.favorite_mood,
            "energy":              user.target_energy,
            "likes_acoustic":      user.likes_acoustic,
            "valence":             0.5,
            "preferred_decade":    user.preferred_decade,
            "preferred_mood_tags": user.preferred_mood_tags,
            "min_popularity":      user.min_popularity,
        }
        song_dict = {
            "genre":            song.genre,
            "mood":             song.mood,
            "energy":           song.energy,
            "valence":          song.valence,
            "acousticness":     song.acousticness,
            "popularity":       song.popularity,
            "release_decade":   song.release_decade,
            "mood_tags":        song.mood_tags,
            "explicit_language": song.explicit_language,
            "key":              song.key,
        }
        score, reasons = score_song(user_prefs, song_dict)
        return f"'{song.title}' scored {score}: " + ", ".join(reasons)