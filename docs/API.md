# 📚 Pokédex API Reference

> Complete API documentation for the Pokédex backend

## Base URL

```
Development: http://localhost:8000
Production:  https://your-api-domain.com
```

---

## Authentication

Currently, the API does not require authentication. For production deployments, consider adding:
- API key authentication
- OAuth 2.0
- JWT tokens

---

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/chat` | RAG-powered chat |
| `GET` | `/graph` | Knowledge graph data |
| `GET` | `/logs` | Evaluation logs |
| `POST` | `/ingest` | Trigger full ingestion |
| `POST` | `/process` | Rebuild knowledge graph |
| `POST` | `/add/text` | Upload text file |
| `POST` | `/add/image` | Upload image file |
| `POST` | `/add/audio` | Upload audio file |

---

## Health Check

Check if the API is running.

### Request

```http
GET /health
```

### Response

```json
{
  "status": "ok"
}
```

### Status Codes

| Code | Description |
|------|-------------|
| `200` | Server is healthy |
| `500` | Server error |

---

## Chat (RAG Query)

Query the multimodal RAG system with natural language.

### Request

```http
POST /chat
Content-Type: multipart/form-data
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `message` | `string` | Yes | The question to ask |

### Example Request

```bash
curl -X POST http://localhost:8000/chat \
  -F "message=What types is Bulbasaur?"
```

### Response

```json
{
  "content": "Bulbasaur is a dual-type Grass/Poison Pokémon introduced in Generation I. It is one of the three starter Pokémon available in the Kanto region.",
  "node": {
    "name": "Bulbasaur",
    "generation": 1,
    "primary_type": "Grass",
    "secondary_type": "Poison"
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `content` | `string` | The AI-generated response |
| `node` | `object \| null` | The focused Pokémon node (if resolved) |
| `node.name` | `string` | Pokémon name |
| `node.generation` | `integer` | Generation number |
| `node.primary_type` | `string \| null` | Primary type |
| `node.secondary_type` | `string \| null` | Secondary type |

### Status Codes

| Code | Description |
|------|-------------|
| `200` | Successful response |
| `400` | Invalid request (missing message) |
| `500` | Server error |

### Example Queries

```bash
# Factual lookup
curl -X POST http://localhost:8000/chat \
  -F "message=What types is Charmander?"

# Evolution chain
curl -X POST http://localhost:8000/chat \
  -F "message=What does Squirtle evolve into?"

# Comparison
curl -X POST http://localhost:8000/chat \
  -F "message=Compare the three Gen 1 starter Pokémon"

# Multi-hop
curl -X POST http://localhost:8000/chat \
  -F "message=Which starter Pokémon is weak against Bulbasaur?"
```

---

## Knowledge Graph

Retrieve the complete knowledge graph as JSON.

### Request

```http
GET /graph
```

### Response

```json
{
  "pokemon_nodes": [
    {
      "name": "Bulbasaur",
      "generation": 1,
      "primary_type": "Grass",
      "secondary_type": "Poison"
    },
    {
      "name": "Ivysaur",
      "generation": 1,
      "primary_type": "Grass",
      "secondary_type": "Poison"
    }
  ],
  "type_nodes": [
    {"name": "Grass"},
    {"name": "Poison"},
    {"name": "Fire"},
    {"name": "Water"}
  ],
  "pokemon_type_edges": [
    {"from_pokemon": "Bulbasaur", "to_type": "Grass"},
    {"from_pokemon": "Bulbasaur", "to_type": "Poison"}
  ],
  "evolution_edges": [
    {"from_pokemon": "Bulbasaur", "to_pokemon": "Ivysaur"},
    {"from_pokemon": "Ivysaur", "to_pokemon": "Venusaur"}
  ],
  "mentions_edges": [
    {"from_media_id": "bulbasaur_bulbapedia_pdf", "to_pokemon": "Bulbasaur"}
  ]
}
```

### Response Schema

#### PokemonNode

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | Pokémon name |
| `generation` | `integer` | Generation (1-9) |
| `primary_type` | `string \| null` | Primary type |
| `secondary_type` | `string \| null` | Secondary type |

#### TypeNode

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | Type name (e.g., "Fire", "Water") |

#### PokemonTypeEdge

| Field | Type | Description |
|-------|------|-------------|
| `from_pokemon` | `string` | Pokémon name |
| `to_type` | `string` | Type name |

#### EvolutionEdge

| Field | Type | Description |
|-------|------|-------------|
| `from_pokemon` | `string` | Pre-evolution name |
| `to_pokemon` | `string` | Evolution name |

#### MentionsEdge

| Field | Type | Description |
|-------|------|-------------|
| `from_media_id` | `string` | Media record ID |
| `to_pokemon` | `string` | Pokémon mentioned |

### Status Codes

| Code | Description |
|------|-------------|
| `200` | Graph returned successfully |
| `404` | Graph not built yet |
| `500` | Server error |

---

## Evaluation Logs

Retrieve evaluation logs for all queries.

### Request

```http
GET /logs
```

### Response

```json
[
  {
    "timestamp": "2025-01-11T10:30:00.000Z",
    "query": "What types is Bulbasaur?",
    "answer": "Bulbasaur is a dual-type Grass/Poison Pokémon...",
    "retrieved_context": {
      "graph_context": "...",
      "vector_results": [...]
    },
    "evaluation": {
      "grounded_in_graph": true,
      "latency_ms": 1234
    },
    "focused_pokemon": {
      "name": "Bulbasaur",
      "generation": 1,
      "primary_type": "Grass",
      "secondary_type": "Poison"
    }
  }
]
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `string` | ISO 8601 timestamp |
| `query` | `string` | User's question |
| `answer` | `string` | AI response |
| `retrieved_context` | `object` | Context used for generation |
| `evaluation` | `object` | Evaluation metrics |
| `focused_pokemon` | `object \| null` | Resolved Pokémon node |

### Status Codes

| Code | Description |
|------|-------------|
| `200` | Logs returned successfully |
| `404` | No logs found |
| `500` | Server error |

---

## Trigger Ingestion

Manually trigger the full ingestion pipeline.

### Request

```http
POST /ingest
```

### Response

```json
{
  "message": "Ingestion process completed"
}
```

### What It Does

1. Scans `data/raw/text/` for PDF and TXT files
2. Scans `data/raw/images/` for image files
3. Scans `data/raw/audio/` for audio files
4. Processes each file through modality-specific pipelines
5. Writes records to JSONL files in `data/processed/`
6. Computes embeddings and upserts to Qdrant

### Status Codes

| Code | Description |
|------|-------------|
| `200` | Ingestion completed |
| `500` | Ingestion failed |

---

## Rebuild Graph

Rebuild the knowledge graph from processed data.

### Request

```http
POST /process
```

### Response

```json
{
  "message": "Graph built successfully"
}
```

### What It Does

1. Reads JSONL files from `data/processed/`
2. Extracts entities and relationships using LLM
3. Builds knowledge graph structure
4. Exports `graph.json` for the API
5. Exports CSVs for Neo4j import (optional)

### Status Codes

| Code | Description |
|------|-------------|
| `200` | Graph built successfully |
| `500` | Graph building failed |

---

## Upload Text File

Upload a PDF or TXT file for ingestion.

### Request

```http
POST /add/text
Content-Type: multipart/form-data
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `file` | `file` | Yes | PDF or TXT file |

### Example

```bash
curl -X POST http://localhost:8000/add/text \
  -F "file=@pokemon_guide.pdf"
```

### Response

```json
{
  "message": "File ingested successfully",
  "record": {
    "id": "pokemon_guide_pdf",
    "modality": "text",
    "pokemon": "Unknown",
    "text": "..."
  }
}
```

### Supported Formats

- `.pdf` - PDF documents
- `.txt` - Plain text files

### Status Codes

| Code | Description |
|------|-------------|
| `200` | File ingested |
| `400` | Unsupported file type |
| `500` | Ingestion failed |

---

## Upload Image File

Upload an image file for OCR extraction.

### Request

```http
POST /add/image
Content-Type: multipart/form-data
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `file` | `file` | Yes | Image file |

### Example

```bash
curl -X POST http://localhost:8000/add/image \
  -F "file=@pikachu_card.jpg"
```

### Response

```json
{
  "message": "File ingested successfully",
  "record": {
    "id": "pikachu_card_jpg",
    "modality": "image",
    "pokemon": "Pikachu",
    "text": "Pikachu 60 HP Electric..."
  }
}
```

### Supported Formats

- `.png` - PNG images
- `.jpg`, `.jpeg` - JPEG images

### Status Codes

| Code | Description |
|------|-------------|
| `200` | File ingested |
| `400` | Unsupported file type |
| `500` | OCR/ingestion failed |

---

## Upload Audio File

Upload an audio file for transcription.

### Request

```http
POST /add/audio
Content-Type: multipart/form-data
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `file` | `file` | Yes | Audio file |

### Example

```bash
curl -X POST http://localhost:8000/add/audio \
  -F "file=@pokemon_facts.mp3"
```

### Response

```json
{
  "message": "File ingested successfully",
  "record": {
    "id": "pokemon_facts_mp3",
    "modality": "audio",
    "pokemon": "Multiple",
    "text": "Did you know that Bulbasaur..."
  }
}
```

### Supported Formats

- `.mp3` - MP3 audio files

### Status Codes

| Code | Description |
|------|-------------|
| `200` | File ingested |
| `400` | Unsupported file type |
| `500` | Transcription/ingestion failed |

---

## Error Responses

All endpoints return errors in a consistent format:

```json
{
  "detail": "Error description here"
}
```

### Common Error Codes

| Code | Description |
|------|-------------|
| `400` | Bad Request - Invalid input |
| `404` | Not Found - Resource doesn't exist |
| `422` | Unprocessable Entity - Validation error |
| `500` | Internal Server Error |

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider:

```python
# Example with slowapi
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/chat")
@limiter.limit("10/minute")
async def chat(...):
    ...
```

---

## CORS Configuration

The API allows requests from:

```python
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

For production, update `api/main.py` with your frontend domain.

---

## OpenAPI Documentation

FastAPI automatically generates OpenAPI documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

---

<p align="center">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/132.png" width="60" alt="Ditto">
</p>

<p align="center">
  <em>"This API transforms to match your needs, just like Ditto!"</em>
</p>
