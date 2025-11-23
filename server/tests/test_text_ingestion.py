import json
import unicodedata
from pathlib import Path
from typing import Any, Dict

import scripts.ingest_text_corpus as ingest_corpus
from ingestion.text_ingestion import (
    extract_text_from_pdf,
    ingest_pdf,
    ingest_txt,
    write_text_record,
)

PDF_PATH = Path(
    "data/raw/text/"
    "Bulbasaur (Pokémon) - Bulbapedia, the community-driven Pokémon encyclopedia.pdf"
)


def _normalize(text: str) -> str:
    # Normalize Unicode to avoid accent issues like Pok\u00e9mon vs Pokemon
    return unicodedata.normalize("NFKC", text)


def test_extract_text_from_pdf_bulbasaur():
    assert PDF_PATH.exists(), "Bulbasaur PDF missing under data/raw/text"

    raw_text = extract_text_from_pdf(str(PDF_PATH))
    text = _normalize(raw_text)

    assert len(text) > 5_000
    assert "Bulbasaur" in text
    assert "Grass" in text
    assert "Poison" in text


def test_ingest_pdf_returns_expected_schema():
    assert PDF_PATH.exists(), "Bulbasaur PDF missing under data/raw/text"

    record = ingest_pdf(
        str(PDF_PATH), pokemon="Bulbasaur", generation=1, types=["Grass", "Poison"]
    )

    assert record["id"] == PDF_PATH.stem
    assert record["modality"] == "text"
    assert record["source_path"].endswith(PDF_PATH.name)
    assert record["pokemon"] == "Bulbasaur"
    assert record["types"] == ["Grass", "Poison"]
    assert record["generation"] == 1
    assert "starter" in record["tags"]
    assert "bulbasaur" in record["tags"]
    assert len(record["text"]) > 0
    assert "Bulbasaur" in _normalize(record["text"])


def test_ingest_txt_with_tmp_file(tmp_path):
    txt_path = tmp_path / "charmander.txt"
    txt_path.write_text(
        "Charmander is a Fire-type starter Pokémon from Generation I.",
        encoding="utf-8",
    )

    record = ingest_txt(
        str(txt_path), pokemon="Charmander", generation=1, types=["Fire"]
    )

    assert record["id"] == "charmander"
    assert record["modality"] == "text"
    assert record["source_path"].endswith("charmander.txt")
    assert record["pokemon"] == "Charmander"
    assert record["types"] == ["Fire"]
    assert record["generation"] == 1
    assert "starter" in record["tags"]
    assert "charmander" in record["tags"]
    assert "Charmander" in record["text"]
    assert "Fire-type" in record["text"]


def test_write_textrecord_creates_valid_jsonl(tmp_path, monkeypatch):
    temp_jsonl = tmp_path / "text.jsonl"
    monkeypatch.setattr("ingestion.text_ingestion.TEXT_JSONL", temp_jsonl)

    record = {
        "id": "bulbasaur_test",
        "modality": "text",
        "source_path": "data/raw/text/bulbasaur.pdf",
        "text": "Bulbasaur is a Grass/Poison-type starter Pokémon.",
        "pokemon": "Bulbasaur",
        "types": ["Grass", "Poison"],
        "generation": 1,
        "tags": ["starter", "bulbasaur"],
    }

    write_text_record(record)

    assert temp_jsonl.exists()
    lines = temp_jsonl.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1

    loaded = json.loads(lines[0])
    assert loaded["id"] == "bulbasaur_test"
    assert loaded["pokemon"] == "Bulbasaur"
    assert "Bulbasaur" in loaded["text"]


def test_add_text_pdf_moves_file_and_ingests(tmp_path, monkeypatch):
    raw_dir = tmp_path / "data" / "raw" / "text"
    monkeypatch.setattr(ingest_corpus, "RAW_TEXT_DIR", raw_dir, raising=True)

    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    upload_file = upload_dir / "squirtle_guide.pdf"
    upload_file.write_bytes(b"%PDF-1.4\n%fake")  # dummy PDF bytes

    calls: Dict[str, Any] = {}

    def fake_ingest_pdf(path: str, pokemon: str, generation: int, types: list[str]):
        calls["ingest_args"] = ("pdf", Path(path), pokemon, generation, types)
        return {
            "id": "squirtle_guide",
            "modality": "text",
            "source_path": path,
            "pokemon": pokemon,
            "generation": generation,
            "types": types,
            "text": "Squirtle PDF text.",
        }

    def fake_ingest_txt(path: str, pokemon: str, generation: int, types: list[str]):
        calls["ingest_args"] = ("txt", Path(path), pokemon, generation, types)
        return {
            "id": "squirtle_notes",
            "modality": "text",
            "source_path": path,
            "pokemon": pokemon,
            "generation": generation,
            "types": types,
            "text": "Squirtle TXT text.",
        }

    def fake_write_text_record(record: Dict[str, Any]) -> None:
        calls["written_record"] = record

    monkeypatch.setattr(ingest_corpus, "ingest_pdf", fake_ingest_pdf, raising=True)
    monkeypatch.setattr(ingest_corpus, "ingest_txt", fake_ingest_txt, raising=True)
    monkeypatch.setattr(
        ingest_corpus, "write_text_record", fake_write_text_record, raising=True
    )

    record = ingest_corpus.add_text(upload_file)

    target = raw_dir / upload_file.name
    assert target.exists()
    kind, ingest_path, pokemon, gen, types = calls["ingest_args"]
    assert kind == "pdf"
    assert ingest_path == target
    assert pokemon == "Squirtle"
    assert gen == 1
    assert "water" in [t.lower() for t in types]
    assert calls["written_record"] == record
    assert record["pokemon"] == "Squirtle"


def test_add_text_txt_uses_ingest_txt(tmp_path, monkeypatch):
    raw_dir = tmp_path / "data" / "raw" / "text"
    monkeypatch.setattr(ingest_corpus, "RAW_TEXT_DIR", raw_dir, raising=True)

    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    upload_file = upload_dir / "bulbasaur_notes.txt"
    upload_file.write_text("Bulbasaur notes")

    calls: Dict[str, Any] = {}

    def fake_ingest_pdf(*args, **kwargs):
        calls["pdf_called"] = True
        raise AssertionError("ingest_pdf should not be called for .txt")

    def fake_ingest_txt(path: str, pokemon: str, generation: int, types: list[str]):
        calls["ingest_args"] = (Path(path), pokemon, generation, types)
        return {
            "id": "bulbasaur_notes",
            "modality": "text",
            "source_path": path,
            "pokemon": pokemon,
            "generation": generation,
            "types": types,
            "text": "Bulbasaur TXT text.",
        }

    def fake_write_text_record(record: Dict[str, Any]) -> None:
        calls["written_record"] = record

    monkeypatch.setattr(ingest_corpus, "ingest_pdf", fake_ingest_pdf, raising=True)
    monkeypatch.setattr(ingest_corpus, "ingest_txt", fake_ingest_txt, raising=True)
    monkeypatch.setattr(
        ingest_corpus, "write_text_record", fake_write_text_record, raising=True
    )

    record = ingest_corpus.add_text(upload_file)

    target = raw_dir / upload_file.name
    assert target.exists()
    ingest_path, pokemon, gen, types = calls["ingest_args"]
    assert ingest_path == target
    assert pokemon == "Bulbasaur"
    assert gen == 1
    assert "grass" in [t.lower() for t in types]
    assert calls.get("pdf_called") is None
    assert calls["written_record"] == record
    assert record["pokemon"] == "Bulbasaur"
