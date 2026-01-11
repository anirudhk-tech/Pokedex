# 🤝 Contributing to PokéRAG

First off, thank you for considering contributing to PokéRAG! It's trainers like you that make this Pokédex truly legendary. ⚡

> "I see now that the circumstances of one's birth are irrelevant; it is what you do with the gift of life that determines who you are." — Mewtwo

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [Testing](#testing)

---

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the maintainers.

---

## How Can I Contribute?

### 🐛 Reporting Bugs

Found a bug? Help us squash it! Before creating a bug report, please check existing issues to avoid duplicates.

**Great bug reports include:**

- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Screenshots or logs if applicable
- Your environment (OS, Python version, etc.)

```markdown
## Bug Report

### Description
When querying about Pikachu, the system returns Raichu information.

### Steps to Reproduce
1. Start the server
2. Send POST to /chat with message "What types is Pikachu?"
3. Observe response

### Expected Behavior
Should return Electric type for Pikachu

### Actual Behavior
Returns Electric type but mentions Raichu evolution

### Environment
- OS: macOS 14.0
- Python: 3.11
- Node.js: 20.10
```

### ✨ Suggesting Features

Have an idea to make PokéRAG better? We'd love to hear it!

**Feature requests should include:**

- A clear description of the feature
- The problem it solves
- Any alternatives you've considered

### 🔧 Code Contributions

Ready to write some code? Here's how:

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create a branch** for your feature/fix
4. **Make changes** with tests
5. **Submit** a pull request

#### Good First Issues

Look for issues labeled:
- `good first issue` - Great for newcomers
- `help wanted` - We need your help!
- `documentation` - Improve our docs

---

## Development Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- pnpm (recommended) or npm
- Git

### Backend Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/pokerag.git
cd pokerag

# Create virtual environment
cd server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-cov black isort mypy

# Copy environment file
cp .env.example .env
# Edit .env with your API keys
```

### Frontend Setup

```bash
cd client
pnpm install
```

### Running Tests

```bash
# Backend tests
cd server
pytest -v

# With coverage
pytest --cov=. --cov-report=html
```

### Running Locally

```bash
# Terminal 1: Backend
cd server
uvicorn api.main:app --reload

# Terminal 2: Frontend
cd client
pnpm dev
```

---

## Pull Request Process

### Before Submitting

1. **Update tests**: Add tests for new functionality
2. **Run tests**: Ensure all tests pass
3. **Format code**: Run formatters (see Style Guidelines)
4. **Update docs**: If needed, update README or docs/

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 📚 Documentation
- [ ] 🔧 Refactoring
- [ ] 🧪 Tests

## Related Issues
Fixes #123

## Testing
Describe how you tested your changes

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have added tests that prove my fix/feature works
- [ ] All new and existing tests pass
- [ ] I have updated documentation if needed
```

### Review Process

1. A maintainer will review your PR
2. They may request changes or ask questions
3. Once approved, your PR will be merged
4. Celebrate! 🎉 You're now a PokéRAG contributor!

---

## Style Guidelines

### Python (Backend)

We use [Black](https://black.readthedocs.io/) and [isort](https://pycqa.github.io/isort/) for formatting:

```bash
# Format code
black .
isort .

# Check without changing
black --check .
isort --check .
```

**Key conventions:**

```python
# Use type hints
def get_pokemon(name: str) -> dict:
    ...

# Docstrings for public functions
def ingest_pdf(path: str) -> dict:
    """
    Ingest a PDF file and return a structured record.
    
    Args:
        path: Path to the PDF file
        
    Returns:
        Dict with id, modality, text, and metadata
    """
    ...

# Use Pydantic for data models
class PokemonNode(BaseModel):
    name: str
    generation: int
    primary_type: str | None = None
```

### TypeScript (Frontend)

We use ESLint and Prettier:

```bash
cd client
pnpm lint
```

**Key conventions:**

```typescript
// Use TypeScript types
type PokemonNode = {
  name: string;
  generation: number;
  primary_type?: string | null;
};

// Functional components with hooks
export const GraphView = ({ focusedPokemon }: Props) => {
  const [nodes, setNodes] = useState<Node[]>([]);
  ...
};

// Use descriptive variable names
const pokemonTypeEdges = graph.pokemon_type_edges;

// Handle errors gracefully
try {
  const res = await fetch(`${API_BASE}/graph`);
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
} catch (err) {
  console.error(err);
}
```

### CSS (Tailwind)

```tsx
// Use Tailwind utilities
<div className="flex items-center justify-between px-6 py-4">

// Use cn() for conditional classes
<div className={cn(
  "rounded-lg p-4",
  isActive && "bg-emerald-500",
  isDisabled && "opacity-50"
)}>

// Prefer semantic color names over raw values
className="text-slate-100 bg-slate-950"
```

---

## Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change that neither fixes nor adds |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks |

### Examples

```bash
# Feature
feat(ingestion): add support for JPEG images

# Bug fix
fix(chat): handle empty query gracefully

# Documentation
docs(readme): add deployment instructions

# Refactoring
refactor(graph): extract node creation into helper
```

### Pokémon-Themed Commits (Optional but Fun!)

```bash
feat(api): ⚡ add Pikachu-fast caching layer
fix(graph): 🔥 resolve Charmander type conflict
docs: 🌿 plant new getting started guide
test: 💧 add Squirtle edge case coverage
```

---

## Testing

### Writing Tests

```python
# server/tests/test_example.py

import pytest
from ingestion.text_ingestion import ingest_pdf

def test_ingest_pdf_returns_expected_schema():
    """PDF ingestion returns a well-formed record."""
    record = ingest_pdf("data/raw/text/Bulbasaur.pdf")
    
    assert "id" in record
    assert record["modality"] == "text"
    assert "Bulbasaur" in record["text"]

def test_ingest_pdf_with_missing_file():
    """PDF ingestion handles missing files gracefully."""
    with pytest.raises(FileNotFoundError):
        ingest_pdf("nonexistent.pdf")
```

### Test Organization

```
tests/
├── test_api.py              # API endpoint tests
├── test_text_ingestion.py   # Text processing
├── test_image_ingestion.py  # Image OCR
├── test_audio_ingestion.py  # Audio transcription
├── test_entity_extraction.py # LLM NER
├── test_build_graph.py      # Graph construction
└── test_deepeval.py         # RAG quality
```

### Running Specific Tests

```bash
# Single file
pytest tests/test_api.py -v

# Single test
pytest tests/test_api.py::test_health -v

# Tests matching pattern
pytest -k "bulbasaur" -v

# With coverage for specific module
pytest --cov=ingestion tests/test_text_ingestion.py
```

---

## Questions?

- 📖 Check the [documentation](docs/)
- 💬 Open a [Discussion](https://github.com/yourusername/pokerag/discussions)
- 🐛 File an [Issue](https://github.com/yourusername/pokerag/issues)

---

<p align="center">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/143.png" width="80" alt="Snorlax">
</p>

<p align="center">
  <em>"Every contribution counts, no matter how small. Even Snorlax started somewhere!"</em>
</p>

<p align="center">
  <strong>Happy Contributing! 🎮</strong>
</p>
