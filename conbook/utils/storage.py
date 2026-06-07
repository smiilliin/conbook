import json
import uuid
from pathlib import Path

CONVERSATIONS_FILE = Path(__file__).resolve().parent.parent / "data" / "sessions" / "conversations.jsonl"


def new_session_id() -> str:
    return str(uuid.uuid4())


def make_entity(session_id: str, index: int) -> str:
    return f"{session_id}_s{index:03d}"


def assign_entities(messages: list[dict], session_id: str, exclude_system=True) -> list[dict]:
    result = []
    idx = 0
    for m in messages:
        if exclude_system and m.get("role") == "system":
            continue
        result.append({
            "entity": make_entity(session_id, idx),
            "session_id": session_id,
            "role": m.get("role", ""),
            "content": m.get("content", ""),
            "timestamp": m.get("timestamp", ""),
        })
        idx += 1
    return result


def save_session(messages: list[dict], session_id: str | None = None, filepath: Path | None = None) -> str:
    if filepath is None:
        filepath = CONVERSATIONS_FILE
    if session_id is None:
        session_id = new_session_id()

    filepath.parent.mkdir(parents=True, exist_ok=True)
    records = assign_entities(messages, session_id)

    with filepath.open("a", encoding="UTF-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return session_id


def load_session(session_id: str, filepath: Path | None = None) -> list[dict]:
    if filepath is None:
        filepath = CONVERSATIONS_FILE

    records = []
    if not filepath.exists():
        return records

    with filepath.open("r", encoding="UTF-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if record.get("session_id") == session_id:
                records.append(record)

    records.sort(key=lambda r: r["entity"])
    return records


def records_to_messages(records: list[dict]) -> list[dict]:
    return [{"role": r["role"], "content": r["content"]} for r in records]


def entities_to_text(records: list[dict]) -> str:
    return "\n".join(
        f"entity: {r['entity']}, {r['role']}: {r['content']}" for r in records
    )
