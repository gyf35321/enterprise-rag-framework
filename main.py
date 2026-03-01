import time
from evaluation.metrics import top1_hit, recall_at_k
from evaluation.ground_truth import GROUND_TRUTH
from rag.reranker import CrossEncoderReranker
from rag.retriever import HybridRetriever
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import os

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

import re
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

loader = PyPDFLoader("data/S7-1200 Programmable controller – Support – Siemens.pdf")
documents = loader.load()

chapter_pattern = re.compile(r"\b\d+\.\d+\s+[A-Z][^\n]+")

structured_docs = []
current_chapter = "Unknown"

for i, doc in enumerate(documents):
    text = doc.page_content
    
    match = chapter_pattern.search(text)
    if match:
        current_chapter = match.group().strip()
    
    structured_docs.append(
        Document(
            page_content=text,
            metadata={
                "page": i + 1,
                "chapter": current_chapter
            }
        )
    )

print(f"Total pages: {len(structured_docs)}")

# 二次切块
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(structured_docs)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.from_documents(chunks, embeddings)
hybrid_retriever = HybridRetriever(vectorstore, chunks)
reranker = CrossEncoderReranker()

print("Vector store created successfully.")


print(f"Final chunks: {len(chunks)}")

# 查看示例
print("\nSample metadata example:")
print(chunks[200].metadata)


evaluation_queries = [
    "How do I configure PROFINET communication?"
]
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

total_top1 = 0
total_recall5 = 0
num_queries = len(evaluation_queries)
for query in evaluation_queries:

    print("\n==============================")
    print(f"QUERY: {query}")
    print("==============================")
    candidates = hybrid_retriever.retrieve(query)

    # Rerank
    reranked = reranker.rerank(query, candidates)
    gt_pages = GROUND_TRUTH.get(query, set())

    top1 = top1_hit(reranked, gt_pages)
    recall5 = recall_at_k(reranked, gt_pages, k=5)

    total_top1 += top1
    total_recall5 += recall5

    print("\n=== RERANK SCORES ===")
    for i, (doc, score) in enumerate(reranked[:5]):
        print(f"\nRank {i+1} | Score: {score:.4f}")
        print(doc.metadata)
        

    # 取前三个
    docs = [d for d, s in reranked[:3]]

    context = "\n\n".join([d.page_content for d in docs])
    start_time = time.time()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a Siemens PLC expert."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{query}"}
        ],
        temperature=0
    )

    print("\n=== GPT ANSWER ===\n")
    print(response.choices[0].message.content)
    end_time = time.time()
    latency = end_time - start_time
    print(f"\nLatency: {latency:.2f} seconds")

    usage = response.usage
    print(f"Prompt Tokens: {usage.prompt_tokens}")
    print(f"Completion Tokens: {usage.completion_tokens}")
    print(f"Total Tokens: {usage.total_tokens}")
print("\n==============================")
print("OVERALL METRICS")
print("==============================")

print(f"Top1 Accuracy: {total_top1 / num_queries:.2f}")
print(f"Recall@5: {total_recall5 / num_queries:.2f}")