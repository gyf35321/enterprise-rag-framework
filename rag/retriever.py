from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever


class HybridRetriever:

    def __init__(self, vectorstore, documents, bm25_k=10, vector_k=10):
        self.bm25 = BM25Retriever.from_documents(documents)
        self.bm25.k = bm25_k

        self.vector_retriever = vectorstore.as_retriever(
            search_kwargs={"k": vector_k}
        )

        self.ensemble = EnsembleRetriever(
            retrievers=[self.bm25, self.vector_retriever],
            weights=[0.5, 0.5]
        )

    def retrieve(self, query):
        return self.ensemble.invoke(query)