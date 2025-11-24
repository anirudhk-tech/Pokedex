import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

EVAL_LOG_PATH = Path("logs/eval.jsonl")


def log_evaluation(
    query: str,
    answer: str,
    retrieved_context: Dict[str, Any],
    evaluation_scores: Dict[str, Any],
    focused_pokemon: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Append a single evaluation record as JSON to logs/eval.jsonl.
    Creates the directory/file if needed.
    """
    EVAL_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    record: Dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "answer": answer,
        "retrieved_context": retrieved_context,
        "evaluation": evaluation_scores,
    }

    if focused_pokemon is not None:
        record["focused_pokemon"] = focused_pokemon

    if extra:
        record["extra"] = extra

    with EVAL_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
