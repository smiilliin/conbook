import time

import streamlit as st

from modules.chat_client import chat
from modules.history import load_history_records


ACTION_PROMPTS = {
    "📑 줄거리 정리": """
지금까지의 책 대화를 바탕으로
줄거리를 5~10문장으로 요약해줘.
스포일러는 포함해도 된다.
""",
    "💡 깊이 있는 해석": """
지금까지의 책 대화를 바탕으로
작품의 주제, 상징, 작가의 의도를
깊이 있게 분석해줘.
""",
    "🗣️ 토론하기": """
지금까지의 책 대화를 바탕으로
토론 질문 3개를 만들어줘.
각 질문마다 토론 포인트도 함께 작성해줘.
""",
    "✍🏻 독후감 작성": """
지금까지의 책 대화를 바탕으로
독후감을 작성해줘.

형식:
1. 책 소개
2. 줄거리
3. 느낀 점
4. 추천 이유
""",
    "🚀 인사이트 추출": """
지금까지의 책 대화를 바탕으로
핵심 인사이트 3개를 추출해줘.
각 인사이트는 한 문장 요약과 설명을 포함해줘.
""",
}

HISTORY_MINDMAP_PROMPT_TEMPLATE = """
다음은 과거 책 대화 기록입니다.
대화의 핵심 키워드를 추출하고,
계층적 마인드맵 트리 형태로 결과만 출력해 주세요.
출력 예시는 아래와 같습니다.

📖 죄와 벌
│
├── 👤 등장인물
│   ├─ 라스콜니코프
│   └─ 소냐
│
├── 💭 주제
│   ├─ 죄
│   └─ 구원
│
├── 🧠 철학
│   ├─ 니체
│   └─ 실존주의
│
└── ✍️ 내 생각

대화 기록:
{history_text}
"""


def render_summary_page() -> None:
    book_title = st.session_state.book_info.get("title", "책 제목")
    book_author = st.session_state.book_info.get("author", "저자명")
    st.title(f"{book_title} · {book_author}")
    st.subheader("📑 줄거리 정리")

    with st.status("줄거리 분석 중...", expanded=True) as status:
        st.write("🔄 1단계 대화 기록 데이터 전처리 중...")
        time.sleep(0.8)
        st.write("🧠 LLM 백엔드 로직 구동 중...")
        time.sleep(1.2)
        status.update(label="✅ 줄거리 정리 완료!", state="complete", expanded=False)

    st.write("---")
    summary = st.session_state.get("action_result", {}).get("summary", "")
    if summary:
        st.markdown(summary)
    else:
        st.info("결과가 없습니다.")

    st.write("")
    if st.button("◀️ 대화로 돌아가기", type="secondary", use_container_width=True):
        st.session_state.step = 1
        st.rerun()


def render_analysis_page() -> None:
    book_title = st.session_state.book_info.get("title", "책 제목")
    book_author = st.session_state.book_info.get("author", "저자명")
    st.title(f"{book_title} · {book_author}")
    st.subheader("💡 깊이 있는 해석")

    with st.status("해석 분석 중...", expanded=True) as status:
        st.write("🔄 1단계 대화 기록 데이터 전처리 중...")
        time.sleep(0.8)
        st.write("🧠 LLM 백엔드 로직 구동 중...")
        time.sleep(1.2)
        status.update(label="✅ 해석 분석 완료!", state="complete", expanded=False)

    st.write("---")
    analysis = st.session_state.get("action_result", {}).get("analysis", "")
    if analysis:
        st.markdown(analysis)
    else:
        st.info("결과가 없습니다.")

    st.write("")
    if st.button("◀️ 대화로 돌아가기", type="secondary", use_container_width=True):
        st.session_state.step = 1
        st.rerun()


def render_discussion_page() -> None:
    book_title = st.session_state.book_info.get("title", "책 제목")
    book_author = st.session_state.book_info.get("author", "저자명")
    st.title(f"{book_title} · {book_author}")
    st.subheader("🗣️ 토론하기")

    with st.status("토론 질문 생성 중...", expanded=True) as status:
        st.write("🔄 1단계 대화 기록 데이터 전처리 중...")
        time.sleep(0.8)
        st.write("🧠 LLM 백엔드 로직 구동 중...")
        time.sleep(1.2)
        status.update(label="✅ 토론 질문 생성 완료!", state="complete", expanded=False)

    st.write("---")
    discussion = st.session_state.get("action_result", {}).get("discussion", "")
    if discussion:
        st.markdown(discussion)
    else:
        st.info("결과가 없습니다.")

    st.write("")
    if st.button("◀️ 대화로 돌아가기", type="secondary", use_container_width=True):
        st.session_state.step = 1
        st.rerun()


def render_review_page() -> None:
    book_title = st.session_state.book_info.get("title", "책 제목")
    book_author = st.session_state.book_info.get("author", "저자명")
    st.title(f"{book_title} · {book_author}")
    st.subheader("✍🏻 독후감 작성")

    with st.status("독후감 작성 중...", expanded=True) as status:
        st.write("🔄 1단계 대화 기록 데이터 전처리 중...")
        time.sleep(0.8)
        st.write("🧠 LLM 백엔드 로직 구동 중...")
        time.sleep(1.2)
        status.update(label="✅ 독후감 작성 완료!", state="complete", expanded=False)

    st.write("---")
    review = st.session_state.get("action_result", {}).get("review", "")
    if review:
        st.markdown(review)
    else:
        st.info("결과가 없습니다.")

    st.write("")
    if st.button("◀️ 대화로 돌아가기", type="secondary", use_container_width=True):
        st.session_state.step = 1
        st.rerun()


def render_history_mindmap_page(client) -> None:
    selected_history = st.session_state.get("selected_history", "")
    if not selected_history:
        st.warning("📌 과거 기록을 선택해 주세요.")
        if st.button("◀️ 대화로 돌아가기", type="secondary", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
        return

    records = load_history_records()
    record = next((r for r in records if r.get("file_name") == selected_history), None)
    if not record:
        st.warning("선택한 과거 기록을 찾을 수 없습니다.")
        if st.button("◀️ 대화로 돌아가기", type="secondary", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
        return

    book_title = record.get("title", "책 제목")
    book_author = record.get("author", "저자명") or "저자명"
    st.title(f"{book_title} · {book_author}")
    st.subheader("🧠 과거 대화 마인드맵")

    mindmap = st.session_state.get("history_mindmap", "")
    if not mindmap:
        with st.spinner("과거 대화 데이터를 분석하고 마인드맵을 생성 중입니다..."):
            history_text = record.get("chat_text", record.get("summary", ""))
            prompt = HISTORY_MINDMAP_PROMPT_TEMPLATE.format(history_text=history_text)
            messages = [
                {
                    "role": "system",
                    "content": "당신은 대화 데이터를 바탕으로 계층적 마인드맵 트리 형태를 명확하게 작성하는 전문가입니다.",
                }
            ]
            _, mindmap = chat(prompt, messages, client)
            st.session_state.history_mindmap = mindmap

    st.write("---")
    if mindmap:
        st.code(mindmap, language="text")
    else:
        st.info("마인드맵 생성 결과가 없습니다.")

    st.write("")
    if st.button("◀️ 대화로 돌아가기", type="secondary", use_container_width=True):
        st.session_state.step = 1
        st.rerun()
