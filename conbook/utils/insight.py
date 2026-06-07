import json
import os
import re
from pathlib import Path


def _extract_title_author(summary: str) -> tuple[str, str]:

    if not summary:
        return "", ""

    summary = summary.strip()
    patterns = [
        r"사용자가 ([가-힣A-Za-z]+)의 (.+?)을 읽으며",
        r"사용자가 ([가-힣A-Za-z]+)의 (.+?)을 읽고",
        r"([가-힣A-Za-z]+)의 (.+?)을 읽으며",
        r"([가-힣A-Za-z]+)의 [『\"']?([^』\"']+)[』\"']?",
    ]

    for pattern in patterns:
        match = re.search(pattern, summary, re.DOTALL)
        if match:
            if len(match.groups()) >= 2:
                author = match.group(1).strip()
                title = match.group(2).strip()
                return title, author
            if len(match.groups()) == 1:
                return match.group(1).strip(), ""

    title_match = re.search(r"[『\"']?([^』\"']+)[』\"']?", summary)
    title = title_match.group(1).strip() if title_match else ""
    return title, ""


def _find_project_root() -> Path:
    env_root = os.environ.get("CONBOOK_ROOT") or os.environ.get("CONBOOK_PATH")
    candidates = []
    if env_root:
        candidates.append(Path(env_root).expanduser().resolve())

    current_file = Path(__file__).resolve()
    candidates.append(current_file.parent.parent.parent)
    candidates.extend(current_file.parents)

    cwd = Path.cwd().resolve()
    candidates.append(cwd)
    candidates.extend(cwd.parents)

    seen = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if not candidate.exists():
            continue
        if (candidate / "conbook").is_dir() and (candidate / "requirements.txt").exists():
            return candidate
        if (candidate / "conbook").is_dir() and ((candidate / "data").exists() or (candidate / "test_data").exists()):
            return candidate

    return current_file.parent.parent.parent


def load_history_records() -> list[dict]:
    base_dir = _find_project_root()
    records = []
    seen_files = set()

    search_paths = []
    session_path = base_dir / "data" / "sessions"
    if session_path.exists():
        search_paths.extend(sorted(session_path.glob("*.json")))

    package_session_path = base_dir / "conbook" / "data" / "sessions"
    if package_session_path.exists():
        search_paths.extend(sorted(package_session_path.glob("*.json")))

    search_paths.extend(sorted(base_dir.glob("*.json")))
    test_data_dir = base_dir / "test_data"
    if test_data_dir.exists():
        search_paths.extend(sorted(test_data_dir.glob("*.json")))

    for json_file in search_paths:
        if json_file.name in seen_files:
            continue
        seen_files.add(json_file.name)

        try:
            payload = json.loads(json_file.read_text(encoding="utf-8"))
        except Exception:
            continue

        if isinstance(payload, list):
            payload = {"conversation": payload}

        summary_raw = payload.get("summary", "")
        if isinstance(summary_raw, dict):
            summary = summary_raw.get("summary", "")
        elif isinstance(summary_raw, str):
            summary = summary_raw
        else:
            summary = ""

        parsed_title, parsed_author = _extract_title_author(summary)
        title = (
            payload.get("title")
            or payload.get("book_title")
            or parsed_title
            or summary
            or json_file.stem
        )
        author = (
            payload.get("author")
            or payload.get("writer")
            or payload.get("author_name")
            or parsed_author
            or "미상"
        )

        interests = payload.get("interests", []) or []
        if isinstance(interests, dict):
            interests = [interests]

        conversation = (
            payload.get("conversation")
            or payload.get("messages")
            or payload.get("chat_history")
            or payload.get("dialog")
            or []
        )
        if isinstance(conversation, dict):
            conversation = [conversation]
        if not isinstance(conversation, list):
            conversation = []

        keywords = []
        keyword_details = []
        for item in interests:
            keyword = ""
            tags = []
            if isinstance(item, dict):
                interest_obj = item.get("interest") or item
                keyword = (
                    interest_obj.get("name")
                    or item.get("name")
                    or item.get("interest_name")
                    or ""
                )
                tags = interest_obj.get("tags") or []
                if isinstance(tags, list):
                    tags = [str(t) for t in tags if t]
                else:
                    tags = []
            elif isinstance(item, str):
                keyword = item

            if keyword:
                keywords.append(keyword)
                keyword_details.append(
                    {"keyword": keyword, "tags": tags}
                )

        records.append(
            {
                "file_name": json_file.name,
                "title": title,
                "author": author,
                "summary": summary,
                "timestamp": payload.get("timestamp", ""),
                "keywords": [keyword for keyword in keywords if keyword],
                "keyword_details": keyword_details,
                "tag_pool": list(dict.fromkeys(keywords))[:8],
                "count": len(keywords),
                "conversation": conversation,
            }
        )

    return records
