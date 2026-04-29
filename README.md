# Enterprise Knowledge Retrieval System

An enterprise-oriented RAG framework for document ingestion, hybrid retrieval, reranking, and AI-powered question answering.

## Overview

Enterprise Knowledge Retrieval System is an applied AI engineering prototype designed to transform internal documents into a searchable and answerable knowledge base.

The system combines document parsing, text chunking, embedding-based semantic search, lexical retrieval, cross-encoder reranking, and LLM-based answer generation. It is designed as a modular foundation for enterprise knowledge management, technical documentation search, and AI-assisted decision support.

## Industrial RAG Demo: Siemens S7-1200 Public Documentation

This repository includes an industrial RAG demo based on publicly available Siemens S7-1200 technical documentation.

The demo was tested on a 1,374-page technical manual and generated 3,579 document chunks. It demonstrates the full retrieval-augmented generation pipeline, including PDF ingestion, chapter-aware chunking, FAISS vector search, BM25-based hybrid retrieval, cross-encoder reranking, and LLM-based answer generation.

The demo includes 5 domain-specific industrial automation questions covering CPU capabilities, expansion modules, installation and wiring safety, scan cycle execution, and CPU operating modes.

- Demo notes: [`demo/demo_notes.md`](demo/demo_notes.md)
- Sample questions: [`demo/sample_questions.md`](demo/sample_questions.md)
- Sample outputs: [`demo/sample_outputs.md`](demo/sample_outputs.md)

This is an independent technical evaluation based on publicly available data, not a collaboration project.

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
├── demo/
│   ├── demo_notes.md
│   ├── sample_questions.md
│   └── sample_outputs.md
├── utils/
│   └── config.py
└── README.md