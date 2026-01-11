# 🌊 Pokédex Client

> A modern Next.js frontend for the Pokédex multimodal RAG system

<p>
  <img src="https://img.shields.io/badge/Next.js-16-black.svg?logo=next.js&logoColor=white" alt="Next.js">
  <img src="https://img.shields.io/badge/React-19-blue.svg?logo=react&logoColor=white" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-5.0+-blue.svg?logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Tailwind-4.0-38B2AC.svg?logo=tailwind-css&logoColor=white" alt="Tailwind">
</p>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Features](#features)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Components](#components)
- [Development](#development)

---

## Overview

The Pokédex client is a Next.js 16 application that provides:

- **Chat Interface**: Natural language querying with real-time responses
- **Knowledge Graph Visualization**: Interactive graph powered by React Flow
- **File Upload**: Drag-and-drop multimodal file ingestion
- **Evaluation Logs**: Query history and performance metrics viewer

---

## Quick Start

### 1. Install Dependencies

```bash
cd client
pnpm install
# or
npm install
# or
yarn install
```

### 2. Configure Environment (Optional)

```bash
cp .env.example .env.local
# Edit .env.local if your API is not at localhost:8000
```

### 3. Start Development Server

```bash
pnpm dev
# or
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Features

### 💬 Chat Interface

Ask questions about Pokémon in natural language:

```
"What types is Bulbasaur?"
"Tell me about Charmander's evolution"
"Compare the Gen 1 starters"
```

The chat uses a hybrid RAG system combining:
- Knowledge graph context
- Vector similarity search
- LLM response generation

### 🔮 Knowledge Graph

Interactive visualization of the Pokémon knowledge graph:

- **Pokémon Nodes**: Green-bordered circles
- **Type Nodes**: Dashed gray circles
- **Evolution Edges**: Animated green connections
- **Type Edges**: Blue connections

Pan, zoom, and explore relationships visually.

### 📤 File Upload

Upload new content to expand the knowledge base:

| Format | Description |
|--------|-------------|
| `.pdf` | Text documents |
| `.txt` | Plain text files |
| `.png`, `.jpg` | Images (OCR extracted) |
| `.mp3` | Audio files (transcribed) |

Files are automatically ingested and the graph is rebuilt.

### 📊 Evaluation Logs

View query history with:

- Timestamp
- User query
- AI response
- Focused Pokémon
- Retrieved context
- Evaluation metrics

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_BASE` | `http://localhost:8000` | Backend API URL |

### Example `.env.local`

```bash
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

> **Note**: For production, update this to your deployed API URL.

---

## Project Structure

```
client/
├── app/                          # Next.js App Router
│   ├── page.tsx                  # Main page (chat + graph)
│   ├── layout.tsx                # Root layout
│   ├── globals.css               # Global styles & Tailwind
│   └── favicon.ico               # App icon
│
├── components/                   # React components
│   ├── GraphView.tsx             # Knowledge graph visualization
│   └── ui/                       # shadcn/ui components
│       ├── button.tsx            # Button component
│       ├── dialog.tsx            # Modal dialogs
│       └── textarea.tsx          # Text input
│
├── lib/                          # Utilities
│   └── utils.ts                  # cn() and helpers
│
├── public/                       # Static assets
│   └── *.svg                     # Icons
│
├── components.json               # shadcn/ui config
├── eslint.config.mjs             # ESLint configuration
├── next.config.ts                # Next.js configuration
├── postcss.config.mjs            # PostCSS configuration
├── tailwind.config.ts            # Tailwind configuration
├── tsconfig.json                 # TypeScript configuration
├── package.json                  # Dependencies
└── README.md                     # This file
```

---

## Components

### `page.tsx` - Main Page

The main application page containing:

- **Header**: Logo, Upload button, Logs button
- **Chat Section**: Message list and input form
- **Graph Section**: Knowledge graph visualization

Key state:
- `messages`: Chat history array
- `focusedNode`: Currently focused Pokémon
- `dialogOpen`: Upload dialog state
- `logsDialogOpen`: Logs viewer state

### `GraphView.tsx` - Knowledge Graph

Renders the knowledge graph using React Flow:

```tsx
<GraphView
  updateGraphVisual={boolean}  // Trigger re-fetch
  focusedPokemon={string}      // Highlight this node
/>
```

Features:
- Radial layout for Pokémon nodes
- Column layout for Type nodes
- Animated evolution edges
- Static type edges

### UI Components (shadcn/ui)

Pre-built components from [shadcn/ui](https://ui.shadcn.com/):

| Component | Usage |
|-----------|-------|
| `Button` | Actions, submit buttons |
| `Dialog` | Upload and logs modals |
| `Textarea` | Chat input |

---

## Development

### Available Scripts

```bash
# Development server with hot reload
pnpm dev

# Production build
pnpm build

# Start production server
pnpm start

# Lint code
pnpm lint
```

### Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 16.0 | React framework |
| React | 19.2 | UI library |
| TypeScript | 5.x | Type safety |
| Tailwind CSS | 4.x | Styling |
| React Flow | 12.x | Graph visualization |
| Radix UI | Latest | Accessible primitives |

### Adding New Components

Using shadcn/ui CLI:

```bash
npx shadcn-ui@latest add [component-name]
```

### Styling

The app uses Tailwind CSS with a custom theme:

- **Background**: `slate-950` (dark mode)
- **Primary**: `emerald-500` (Grass type green)
- **Accent**: `sky-500` (Water type blue)
- **Text**: `slate-100` (light on dark)

### API Integration

All API calls go through `fetch` to the backend:

```typescript
const API_BASE = "http://localhost:8000";

// Chat
const res = await fetch(`${API_BASE}/chat`, {
  method: "POST",
  body: formData,
});

// Graph
const res = await fetch(`${API_BASE}/graph`);

// Logs
const res = await fetch(`${API_BASE}/logs`);

// File upload
const res = await fetch(`${API_BASE}/add/${type}`, {
  method: "POST",
  body: formData,
});
```

---

## Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Docker

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install
COPY . .
RUN pnpm build
CMD ["pnpm", "start"]
```

### Environment Variables for Production

Set in your hosting platform:

```
NEXT_PUBLIC_API_BASE=https://your-api-domain.com
```

---

## Troubleshooting

### Common Issues

**1. CORS errors**

Ensure the backend has the correct CORS origins:
```python
# server/api/main.py
origins = [
    "http://localhost:3000",
    "https://your-frontend-domain.com",
]
```

**2. Graph not loading**

- Check backend is running at the configured API URL
- Verify `/graph` endpoint returns data
- Run `python -m scripts.process` to build the graph

**3. Chat not responding**

- Verify backend `/chat` endpoint works
- Check browser console for errors
- Ensure OPENAI_API_KEY is set in backend

---

<p align="center">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/9.png" width="80" alt="Blastoise">
</p>

<p align="center">
  <strong>Built with 🌊 by Pokédex Team</strong>
</p>
