import streamlit as st

from conbook.utils.insight import load_history_records


def render_sidebar() -> None:
    with st.sidebar:
        st.subheader("⚙️ 설정")
        st.text_input("닉네임", value=st.session_state.user_name, key="user_name", placeholder="홍길동")
        interest_options = ["선택(미설정)", "인문학", "사회과학", "자연과학", "공학", "의약학", "예술체육", "복합학"]
        selected_interest = st.selectbox(
            "관심사",
            interest_options,
            index=interest_options.index(st.session_state.interest_area[0]) if st.session_state.interest_area and st.session_state.interest_area[0] in interest_options else 0,
            help="관심 분야를 선택하세요. 선택된 항목은 대화 맥락에 반영됩니다.",
        )
        st.session_state.interest_area = [selected_interest]

        st.divider()

        st.subheader("🗂️ 채팅 기록")
        if st.button("➕ 새 채팅", use_container_width=True):
            st.session_state.step = 0
            st.session_state.chat_ready = False
            st.session_state.chat_history = []
            st.session_state.book_info = {"title": "", "author": ""}
            st.session_state.selected_history = ""
            st.rerun()
        if st.button("➕ 생각 지도", use_container_width=True):
            st.session_state.step = 3
            st.rerun()

        records = load_history_records()
        if records:
            for rec in records[:5]:
                st.markdown(
                    f"<div style='padding:12px; border:1px solid #e2e8f0; border-radius:14px; margin-bottom:10px; background:#ffffff;'>"
                    f"<div style='font-weight:700; margin-bottom:4px;'>{rec['title']} · {rec['author']}</div>"
                    f"<div style='color:#475569; font-size:13px;'>최근 대화 요약을 빠르게 확인하세요.</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
        else:
            st.info("과거 세션이 없습니다. 새 채팅을 시작해 보세요.")
