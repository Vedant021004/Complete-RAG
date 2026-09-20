"""
Hybrid Search Retriever for Production RAG Pipelines

Combines dense vector retrieval (semantic embeddings) with sparse keyword retrieval
(BM25 / lexical scoring) using Reciprocal Rank Fusion (RRF) for optimal context retrieval.
"""

from typing import List, Dict, Any


def reciprocal_rank_fusion(
    dense_results: List[Dict[str, Any]],
    sparse_results: List[Dict[str, Any]],
    k: int = 60,
) -> List[Dict[str, Any]]:
    """
    Applies Reciprocal Rank Fusion to merge ranked lists from dense and sparse retrievers.

    Args:
        dense_results: Ranked list of documents from dense embedding search.
        sparse_results: Ranked list of documents from sparse BM25 keyword search.
        k: Smoothing constant (default: 60).

    Returns:
        Fused and re-ranked list of unique documents with combined RRF scores.
    """
    scores: Dict[str, float] = {}
    doc_map: Dict[str, Dict[str, Any]] = {}

    for rank, doc in enumerate(dense_results, start=1):
        doc_id = doc["id"]
        doc_map[doc_id] = doc
        scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (k + rank))

    for rank, doc in enumerate(sparse_results, start=1):
        doc_id = doc["id"]
        doc_map[doc_id] = doc
        scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (k + rank))

    # Sort documents by accumulated RRF score descending
    sorted_doc_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

    ranked_results = []
    for doc_id in sorted_doc_ids:
        entry = dict(doc_map[doc_id])
        entry["rrf_score"] = round(scores[doc_id], 6)
        ranked_results.append(entry)

    return ranked_results


if __name__ == "__main__":
    sample_dense = [
        {"id": "doc_1", "text": "LangGraph multi-agent orchestration architecture", "dense_rank": 1},
        {"id": "doc_2", "text": "Vector database indexing with Chroma and HNSW", "dense_rank": 2},
    ]

    sample_sparse = [
        {"id": "doc_2", "text": "Vector database indexing with Chroma and HNSW", "bm25_rank": 1},
        {"id": "doc_3", "text": "BM25 inverted index keyword search implementation", "bm25_rank": 2},
    ]

    fused = reciprocal_rank_fusion(sample_dense, sample_sparse)
    print("Hybrid Search RRF Results:")
    for item in fused:
        print(f"  - [{item['id']}] (score: {item['rrf_score']}): {item['text']}")
