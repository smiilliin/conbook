import json
from pathlib import Path
from typing import Any, Dict, List, Optional


def _get_history_base_path(base_dir: Optional[str] = None) -> Path:
    project_root = Path(__file__).resolve().parent.parent
    if base_dir:
        return project_root / base_dir
    return project_root


def load_history_records(base_dir: Optional[str] = None) -> List[Dict[str, Any]]:
    base_path = _get_history_base_path(base_dir)
    records: List[Dict[str, Any]] = []

    for json_file in sorted(base_path.glob("result*.json")):
        try:
            payload = json.loads(json_file.read_text(encoding="utf-8"))
        except Exception:
            continue

        summary = payload.get("summary", {}) or {}
        interests = payload.get("interests", []) or []
        tags: List[str] = []
        for item in interests:
            interest = item.get("interest", {}) or {}
            tags.extend(interest.get("tags", [])[:4])

        best_title = payload.get("title") or payload.get("book_title") or summary.get("summary", "")[:60]
        best_author = payload.get("author") or payload.get("book_author") or ""

        records.append(
            {
                "file_name": json_file.name,
                "title": best_title,
                "author": best_author,
                "summary": summary.get("summary", ""),
                "timestamp": summary.get("timestamp", ""),
                "keywords": [item.get("interest", {}).get("name", "") for item in interests if item.get("interest", {}).get("name")],
                "tag_pool": list(dict.fromkeys(tags))[:8],
                "count": len(interests),
            }
        )

    return records


def load_history_record(file_name: str, base_dir: Optional[str] = None) -> Dict[str, Any]:
    base_path = _get_history_base_path(base_dir)
    json_file = base_path / file_name

    try:
        return json.loads(json_file.read_text(encoding="utf-8"))
    except Exception:
        return {}
