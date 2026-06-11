import streamlit as st


def render_book_info() -> None:
    st.title("📖 Conbook")
    nickname = st.session_state.get("nickname", "홍길동")
    st.write(f"{nickname}님 안녕하세요! 책으로 대화하는 AI, Conbook에 오신 것을 환영합니다.")
    
    st.divider()
    st.write("")

    st.subheader("책 정보 입력")
    col1, col2 = st.columns(2)
    
    with col1:
        book_title = st.text_input(
            "책 제목 (필수)",
            value=st.session_state.book_info.get("title", ""),
            placeholder="예: 이방인"
        )
    
    with col2:
        book_author = st.text_input(
            "저자명 (선택)",
            value=st.session_state.book_info.get("author", ""),
            placeholder="예: 알베르 카뮈"
        )
    
    st.session_state.book_info = {"title": book_title, "author": book_author}
    
    st.write("")
    if st.button("대화 시작하기", use_container_width=True, type="primary"):
        if not book_title.strip():
            st.warning("📌 책 제목을 입력해 주세요.")
        else:
            st.session_state.step = 1
            st.session_state.chat_ready = True
            st.rerun()
