import json
from pathlib import Path


def load_history_records(base_dir="conbook-master"):
    base_path = Path(__file__).resolve().parent.parent / base_dir
    records = []

    for json_file in sorted(base_path.glob("result*.json")):
        try:
            payload = json.loads(json_file.read_text(encoding="utf-8"))
        except Exception:
            continue

        summary = payload.get("summary", {}) or {}
        interests = payload.get("interests", []) or []
        tags = []
        for item in interests:
            interest = item.get("interest", {}) or {}
            tags.extend(interest.get("tags", [])[:4])

        records.append(
            {
                "file_name": json_file.name,
                "title": summary.get("summary", "")[:60],
                "summary": summary.get("summary", ""),
                "timestamp": summary.get("timestamp", ""),
                "keywords": [item.get("interest", {}).get("name", "") for item in interests if item.get("interest", {}).get("name")],
                "tag_pool": list(dict.fromkeys(tags))[:8],
                "count": len(interests),
            }
        )

    return records
