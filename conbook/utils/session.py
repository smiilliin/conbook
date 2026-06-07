import streamlit as st

from conbook.utils.prompt import build_system_prompt


def set_page_config() -> None:
    st.set_page_config(page_title="Conbook : 나만의 독서 기록장", page_icon="📚", layout="wide")


def init_session_state() -> None:
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "book_info" not in st.session_state:
        st.session_state.book_info = {"title": "", "author": ""}
    if "goal_setting" not in st.session_state:
        st.session_state.goal_setting = "선택(미설정)"
    if "interest_area" not in st.session_state:
        st.session_state.interest_area = ["선택(미설정)"]
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    if "chat_ready" not in st.session_state:
        st.session_state.chat_ready = False
    if "selected_history" not in st.session_state:
        st.session_state.selected_history = ""
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": build_system_prompt(st.session_state.goal_setting, st.session_state.interest_area)}]
