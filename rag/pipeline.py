from openai import OpenAI


class RAGPipeline:
    def __init__(self, retriever, reranker, client: OpenAI, system_prompt="You are a Siemens PLC expert."):
        self.retriever = retriever
        self.reranker = reranker
        self.client = client
        self.system_prompt = system_prompt

    def answer(self, query: str, top_k: int = 3):
        # 1) Retrieve
        candidates = self.retriever.retrieve(query)

        # 2) Rerank
        reranked = self.reranker.rerank(query, candidates)

        # 3) Take top_k docs
        docs = [d for d, s in reranked[:top_k]]
        context = "\n\n".join([d.page_content for d in docs])

        # 4) LLM generate
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{query}"}
            ],
            temperature=0
        )

        return response.choices[0].message.content, reranked