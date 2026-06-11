import streamlit as st

from modules import (
    build_system_prompt,
    create_client,
    render_book_info,
    render_insight_page,
    render_chat,
    render_sidebar,
    render_summary_page,
    render_analysis_page,
    render_discussion_page,
    render_review_page,
    render_history_mindmap_page,
)


def set_page_config() -> None:
    st.set_page_config(page_title="Conbook UI Prototype", page_icon="📚", layout="wide")


def init_session_state() -> None:
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    if "book_info" not in st.session_state:
        st.session_state.book_info = {"title": "", "author": ""}
    if "goal_setting" not in st.session_state:
        st.session_state.goal_setting = "선택(미설정)"
    if "interest_area" not in st.session_state:
        st.session_state.interest_area = ["선택(미설정)"]
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": build_system_prompt(st.session_state.goal_setting, st.session_state.interest_area)}
        ]
    if "chat_ready" not in st.session_state:
        st.session_state.chat_ready = False
    if "selected_history" not in st.session_state:
        st.session_state.selected_history = ""
    if "history_mindmap" not in st.session_state:
        st.session_state.history_mindmap = ""


def main() -> None:
    set_page_config()
    init_session_state()
    render_sidebar()

    client = create_client()
    step = st.session_state.step

    if step == 0:
        render_book_info()
    elif step == 1:
        render_chat(client)
    elif step == 2:
        render_insight_page()
    elif step == 3:
        render_summary_page()
    elif step == 4:
        render_analysis_page()
    elif step == 5:
        render_discussion_page()
    elif step == 6:
        render_review_page()
    elif step == 7:
        render_history_mindmap_page(client)
    else:
        render_book_info()


if __name__ == "__main__":
    main()
