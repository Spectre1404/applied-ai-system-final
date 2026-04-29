"""
Evaluation helpers for recommendation outputs.
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
