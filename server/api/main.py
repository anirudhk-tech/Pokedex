# api/main.py
import logging

from fastapi import (  # type: ignore (local editor interpreter issue)
    FastAPI,
    HTTPException,
)
from scripts.ingest import main as run_full_ingest
from scripts.process import main as run_build_graph

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

app = FastAPI(title="Pokemon Starter RAG API")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ingest")
def ingest_corpus() -> dict:
    """
    Run the full ingestion pipeline:
    - ingest_text_corpus.main()
    - ingest_images_corpus.main()
    - ingest_audio_corpus.main()
    """
    try:
        logger.info("API: starting full ingestion via /ingest")
        run_full_ingest()
        logger.info("API: ingestion completed")
        return {"message": "Ingestion process completed."}
    except Exception as e:
        logger.exception("Error during ingestion")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process")
def process_graph() -> dict:
    """
    Run the graph-building pipeline:
    - build_graph_and_export_to_csv_and_json()
    """
    try:
        logger.info("API: starting graph build via /process")
        run_build_graph()
        logger.info("API: graph built and exported")
        return {"message": "Graph built and exported to CSV and JSON successfully."}
    except Exception as e:
        logger.exception("Error during graph processing")
        raise HTTPException(status_code=500, detail=str(e))
