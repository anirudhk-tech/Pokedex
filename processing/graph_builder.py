import json
from pathlib import Path
from typing import Any, Dict, Iterator

from processing.entity_extraction import extract_entities

TEXT_JSONL = Path("data/processed/text.jsonl")
IMAGES_JSONL = Path("data/processed/images.jsonl")
AUDIO_JSONL = Path("data/processed/audio.jsonl")


def _iter_jsonl(path: Path) -> Iterator[Dict[str, Any]]:
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj: Dict[str, Any] = json.loads(line)
            yield obj


def build_graph():
    pokemon_nodes: Dict[str, Dict[str, Any]] = {}
    type_nodes: Dict[str, Dict[str, Any]] = {}

    pokemon_type_edges: set[tuple[str, str]] = set()
    evolution_edges: set[tuple[str, str]] = set()
    mentions_edges: set[tuple[str, str]] = set()

    def merge_fragment(fragment: Dict[str, Any]):
        for p in fragment["pokemon_nodes"]:
            name = p["name"]
            pokemon_nodes[name] = p

        for t in fragment["type_nodes"]:
            type_name = t["name"]
            type_nodes[type_name] = t

        for e in fragment["pokemon_type_edges"]:
            pokemon_type_edges.add((e["from_pokemon"], e["to_type"]))

        for e in fragment["evolution_edges"]:
            evolution_edges.add((e["from_pokemon"], e["to_pokemon"]))

        for e in fragment["mentions_edges"]:
            mentions_edges.add((e["from_media_id"], e["to_pokemon"]))

    for path in [TEXT_JSONL, IMAGES_JSONL, AUDIO_JSONL]:
        for line in _iter_jsonl(path):
            fragment = extract_entities(
                text=line.get("text", ""),
                media_id=line["id"],
                pokemon_hint=line.get("pokemon"),
            )
            merge_fragment(fragment)

    return {
        "pokemon_nodes": list(pokemon_nodes.values()),
        "type_nodes": list(type_nodes.values()),
        "pokemon_type_edges": [
            {"from_pokemon": src, "to_type": dst} for (src, dst) in pokemon_type_edges
        ],
        "evolution_edges": [
            {"from_pokemon": src, "to_pokemon": dst} for (src, dst) in evolution_edges
        ],
        "mentions_edges": [
            {"from_media_id": src, "to_pokemon": dst} for (src, dst) in mentions_edges
        ],
    }
