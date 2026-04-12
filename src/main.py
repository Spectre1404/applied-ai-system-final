"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os
from src.recommender import load_songs, recommend_songs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print top-k recommendations for a given user profile."""
    print(f"\n{'=' * 55}")
    print(f"Profile: {profile_name}")
    print(f"Prefs: genre={user_prefs.get('genre')}, mood={user_prefs.get('mood')}, energy={user_prefs.get('energy')}")
    print(f"{'=' * 55}")

    recommendations = recommend_songs(user_prefs, songs, k=k)
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"{i}. {song['title']} — Score: {score:.2f}")
        print(f"   Because: {explanation}")
    print()


def main() -> None:
    songs = load_songs(os.path.join(BASE_DIR, "data", "songs.csv"))

    profiles = [
        (
            "High-Energy Pop",
            {"genre": "pop", "mood": "happy", "energy": 0.9, "valence": 0.8, "likes_acoustic": False},
        ),
        (
            "Chill Lofi",
            {"genre": "lofi", "mood": "calm", "energy": 0.3, "valence": 0.5, "likes_acoustic": True},
        ),
        (
            "Deep Intense Rock",
            {"genre": "rock", "mood": "angry", "energy": 0.95, "valence": 0.2, "likes_acoustic": False},
        ),
        (
            "Conflicting: High Energy + Sad Mood",
            {"genre": "pop", "mood": "sad", "energy": 0.9, "valence": 0.1, "likes_acoustic": False},
        ),
        (
            "Unknown Genre",
            {"genre": "bossa nova", "mood": "romantic", "energy": 0.5, "valence": 0.6, "likes_acoustic": True},
        ),
    ]

    for name, prefs in profiles:
        print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()