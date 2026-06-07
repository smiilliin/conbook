import streamlit as st


def render_book_info() -> None:
    st.title("Conbook: 대화와 기록")
    user_label = st.session_state.user_name.strip() or "홍길동"
    st.write(f"안녕하세요, **{user_label}**님! AI와 함께 책과 관련된 생각을 나누어봐요.")

    st.write("")
    st.subheader("📖 책 정보 입력")
    col1, col2, col3 = st.columns([2, 2, 1])
    book_title = col1.text_input(
        "책 제목 (필수)",
        value=st.session_state.book_info["title"],
        placeholder="예: 이방인",
        key="book_input_title",
    )
    book_author = col2.text_input(
        "저자명 (선택)",
        value=st.session_state.book_info["author"],
        placeholder="예: 알베르 카뮈",
        key="book_input_author",
    )
    with col3:
        st.session_state.goal_setting = st.selectbox(
            "목표",
            ["선택(미설정)", "정보습득", "의사결정", "자기계발", "취미독서"],
            index=["선택(미설정)", "정보습득", "의사결정", "자기계발", "취미독서"].index(st.session_state.goal_setting),
        )

    st.session_state.book_info["title"] = book_title
    st.session_state.book_info["author"] = book_author

    if st.button(" 대화 시작하기", use_container_width=True):
        if not book_title.strip():
            st.warning("⚠️ 책 제목을 입력해야 채팅을 시작할 수 있습니다.")
        else:
            st.session_state.chat_ready = True
            st.session_state.step = 1
            st.session_state.chat_history = []
            st.rerun()

    if book_title.strip():
        author_text = book_author.strip() or "저자 미입력"
        st.info(f"대화 제목: **{book_title}** · {author_text}")
