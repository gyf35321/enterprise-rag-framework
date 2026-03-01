def top1_hit(reranked, ground_truth_pages):
    if not reranked:
        return 0

    top_doc = reranked[0][0]
    return 1 if top_doc.metadata["page"] in ground_truth_pages else 0


def recall_at_k(reranked, ground_truth_pages, k=5):
    top_k_docs = reranked[:k]
    hits = 0

    for doc, _ in top_k_docs:
        if doc.metadata["page"] in ground_truth_pages:
            hits += 1

    return hits / len(ground_truth_pages) if ground_truth_pages else 0