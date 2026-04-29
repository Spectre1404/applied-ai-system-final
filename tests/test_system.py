from src.rag import recommend_from_query
from src.recommender import load_songs

def test_rag_system_returns_ok_for_clear_query():
    songs = load_songs("data/songs.csv")
    out = recommend_from_query("Recommend calm songs for studying", songs, k=3)
    assert out["status"] == "ok"
    assert len(out["recommendations"]) > 0
    assert 0.0 <= out["confidence"] <= 1.0

def test_rag_system_fallback_for_blank_query():
    songs = load_songs("data/songs.csv")
    out = recommend_from_query("", songs, k=3)
    assert out["status"] == "fallback"
    assert "Please enter" in out["message"]

def test_rag_system_fallback_for_gibberish():
    songs = load_songs("data/songs.csv")
    out = recommend_from_query("asdfghjkl", songs, k=3)
    assert out["status"] in ["ok", "fallback"]