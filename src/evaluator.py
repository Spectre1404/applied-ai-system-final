"""
Evaluation helpers for recommendation outputs and end-to-end checks.
"""

from typing import Dict, List


def precision_at_k(recommended: List[int], relevant: List[int], k: int = 5) -> float:
    """Compute precision@k for ranked recommendation ids."""
    if k <= 0:
        return 0.0

    top_k = recommended[:k]
    if not top_k:
        return 0.0

    relevant_set = set(relevant)
    hits = sum(1 for item_id in top_k if item_id in relevant_set)
    return hits / len(top_k)


def evaluate_profile(
    recommended: List[int],
    relevant: List[int],
    k_values: List[int] = None,
) -> Dict[str, float]:
    """Return precision metrics across multiple cutoff values."""
    if k_values is None:
        k_values = [1, 3, 5]

    metrics: Dict[str, float] = {}
    for k in k_values:
        metrics[f"precision@{k}"] = round(precision_at_k(recommended, relevant, k), 4)
    return metrics


def evaluate_system(songs: List[Dict]) -> Dict:
    from src.rag import recommend_from_query

    test_cases = [
        ("Recommend calm songs for studying", True),
        ("Give me upbeat pop songs for a workout", True),
        ("songs like coldplay", True),
        ("", False),
        ("asdfghjkl", False),
        ("romantic lofi for late night coding", True),
    ]

    results = []
    passed = 0
    total = len(test_cases)
    for query, should_succeed in test_cases:
        out = recommend_from_query(query, songs, k=3)
        ok = out["status"] == "ok"
        if should_succeed:
            test_passed = ok and len(out["recommendations"]) > 0
        else:
            test_passed = out["status"] == "fallback"
        if test_passed:
            passed += 1
        results.append(
            {
                "query": query,
                "status": out["status"],
                "passed": test_passed,
                "confidence": out.get("confidence", 0.0),
            }
        )

    avg_conf = round(sum(r["confidence"] for r in results) / total if total else 0.0, 2)
    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": round(passed / total, 2) if total else 0.0,
        "avg_confidence": avg_conf,
        "details": results,
    }


def print_evaluation_report(songs: List[Dict]) -> None:
    report = evaluate_system(songs)
    print("\nEVALUATION REPORT")
    print("=" * 60)
    print(f"Passed: {report['passed']}/{report['total']}")
    print(f"Pass rate: {report['pass_rate']}")
    print(f"Average confidence: {report['avg_confidence']}")
    print("\nDetails:")
    for row in report["details"]:
        print(
            f"- {row['query']!r}: {row['status']} | "
            f"passed={row['passed']} | confidence={row['confidence']}"
        )
