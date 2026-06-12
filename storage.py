import json
import uuid
from pathlib import Path

CONVERSATIONS_FILE = "conversations.jsonl"


def new_session_id() -> str:
    return str(uuid.uuid4())


def make_entity(session_id: str, index: int) -> str:
    return f"{session_id}_s{index:03d}"


def assign_entities(messages: list[dict], session_id: str, exclude_system=True) -> list[dict]:
    """각 메시지에 entity를 붙여 반환. system 메시지는 기본 제외."""
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
            "time": m.get("time")
        })
        idx += 1
    return result


def save_session(messages: list[dict], session_id: str | None = None, filepath: str = CONVERSATIONS_FILE) -> str:
    """대화를 entity와 함께 JSONL 파일에 저장. session_id를 반환."""
    if session_id is None:
        session_id = new_session_id()

    records = assign_entities(messages, session_id)

    with open(filepath, "a", encoding="UTF-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return session_id


def load_session(session_id: str, filepath: str = CONVERSATIONS_FILE) -> list[dict]:
    """특정 세션의 메시지를 entity 순서대로 불러옴."""
    records = []
    path = Path(filepath)
    if not path.exists():
        return records

    with open(filepath, "r", encoding="UTF-8") as f:
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
    """저장된 records를 LLM용 messages 형식으로 변환."""
    return [{"role": r["role"], "content": r["content"]} for r in records]


def entities_to_text(records: list[dict]) -> str:
    """entity와 대화를 텍스트로 변환 (insight 추출용)."""
    parts = []
    for r in records:
        parts.append(f"entity: {r['entity']}, {r['role']}: {r['content']}")
    return "\n".join(parts)
