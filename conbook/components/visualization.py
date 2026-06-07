import math
import re
from collections import Counter

import plotly.graph_objects as go
import streamlit as st

from conbook.utils.insight import load_history_records


def extract_keywords(record: dict, max_keywords: int = 5) -> list[str]:
    if record.get("keywords"):
        return [str(k) for k in record["keywords"][:max_keywords] if k]

    summary = str(record.get("summary", "") or "")
    tokens = re.findall(r"[가-힣A-Za-z]{2,}", summary)
    stopwords = {
        "에서", "있는", "하는", "하다", "그리고", "이런", "그런", "있다", "됩니다", "합니다",
        "것이", "것을", "때문", "사용자", "대화", "기록", "책의",
    }
    candidates = [tok for tok in tokens if tok not in stopwords]
    most_common = Counter(candidates).most_common(max_keywords)
    return [word for word, _ in most_common]


def truncate_text(text: str, limit: int = 120) -> str:
    clean_text = " ".join(str(text).split())
    if len(clean_text) <= limit:
        return clean_text
    return clean_text[:limit].rstrip() + "..."


def build_mindmap(records: list[dict], user_label: str) -> go.Figure:
    nodes = []
    edges = []

    nodes.append({
        "id": "user",
        "type": "user",
        "label": user_label,
        "x": 0.0,
        "y": 0.0,
        "font_size": 16,
    })

    book_count = len(records)
    book_radius = 1.1
    for idx, record in enumerate(records):
        angle = 2 * math.pi * idx / max(book_count, 1)
        book_x = book_radius * math.cos(angle)
        book_y = book_radius * math.sin(angle)
        book_label = record.get("title") or record.get("file_name")
        book_id = f"book::{record['file_name']}"
        nodes.append({
            "id": book_id,
            "type": "book",
            "label": book_label,
            "x": book_x,
            "y": book_y,
            "font_size": 14,
        })
        edges.append(("user", book_id))

        keyword_entries = record.get("keyword_details") or []
        if not keyword_entries:
            keywords = extract_keywords(record, max_keywords=4)
            keyword_entries = [{"keyword": kw, "tags": []} for kw in keywords or ["키워드 없음"]]
        if not keyword_entries:
            keyword_entries = [{"keyword": "키워드 없음", "tags": []}]

        keyword_radius = 1.4
        detail_radius = 1.8
        keyword_span = 0.45
        keyword_count = len(keyword_entries)
        for keyword_idx, entry in enumerate(keyword_entries[:5]):
            keyword = entry.get("keyword") or "키워드 없음"
            tags = entry.get("tags") or []
            detail_text = ", ".join(tags[:3]) if tags else ""
            if not detail_text:
                detail_text = "태그 없음"
            keyword_angle = angle + (keyword_idx - (keyword_count - 1) / 2) * keyword_span / max(keyword_count, 1)
            keyword_x = keyword_radius * math.cos(keyword_angle)
            keyword_y = keyword_radius * math.sin(keyword_angle)
            keyword_id = f"kw::{record['file_name']}::{keyword}"
            nodes.append({
                "id": keyword_id,
                "type": "keyword",
                "label": keyword,
                "x": keyword_x,
                "y": keyword_y,
                "font_size": 12,
            })
            edges.append((book_id, keyword_id))

            detail_x = detail_radius * math.cos(keyword_angle)
            detail_y = detail_radius * math.sin(keyword_angle)
            detail_id = f"detail::{record['file_name']}::{keyword}"
            nodes.append({
                "id": detail_id,
                "type": "detail",
                "label": detail_text,
                "x": detail_x,
                "y": detail_y,
                "font_size": 10,
            })
            edges.append((keyword_id, detail_id))

    edge_x = []
    edge_y = []
    for source_id, target_id in edges:
        source = next(node for node in nodes if node["id"] == source_id)
        target = next(node for node in nodes if node["id"] == target_id)
        edge_x.extend([source["x"], target["x"], None])
        edge_y.extend([source["y"], target["y"], None])

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(color="#94a3b8", width=1.8),
            hoverinfo="none",
        )
    )

    for node_type, text_size, text_color in [
        ("user", 16, "#0f172a"),
        ("book", 14, "#0f172a"),
        ("keyword", 12, "#0f172a"),
        ("detail", 10, "#334155"),
    ]:
        group_nodes = [node for node in nodes if node.get("type") == node_type]
        if not group_nodes:
            continue
        fig.add_trace(
            go.Scatter(
                x=[node["x"] for node in group_nodes],
                y=[node["y"] for node in group_nodes],
                mode="text",
                text=[node["label"] for node in group_nodes],
                textposition="middle center",
                textfont=dict(size=text_size, family="Noto Sans KR", color=text_color),
                hoverinfo="text",
            )
        )

    fig.update_layout(
        showlegend=False,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=900,
    )
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    return fig


def render_visualization_page() -> None:
    st.title("🧠 독서 마인드맵")
    st.caption("최근 대화 기록에서 책 제목과 키워드를 추출하여 사용자 중심의 마인드맵을 생성합니다.")

    records = load_history_records()
    if not records:
        st.info("현재 불러올 수 있는 세션 기록이 없습니다. JSON 기록을 추가해 주세요.")
        return

    recent_books = sorted(
        records,
        key=lambda r: r.get("timestamp") or "",
        reverse=True,
    )[:10]
    if not any(rec.get("timestamp") for rec in recent_books):
        recent_books = records[-10:]

    user_label = st.session_state.get("user_name", "홍길동") or "홍길동"

    fig = build_mindmap(recent_books, user_label)
    st.plotly_chart(fig, use_container_width=True)


