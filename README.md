# Enterprise Knowledge Retrieval System

An enterprise-oriented RAG framework for document ingestion, hybrid retrieval, reranking, and AI-powered question answering.

## Overview

Enterprise Knowledge Retrieval System is an applied AI engineering prototype designed to transform internal documents into a searchable and answerable knowledge base.

The system combines document parsing, text chunking, embedding-based semantic search, lexical retrieval, cross-encoder reranking, and LLM-based answer generation. It is designed as a modular foundation for enterprise knowledge management, technical documentation search, and AI-assisted decision support.

## Key Features

- PDF document ingestion and text extraction
- Chapter-aware document parsing
- Recursive text chunking for long documents
- Embedding-based semantic retrieval
- FAISS vector database integration
- Hybrid retrieval combining semantic and lexical search
- Cross-encoder reranking for improved retrieval quality
- LLM-based answer generation
- Evaluation logic for retrieval performance
- Modular project structure for future extension

## Tech Stack

- Python
- LangChain
- FAISS
- HuggingFace embeddings
- Cross-Encoder reranking
- OpenAI API
- Scikit-learn
- PDF processing
- Retrieval-Augmented Generation

## Project Structure

```text
enterprise-rag-framework/
├── main.py
├── requirements.txt
├── rag/
│   ├── pipeline.py
│   ├── retriever.py
│   └── reranker.py
├── evaluation/
│   ├── ground_truth.py
│   └── metrics.py
├── utils/
│   └── config.py
└── README.md