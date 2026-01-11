# 📜 Changelog

All notable changes to Pokédex will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### 🚀 Planned
- Video file ingestion support (MP4)
- Neo4j graph database integration
- User authentication & rate limiting
- Streaming chat responses
- Multi-language support

---

## [1.0.0] - 2025-01-11

### ✨ Added

**Core Features**
- 🧠 Hybrid RAG system combining knowledge graph and vector search
- 📄 Text ingestion (PDF, TXT) with pypdf extraction
- 🖼️ Image ingestion with Tesseract OCR
- 🎵 Audio ingestion with OpenAI Whisper transcription
- 🔗 LLM-powered entity and relationship extraction
- 📊 Knowledge graph construction and visualization

**API**
- `POST /chat` - RAG-powered natural language queries
- `GET /graph` - Knowledge graph JSON endpoint
- `GET /logs` - Evaluation logs retrieval
- `POST /ingest` - Batch ingestion trigger
- `POST /process` - Graph rebuild trigger
- `POST /add/text` - Single text file upload
- `POST /add/image` - Single image file upload
- `POST /add/audio` - Single audio file upload
- `GET /health` - Health check endpoint

**Frontend**
- 💬 Real-time chat interface with message history
- 🔮 Interactive knowledge graph visualization (React Flow)
- 📤 Drag-and-drop file upload dialog
- 📋 Evaluation logs viewer

**Infrastructure**
- FastAPI backend with CORS support
- Qdrant Cloud vector database integration
- OpenAI GPT-4 and Ada-002 embeddings
- Next.js 16 frontend with Tailwind CSS

**Quality**
- Comprehensive test suite with pytest
- DeepEval integration for RAG quality evaluation
- Structured evaluation logging per query
- Type hints throughout Python codebase

**Documentation**
- Enterprise-grade README with badges and architecture diagrams
- API reference documentation
- Architecture deep-dive documentation
- Contributing guidelines
- Code of Conduct
- Security policy

### 🏗️ Architecture

- Modular ingestion pipeline (text, image, audio)
- Separate processing pipeline (entity extraction, graph building)
- Dual storage: JSON graph + Qdrant vectors
- Evaluation-first design with logging

---

## Version History

| Version | Date | Highlights |
|---------|------|------------|
| 1.0.0 | 2025-01-11 | Initial release with full multimodal RAG |

---

## Pokémon in This Release

This release includes knowledge about:

| Pokémon | Generation | Types |
|---------|------------|-------|
| 🌿 Bulbasaur | 1 | Grass / Poison |
| 🔥 Charmander | 1 | Fire |
| 💧 Squirtle | 1 | Water |
| ⚡ Pikachu | 1 | Electric |

*More Pokémon can be added by uploading relevant documents!*

---

## Migration Guide

### From 0.x to 1.0.0

This is the initial release. No migration needed!

For future migrations, guides will be provided here.

---

## Contributors

Thanks to everyone who contributed to this release! 🎉

---

<p align="center">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/151.png" width="60" alt="Mew">
</p>

<p align="center">
  <em>"Every release is a new adventure, just like discovering Mew!"</em>
</p>
