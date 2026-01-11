# 📖 Pokédex Documentation

> Your comprehensive guide to the Pokédex multimodal RAG system

---

## 📚 Documentation Index

| Document | Description |
|----------|-------------|
| [Quick Start](QUICKSTART.md) | Get running in 5 minutes |
| [API Reference](API.md) | Complete API documentation |
| [Architecture](ARCHITECTURE.md) | System design deep-dive |

---

## 🗂️ Other Documentation

| Document | Location | Description |
|----------|----------|-------------|
| [Main README](../README.md) | Root | Project overview |
| [Server README](../server/README.md) | `/server` | Backend documentation |
| [Client README](../client/README.md) | `/client` | Frontend documentation |
| [Contributing](../CONTRIBUTING.md) | Root | How to contribute |
| [Code of Conduct](../CODE_OF_CONDUCT.md) | Root | Community guidelines |
| [Security](../SECURITY.md) | Root | Security policy |
| [Changelog](../CHANGELOG.md) | Root | Version history |

---

## 🗺️ Reading Order

### For New Users
1. Start with [Quick Start](QUICKSTART.md) to get running
2. Try some queries in the UI
3. Read the [API Reference](API.md) to understand endpoints

### For Developers
1. Review the [Architecture](ARCHITECTURE.md) first
2. Check [Contributing](../CONTRIBUTING.md) for guidelines
3. Explore the [Server README](../server/README.md) for backend details
4. See [Client README](../client/README.md) for frontend details

### For Operators
1. Read [Quick Start](QUICKSTART.md) for setup
2. Review [Security](../SECURITY.md) for best practices
3. Check [Architecture](ARCHITECTURE.md) for scaling considerations

---

## 🔍 Quick Links

### API Endpoints
- `GET /health` - Health check
- `POST /chat` - RAG queries
- `GET /graph` - Knowledge graph
- `GET /logs` - Evaluation logs
- `POST /add/*` - File uploads

### Key Components
- **Ingestion**: `server/ingestion/`
- **Processing**: `server/processing/`
- **API Routes**: `server/api/routes/`
- **Frontend**: `client/app/`

### Configuration
- Backend: `server/.env`
- Frontend: `client/.env.local`

---

## 🆘 Need Help?

- 📖 Check this documentation first
- 🔍 Search existing [GitHub Issues](https://github.com/yourusername/pokerag/issues)
- 💬 Start a [Discussion](https://github.com/yourusername/pokerag/discussions)
- 🐛 Report bugs via [Issues](https://github.com/yourusername/pokerag/issues/new)

---

<p align="center">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/137.png" width="60" alt="Porygon">
</p>

<p align="center">
  <em>"Like Porygon navigating cyberspace, this documentation guides you through the system!"</em>
</p>
