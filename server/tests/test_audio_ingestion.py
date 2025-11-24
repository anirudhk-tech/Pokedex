import json
from pathlib import Path
from typing import Any, Dict

import scripts.ingest_audio_corpus as ingest_corpus
from ingestion.audio_ingestion import (
    extract_text_from_audio,
    ingest_audio,
    write_audio_record,
)
from processing import vector_store


class FakeModel:
    def transcribe(
        self, path: str, fp16: bool
    ) -> Dict[
        str, str
    ]:  # fp16 is a boolean that disables warnings on CPU, unnecessary for tests
        assert path.endswith("bulbasaur.mp3")
        return {"text": "This is a Bulbasaur audio clip"}


def test_text_from_audio_smoke(tmp_path: Path, monkeypatch):
    fake_audio = tmp_path / "bulbasaur.mp3"
    fake_audio.write_bytes(b"RIFF....")

    def fake_transcribe(path: str) -> str:
        assert path.endswith("bulbasaur.mp3")
        return "This is a Bulbasaur audio clip"

    monkeypatch.setattr(
        "ingestion.audio_ingestion.extract_text_from_audio", fake_transcribe
    )

    text = extract_text_from_audio(str(fake_audio), model=FakeModel())
    assert "bulbasaur" in text.lower()


def test_ingest_audio_builds_record(tmp_path: Path, monkeypatch):
    audio_path = tmp_path / "bulbasaur.mp3"
    audio_path.write_bytes(b"RIFF....")

    monkeypatch.setattr(
        "ingestion.audio_ingestion.write_audio_record",
        lambda p: "Bulbasaur is a Grass/Poison-type starter Pokémon.",
    )

    monkeypatch.setattr(
        "ingestion.audio_ingestion.upsert_document", lambda *a, **k: None, raising=True
    )
    monkeypatch.setattr(
        "ingestion.audio_ingestion.embed_text", lambda text: [0.0] * 1536, raising=True
    )

    record = ingest_audio(
        str(audio_path),
        pokemon="Bulbasaur",
        generation=1,
        types=["Grass", "Poison"],
        model=FakeModel(),
    )

    assert record["id"] == audio_path.stem
    assert record["modality"] == "audio"
    assert record["source_path"].endswith("bulbasaur.mp3")
    assert record["pokemon"] == "Bulbasaur"
    assert record["types"] == ["Grass", "Poison"]
    assert record["generation"] == 1
    assert "audio" in record["tags"]
    assert "starter" in record["tags"]
    assert "bulbasaur" in [t.lower() for t in record["tags"]]
    assert "bulbasaur" in record["text"].lower()


def test_write_audio_record_creates_valid_jsonl(tmp_path: Path, monkeypatch):
    temp_jsonl = tmp_path / "audio.jsonl"
    monkeypatch.setattr("ingestion.audio_ingestion.AUDIO_JSONL", temp_jsonl)

    record = {
        "id": "bulbasaur_audio_test",
        "modality": "audio",
        "source_path": "data/raw/audio/bulbasaur_sample.mp3",
        "text": "Bulbasaur audio sample transcript.",
        "pokemon": "Bulbasaur",
        "generation": 1,
        "types": ["Grass", "Poison"],
        "tags": ["starter", "audio", "bulbasaur"],
    }

    write_audio_record(record)

    assert temp_jsonl.exists()
    lines = temp_jsonl.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1

    loaded = json.loads(lines[0])
    assert loaded["id"] == "bulbasaur_audio_test"
    assert loaded["pokemon"] == "Bulbasaur"
    assert "Bulbasaur" in loaded["text"]


def test_add_audio_moves_file_and_ingests(tmp_path, monkeypatch):
    raw_dir = tmp_path / "data" / "raw" / "audio"
    monkeypatch.setattr(ingest_corpus, "RAW_AUDIO_DIR", raw_dir, raising=True)

    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    upload_file = upload_dir / "bulbasaur_intro.mp3"
    upload_file.write_bytes(b"fake mp3 bytes")

    calls: Dict[str, Any] = {}

    def fake_ingest_audio(path: str, pokemon: str, generation: int, types: list[str]):
        calls["ingest_args"] = (Path(path), pokemon, generation, types)
        return {
            "id": "bulbasaur_intro",
            "modality": "audio",
            "source_path": path,
            "pokemon": pokemon,
            "generation": generation,
            "types": types,
            "text": "Bulbasaur audio transcript.",
        }

    def fake_write_audio_record(record: Dict[str, Any]) -> None:
        calls["written_record"] = record

    monkeypatch.setattr(ingest_corpus, "ingest_audio", fake_ingest_audio, raising=True)
    monkeypatch.setattr(
        ingest_corpus, "write_audio_record", fake_write_audio_record, raising=True
    )

    record = ingest_corpus.add_audio(upload_file)

    target = raw_dir / upload_file.name
    assert target.exists()

    ingest_path, pokemon, gen, types = calls["ingest_args"]
    assert ingest_path == target
    assert pokemon == "Bulbasaur"
    assert gen == 1
    assert "grass" in [t.lower() for t in types]

    assert calls["written_record"] == record
    assert record["pokemon"] == "Bulbasaur"
