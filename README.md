# Hybrid Multi-Modal Enterprise RAG System

## Project Goals

Before building any ingestion or pipeline logic, this project defines how solution quality will be measured and what outcomes are expected:

- **Correct Response:** A response is correct if it is factually accurate, relevant to the query, and grounded in the ingested enterprise data. Responses must reference supporting sources whenever possible.
- **Supported Query Types:** System supports factual lookups, summarization, and multi-step reasoning across ingested modalities of text, image, and audio.
- **Success Metrics:** Evaluation tracks retrieval quality, hallucination rate (frequency of unsupported/generated outputs), answer accuracy, and response latency.
- **Graceful Failure:** If confident answers cannot be generated, the system will fallback to informative error messages or request clarification, avoiding hallucinated or unsupported output.

All pipeline components will include functional unit tests, and evaluation reports will be automatically logged per query for continuous tracking.

## Project Overview

This project aims to design and implement a modular, scalable prototype of an enterprise-grade Retrieval-Augmented Generation (RAG) system. It supports ingestion of heterogeneous data sources from three modalities — text (PDF, TXT), images (JPG, PNG), and audio (MP3) — enabling a unified, multimodal knowledge base.

Core features include:

- Modular pipeline design prioritizing robustness and ease of testing
- Ingestion with modality-specific preprocessing: OCR for images, ASR transcription for audio, text extraction for documents
- Entity and relationship extraction leveraging large language models (LLMs)
- Construction of a cross-modal knowledge graph for semantic and multi-hop retrieval
- Hybrid search combining keyword matching and vector similarity search for improved retrieval relevance
- A demo user interface with file upload, natural language queries, and visualization of results including graph exploration

## Architecture Highlights

The system is architected as composed, independently testable modules:

- **Data Ingestion & Preprocessing:**  
  - Text documents parsed to clean text  
  - Images OCR-processed to extract text  
  - Audio transcribed via automatic speech recognition  

- **Query Processing & Retrieval:**  
  - Query triage and rewriting for enhanced search precision  
  - Agent-driven orchestration combining vector and keyword search  
  - Multi-modal indexing with managed vector databases  

- **Entity & Relationship Extraction:**  
  - Use of LLMs for named entity recognition and relationship identification across modalities  
  - Cross-modal entity linking to unify references (e.g., same person in text and audio)  
  - Schema inference for knowledge graph construction  

- **Knowledge Graph & Hybrid Search:**  
  - Graph database (e.g., Neo4j) storing entities and relations  
  - Hybrid search combining graph traversal and dense vector retrieval  
  - Integration with LLM for grounded response generation  

- **User Interface & Evaluation:**  
  - Intuitive UI or notebook for file upload, querying, and visualizing answers  
  - Logging of evaluation metrics per query for continuous improvement  
  - Graceful handling of ambiguous or incomplete queries with fallback responses

This design ensures an evaluation-first, extensible system tailored to enterprise needs and demonstrates cutting-edge multimodal retrieval-augmented generation technology with professional documentation and engineering best practices.

---

## Evaluation-First Pipeline Design

This project uses a minimal DeepEval-based test suite to evaluate the end-to-end RAG pipeline on three query types — lookup, summarization, and semantic linkage — with expected answers defined in `tests/test_queries.json`. The suite is run as part of the development workflow to provide objective signals on answer correctness and system regressions.

Supported query types are:
- Lookup: precise factual retrieval from ingested Pokémon starter data.
- Summarization: concise synthesis of multi-source information about a starter’s role, traits, or history.
- Semantic linkages: relational retrieval spanning connected entities, such as cross-generation comparisons or shared typings.

Evaluation goals are:
- Retrieval quality: measuring how accurately and consistently the system returns relevant context and correct answers.
- Hallucination control: reducing unsupported or fabricated information in responses, using retrieved context as the single source of truth.
- Latency: tracking end-to-end response time to ensure interactive performance under typical query loads.

DeepEval is used to score model outputs against reference answers with automated metrics, and results are tracked across runs to monitor quality over time. Functional unit tests (via `pytest`) cover ingestion, transcription, entity extraction, embedding, search, graph construction, and answer generation modules, and are executed in CI to guard against regressions.
