import streamlit as st

from modules.history import load_history_records


def _select_history(file_name: str) -> None:
    records = load_history_records()
    rec = next((r for r in records if r.get("file_name") == file_name), None)
    if rec:
        st.session_state.selected_history = file_name
        st.session_state.book_info = {
            "title": rec.get("title") or rec.get("file_name"),
            "author": rec.get("author", "") or "",
        }
        st.session_state.history_mindmap = ""
        st.session_state.step = 7
        st.rerun()


def render_sidebar() -> None:
    with st.sidebar:
        st.subheader("⚙️ 설정")
        st.text_input("닉네임", value=st.session_state.user_name, key="user_name", placeholder="홍길동")

        interest_options = [
            "선택(미설정)",
            "인문학",
            "사회과학",
            "자연과학",
            "공학",
            "의약학",
            "예술체육",
            "복합학",
        ]
        selected_interest = st.selectbox(
            "관심사",
            interest_options,
            index=(interest_options.index(st.session_state.interest_area[0])
                   if st.session_state.interest_area
                   and st.session_state.interest_area[0] in interest_options
                   else 0),
            help="관심 분야를 선택하세요. 선택된 항목은 대화 맥락에 반영됩니다.",
        )
        st.session_state.interest_area = [selected_interest]

        st.divider()

        st.subheader("📚 독서 기록")
        if st.button("➕ 새 채팅", use_container_width=True):
            st.session_state.step = 0
            st.session_state.chat_ready = False
            st.session_state.chat_history = []
            st.session_state.book_info = {"title": "", "author": ""}
            st.session_state.selected_history = ""
            st.rerun()

        records = load_history_records()
        if records:
            for rec in records[:5]:
                title = rec.get("title") or rec.get("file_name")
                author = rec.get("author") or ""
                label = f"{title} · {author}" if author else f"{title}"
                key = f"history_{rec.get('file_name')}"
                if st.button(label, key=key, use_container_width=True):
                    _select_history(rec.get("file_name"))
        else:
            st.info("과거 세션이 없습니다. 새 채팅을 시작해 보세요.")
