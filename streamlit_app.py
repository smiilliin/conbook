from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

DEFAULT_RESULT_PATH = Path(__file__).with_name("result4.json")


def load_json_from_text(text: str) -> dict:
    return json.loads(text)


def load_json_from_file(file_path: Path) -> dict:
    return load_json_from_text(file_path.read_text(encoding="utf-8"))


def render_direction_items(items: list[dict]) -> None:
    if not items:
        st.caption("direction 항목이 없습니다.")
        return

    for item in items:
        entity = item.get("entity", "unknown")
        description = item.get("description", "")
        st.markdown(f"- **{entity}**: {description}")


def render_result(data: dict) -> None:
    summary = data.get("summary", {})
    interests = data.get("interests", [])

    st.subheader("전체 요약")
    st.write(summary.get("summary", ""))

    summary_interests = summary.get("interests", [])
    if summary_interests:
        st.subheader("추출된 관심사")
        st.write(", ".join(summary_interests))

    if not interests:
        st.info("표시할 interest 결과가 없습니다.")
        return

    st.subheader("관심사별 결과")
    for index, block in enumerate(interests, start=1):
        interest = block.get("interest", {})
        direction = block.get("direction") or {}

        with st.expander(f"{index}. {interest.get('name', 'unknown')}", expanded=True):
            tags = interest.get("tags", [])
            if tags:
                st.write("태그:", ", ".join(tags))

            st.write("방향 요약:", direction.get("summary", ""))
            st.write("대화 흐름:")
            render_direction_items(direction.get("direction", []))


st.set_page_config(page_title="Conbook Result Viewer", layout="wide")
st.title("Conbook 결과 뷰어")
st.caption("result4.json을 읽어 텍스트 중심으로 보여줍니다.")

source = st.sidebar.radio(
    "데이터 소스",
    ["기본 파일", "파일 업로드", "JSON 직접 입력"],
)

raw_text = ""
source_label = ""

if source == "기본 파일":
    source_label = str(DEFAULT_RESULT_PATH)
    if DEFAULT_RESULT_PATH.exists():
        raw_text = DEFAULT_RESULT_PATH.read_text(encoding="utf-8")
    else:
        st.error(f"기본 파일을 찾을 수 없습니다: {DEFAULT_RESULT_PATH}")
elif source == "파일 업로드":
    uploaded_file = st.file_uploader("result4.json 업로드", type=["json"])
    if uploaded_file is not None:
        source_label = uploaded_file.name
        raw_text = uploaded_file.read().decode("utf-8")
else:
    source_label = "직접 입력"
    raw_text = st.text_area(
        "JSON 붙여넣기", height=260, placeholder="여기에 result JSON을 붙여넣으세요."
    )

if raw_text.strip():
    try:
        data = load_json_from_text(raw_text)
    except json.JSONDecodeError as exc:
        st.error(f"JSON 파싱 실패: {exc}")
    else:
        st.sidebar.success(f"로드 완료: {source_label}")
        render_result(data)

        with st.expander("원본 JSON 보기"):
            st.code(raw_text, language="json")
else:
    st.info("왼쪽 사이드바에서 파일을 고르거나 JSON을 입력하세요.")
