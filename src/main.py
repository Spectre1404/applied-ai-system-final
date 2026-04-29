import os
from src.recommender import load_songs, recommend_songs, format_recommendations_table
from src.rag import recommend_from_query
from src.evaluator import print_evaluation_report

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def print_recommendations(profile_name: str, user_prefs: dict, songs: list, k: int = 5, mode: str = "balanced", diversity: bool = False) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=k, mode=mode, diversity=diversity)
    label = f"{profile_name} [mode={mode}{'  diversity=ON' if diversity else ''}]"
    print(format_recommendations_table(recommendations, label))

def demo_ai_system(songs: list) -> None:
    print("\n" + "=" * 80)
    print("APPLIED AI SYSTEM DEMO")
    print("=" * 80)

    sample_queries = [
        "Recommend calm songs for studying",
        "Give me upbeat pop songs for a workout",
        "romantic lofi for late night coding",
    ]

    for q in sample_queries:
        result = recommend_from_query(q, songs, k=3)
        print(f"\nQuery: {q}")
        print(f"Status: {result['status']}")
        print(f"Confidence: {result.get('confidence', 0.0)}")
        if result["status"] == "ok":
            for i, rec in enumerate(result["recommendations"], 1):
                print(f"{i}. {rec['title']} — {rec['artist']}")
                print(f"   Score: {rec['score']}")
                print(f"   Why: {rec['reasons']}")
        else:
            print(result["message"])

def main() -> None:
    songs = load_songs(os.path.join(BASE_DIR, "data", "songs.csv"))

    profiles = [
        (
            "High-Energy Pop",
            {
                "genre": "pop", "mood": "happy", "energy": 0.9, "valence": 0.8,
                "likes_acoustic": False, "preferred_decade": "2020s",
                "preferred_mood_tags": ["euphoric", "uplifting", "feel-good"],
                "min_popularity": 70,
            },
        ),
        (
            "Chill Lofi",
            {
                "genre": "lofi", "mood": "calm", "energy": 0.3, "valence": 0.5,
                "likes_acoustic": True, "preferred_decade": "2020s",
                "preferred_mood_tags": ["cozy", "focused", "nostalgic"],
                "min_popularity": 60,
            },
        ),
        (
            "Deep Intense Rock",
            {
                "genre": "rock", "mood": "angry", "energy": 0.95, "valence": 0.2,
                "likes_acoustic": False, "preferred_decade": "2010s",
                "preferred_mood_tags": ["aggressive", "powerful", "intense"],
                "min_popularity": 60,
            },
        ),
        (
            "Conflicting: High Energy + Sad Mood",
            {
                "genre": "pop", "mood": "sad", "energy": 0.9, "valence": 0.1,
                "likes_acoustic": False, "preferred_mood_tags": ["melancholic"],
                "min_popularity": 0,
            },
        ),
        (
            "Unknown Genre",
            {
                "genre": "bossa nova", "mood": "romantic", "energy": 0.5, "valence": 0.6,
                "likes_acoustic": True, "preferred_mood_tags": ["sensual", "warm"],
                "min_popularity": 0,
            },
        ),
    ]

    print("\n" + "=" * 80)
    print("CHALLENGE 2: SCORING MODE COMPARISON — High-Energy Pop")
    print("=" * 80)
    for mode in ["balanced", "genre_first", "mood_first", "energy_focused"]:
        print_recommendations("High-Energy Pop", profiles[0][1], songs, k=3, mode=mode)

    print("\n" + "=" * 80)
    print("ALL PROFILES — BALANCED MODE")
    print("=" * 80)
    for name, prefs in profiles:
        print_recommendations(name, prefs, songs, k=5)

    print("\n" + "=" * 80)
    print("CHALLENGE 3: DIVERSITY PENALTY — Chill Lofi")
    print("=" * 80)
    print_recommendations("Chill Lofi (no diversity)", profiles[1][1], songs, k=5, diversity=False)
    print_recommendations("Chill Lofi (diversity ON)", profiles[1][1], songs, k=5, diversity=True)

    demo_ai_system(songs)
    print_evaluation_report(songs)

if __name__ == "__main__":
    main()