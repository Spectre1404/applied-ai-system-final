"""
Minimal RAG (Retrieval-Augmented Generation) helpers.
"""

from typing import Dict, List


def tokenize(text: str) -> List[str]:
    """Lowercase whitespace tokenizer."""
    return [token for token in text.lower().split() if token]


def retrieve(query: str, documents: List[Dict], top_k: int = 3) -> List[Dict]:
    """
    Retrieve top-k documents by token overlap with the query.

    Each document is expected to include a "text" field.
    """
    query_tokens = set(tokenize(query))
    scored_docs = []

    for doc in documents:
        doc_text = str(doc.get("text", ""))
        doc_tokens = set(tokenize(doc_text))
        overlap = len(query_tokens.intersection(doc_tokens))
        scored_docs.append((overlap, doc))

    scored_docs.sort(key=lambda item: item[0], reverse=True)
    return [doc for score, doc in scored_docs[:top_k] if score > 0]
