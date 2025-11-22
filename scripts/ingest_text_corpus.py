import logging
from pathlib import Path

from ingestion.text_ingestion import ingest_pdf, ingest_txt, write_record

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

RAW_TEXT_DIR = Path("data/raw/text")

POKEMON_MAPPING = {  # basic metadata (name, generation)
    "Bulbasaur": ("Bulbasaur", 1),
    "Charmander": ("Charmander", 1),
    "Squirtle": ("Squirtle", 1),
}


def resolve_metadata(path: Path) -> tuple[str, int]:
    for key, (pokemon, gen) in POKEMON_MAPPING.items():
        if key.lower() in path.stem.lower():
            return pokemon, gen
    raise ValueError(f"Could not resolve metadata for {path}")


def main() -> None:
    for path in RAW_TEXT_DIR.iterdir():
        if not path.is_file():
            continue

        if path.suffix.lower() not in {".pdf", ".txt"}:
            continue

        pokemon, generation = resolve_metadata(path)

        if path.suffix.lower() == ".pdf":
            record = ingest_pdf(str(path), pokemon=pokemon, generation=generation)
            write_record(record)
        elif path.suffix.lower() == ".txt":
            record = ingest_txt(str(path), pokemon=pokemon, generation=generation)
            write_record(record)


if __name__ == "__main__":
    main()
