import json
import logging
from pathlib import Path

from fastapi import APIRouter  # type: ignore (safe to ignore, local editor quirk)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["logs"])

LOGS_PATH = Path("logs/eval.jsonl")


@router.get("/logs")
def get_logs():
    if not LOGS_PATH.exists():
        return []
    records = []
    with LOGS_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records
