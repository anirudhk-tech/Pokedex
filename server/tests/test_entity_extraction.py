import json
from typing import Any, Dict

import pytest

from processing.entity_extraction import extract_entities


def test_extract_entities_parse_valid_json(monkeypatch):
    fake_payload: Dict[str, Any] = {
        "pokemon_nodes": [
            {
                "name": "Bulbasaur",
                "generation": 1,
                "primary_type": "Grass",
                "secondary_type": "Poison",
            }
        ],
        "type_nodes": [
            {"name": "Grass"},
            {"name": "Poison"},
        ],
        "pokemon_type_edges": [
            {"from_pokemon": "Bulbasaur", "to_type": "Grass"},
            {"from_pokemon": "Bulbasaur", "to_type": "Poison"},
        ],
        "evolution_edges": [
            {"from_pokemon": "Bulbasaur", "to_pokemon": "Ivysaur"},
        ],
        "mentions_edges": [
            {"from_media_id": "bulbasaur_audio", "to_pokemon": "Charmander"},
        ],
    }

    fake_json = json.dumps(fake_payload, ensure_ascii=False)

    class FakeResponse:
        def __init__(self, text: str):
            self.output_text = text

    class FakeResponses:
        def create(self, *args, **kwargs):
            return FakeResponse(fake_json)

    class FakeClient:
        def __init__(self):
            self.responses = FakeResponses()

    monkeypatch.setattr(
        "processing.entity_extraction.openai_client",
        FakeClient(),
        raising=True,
    )

    result = extract_entities(
        text="Bulbasaur is a Grass/Poison starter.",
        media_id="bulbasaur_audio",
        pokemon_hint="Bulbasaur",
    )

    assert "pokemon_nodes" in result
    assert "type_nodes" in result
    assert "pokemon_type_edges" in result
    assert "evolution_edges" in result
    assert "mentions_edges" in result

    assert len(result["pokemon_nodes"]) == 1
    node = result["pokemon_nodes"][0]
    assert node["name"] == "Bulbasaur"
    assert node["generation"] == 1
    assert node["primary_type"] == "Grass"
    assert node["secondary_type"] == "Poison"

    assert {"name": "Grass"} in result["type_nodes"]
    assert {"name": "Poison"} in result["type_nodes"]

    assert {
        "from_pokemon": "Bulbasaur",
        "to_type": "Grass",
    } in result["pokemon_type_edges"]
    assert {
        "from_pokemon": "Bulbasaur",
        "to_type": "Poison",
    } in result["pokemon_type_edges"]

    assert {
        "from_pokemon": "Bulbasaur",
        "to_pokemon": "Ivysaur",
    } in result["evolution_edges"]

    assert {
        "from_media_id": "bulbasaur_audio",
        "to_pokemon": "Charmander",
    } in result["mentions_edges"]
