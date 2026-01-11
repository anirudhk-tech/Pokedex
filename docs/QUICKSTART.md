# ⚡ Quick Start Guide

> Get PokéRAG running in 5 minutes!

---

## Prerequisites Checklist

Before you begin, make sure you have:

- [ ] **Python 3.9+** installed
- [ ] **Node.js 18+** installed
- [ ] **pnpm** (or npm/yarn) installed
- [ ] **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- [ ] **Qdrant Cloud Account** ([Sign up free](https://cloud.qdrant.io))

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/pokerag.git
cd pokerag
```

---

## Step 2: Backend Setup

```bash
# Navigate to server
cd server

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Step 3: Configure Environment

Create `server/.env`:

```bash
# Copy the example
cp .env.example .env

# Edit with your keys
nano .env  # or use your favorite editor
```

Fill in your values:

```env
OPENAI_API_KEY=sk-your-key-here
QDRANT_URL=https://your-cluster.cloud.qdrant.io
QDRANT_API_KEY=your-qdrant-key
QDRANT_COLLECTION=pokemon_corpus
```

---

## Step 4: Setup Qdrant Collection

1. Go to [Qdrant Cloud Console](https://cloud.qdrant.io)
2. Create a new cluster (or use existing)
3. Create a collection:
   - **Name**: `pokemon_corpus`
   - **Vector Size**: `1536`
   - **Distance**: `Cosine`

---

## Step 5: Run Ingestion

```bash
# Still in server/ directory
# Make sure venv is activated

# Ingest the sample Pokémon data
python -m scripts.ingest

# Build the knowledge graph
python -m scripts.process
```

You should see output like:

```
📄 Processing text files...
  ✓ Bulbasaur (Pokémon) - Bulbapedia.pdf
  ✓ Charmander (Pokémon) - Bulbapedia.pdf
  ...

🖼️ Processing images...
  ✓ charmander_image.jpg
  ...

🎵 Processing audio...
  ✓ bulbasaur_debut.mp3
  ...

✅ Ingestion complete!
```

---

## Step 6: Start the Backend

```bash
# In server/ directory
uvicorn api.main:app --reload --port 8000
```

Test it:

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

---

## Step 7: Frontend Setup

Open a **new terminal**:

```bash
# From project root
cd client

# Install dependencies
pnpm install

# Start dev server
pnpm dev
```

---

## Step 8: Start Using PokéRAG! 🎉

Open your browser to **http://localhost:3000**

### Try These Queries

```
"What types is Bulbasaur?"
```

```
"Tell me about Charmander's evolution"
```

```
"Compare the Gen 1 starter Pokémon"
```

### Upload New Files

1. Click the **Upload** button
2. Select a PDF, image, or audio file
3. The system will ingest it automatically

### View the Knowledge Graph

The right panel shows the interactive graph. Try:
- Zooming in/out
- Dragging nodes
- Following evolution edges

### Check Evaluation Logs

Click **Logs** to see query history with:
- User questions
- AI responses
- Retrieved context
- Evaluation metrics

---

## Troubleshooting

### "Cannot connect to Qdrant"

- Check your `QDRANT_URL` is correct
- Verify your API key
- Ensure the cluster is running

### "OpenAI API error"

- Verify your `OPENAI_API_KEY`
- Check you have API credits
- Ensure the key has GPT-4 access

### "Tesseract not found"

```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

### "Frontend can't reach backend"

- Ensure backend is running on port 8000
- Check CORS settings in `api/main.py`
- Verify no firewall blocking

---

## Next Steps

Now that you're running, explore:

1. 📚 Read the [API Documentation](API.md)
2. 🏗️ Understand the [Architecture](ARCHITECTURE.md)
3. 🤝 Check the [Contributing Guide](../CONTRIBUTING.md)
4. 🧪 Run the test suite: `pytest`

---

## Quick Commands Reference

```bash
# Backend
cd server
source venv/bin/activate
uvicorn api.main:app --reload

# Frontend  
cd client
pnpm dev

# Tests
cd server
pytest -v

# Re-ingest data
python -m scripts.ingest
python -m scripts.process
```

---

<p align="center">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png" width="60" alt="Pikachu">
</p>

<p align="center">
  <strong>You're all set, trainer! Go catch some knowledge! ⚡</strong>
</p>
