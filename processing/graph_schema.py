from typing import Any, Dict

JSON_GRAPH_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "pokemon_nodes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "generation": {"type": "integer"},
                    "primary_type": {"type": "string"},
                    "secondary_type": {"type": "string"},
                },
                "required": ["name", "generation", "primary_type", "secondary_type"],
                "additionalProperties": False,
            },
        },
        "type_nodes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
                "additionalProperties": False,
            },
        },
        "pokemon_type_edges": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "from_pokemon": {"type": "string"},
                    "to_type": {"type": "string"},
                },
                "required": ["from_pokemon", "to_type"],
                "additionalProperties": False,
            },
        },
        "evolution_edges": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "from_pokemon": {"type": "string"},
                    "to_pokemon": {"type": "string"},
                },
                "required": ["from_pokemon", "to_pokemon"],
                "additionalProperties": False,
            },
        },
        "mentions_edges": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "from_media_id": {"type": "string"},
                    "to_pokemon": {"type": "string"},
                },
                "required": ["from_media_id", "to_pokemon"],
                "additionalProperties": False,
            },
        },
    },
    "required": [
        "pokemon_nodes",
        "type_nodes",
        "pokemon_type_edges",
        "evolution_edges",
        "mentions_edges",
    ],
    "additionalProperties": False,
}
