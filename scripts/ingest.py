import logging

from scripts.ingest_audio_corpus import main as ingest_audio_data
from scripts.ingest_images_corpus import main as ingest_images_data
from scripts.ingest_text_corpus import main as ingest_text_data

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)


def main():
    logger.info("Starting ingestion process...")
    logger.info("Ingesting text data...")
    ingest_text_data()
    logger.info("Ingesting image data...")
    ingest_images_data()
    logger.info("Ingesting audio data...")
    ingest_audio_data()
    logger.info("Ingestion process completed.")


if __name__ == "__main__":
    main()
