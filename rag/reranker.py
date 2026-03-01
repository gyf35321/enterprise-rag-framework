from sentence_transformers import CrossEncoder


class CrossEncoderReranker:

    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query, documents):
        pairs = [[query, d.page_content] for d in documents]
        scores = self.model.predict(pairs)

        reranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return reranked