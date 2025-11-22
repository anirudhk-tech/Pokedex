import json
from pathlib import Path
from typing import Any, Dict, Union

from processing import entity_extraction, graph_builder


def _write_jsonl(path: Path, records: list[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False))
            f.write("\n")


def test_build_graph_merges_fragments(tmp_path, monkeypatch):
    processed_dir = tmp_path / "data" / "processed"
    text_jsonl = processed_dir / "text.jsonl"
    images_jsonl = processed_dir / "images.jsonl"
    audio_jsonl = processed_dir / "audio.jsonl"

    text_recs = [
        {
            "id": "bulbasaur_fact",
            "modality": "text",
            "source_path": "data/raw/text/bulbasaur_fact.txt",
            "text": "Bulbasaur is a Grass/Poison starter.",
            "pokemon": "Bulbasaur",
            "generation": 1,
        },
    ]
    audio_recs = [
        {
            "id": "charmander_fact",
            "modality": "audio",
            "source_path": "data/raw/audio/charmander_fact.mp3",
            "text": "Charmander is a Fire-type starter.",
            "pokemon": "Charmander",
            "generation": 1,
        },
    ]
    image_recs = [
        {
            "id": "squirtle_card",
            "modality": "image",
            "source_path": "data/raw/images/squirtle_card.jpg",
            "text": "Squirtle is a Water-type starter.",
            "pokemon": "Squirtle",
            "generation": 1,
        },
    ]

    _write_jsonl(text_jsonl, text_recs)
    _write_jsonl(audio_jsonl, audio_recs)
    _write_jsonl(images_jsonl, image_recs)

    monkeypatch.setattr(graph_builder, "TEXT_JSONL", text_jsonl, raising=True)
    monkeypatch.setattr(graph_builder, "AUDIO_JSONL", audio_jsonl, raising=True)
    monkeypatch.setattr(graph_builder, "IMAGES_JSONL", images_jsonl, raising=True)

    def fake_extract_entities(
        text: str, media_id: str, pokemon_hint: Union[str, None] = None
    ):
        pokemon = pokemon_hint or "Unknown"
        return {
            "pokemon_nodes": [
                {
                    "name": pokemon,
                    "generation": 1,
                    "primary_type": None,
                    "secondary_type": None,
                }
            ],
            "type_nodes": [],
            "pokemon_type_edges": [],
            "evolution_edges": [],
            "mentions_edges": [
                {"from_media_id": media_id, "to_pokemon": pokemon},
            ],
        }

    monkeypatch.setattr(
        entity_extraction,
        "extract_entities",
        fake_extract_entities,
        raising=True,
    )

    graph = graph_builder.build_graph()

    names = {n["name"] for n in graph["pokemon_nodes"]}
    assert names == {"Bulbasaur", "Charmander", "Squirtle"}

    assert len(graph["mentions_edges"]) == 3
    assert {
        "from_media_id": "bulbasaur_fact",
        "to_pokemon": "Bulbasaur",
    } in graph["mentions_edges"]
    assert {
        "from_media_id": "charmander_fact",
        "to_pokemon": "Charmander",
    } in graph["mentions_edges"]
    assert {
        "from_media_id": "squirtle_card",
        "to_pokemon": "Squirtle",
    } in graph["mentions_edges"]
