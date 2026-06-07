import streamlit as st

from conbook.utils.api import chat
from conbook.utils.prompt import build_system_prompt


def render_chat(client) -> None:
    if st.session_state.book_info.get("title"):
        book_title = st.session_state.book_info["title"]
        st.markdown(f"## 💬 *{book_title}* 에 대한 대화")
        if st.session_state.chat_ready:
            st.caption("현재 채팅 상태: 읽는 중")
    else:
        st.warning("⚠️ 책 정보가 없습니다. 먼저 책 정보 입력 페이지로 돌아가 주세요.")

    if st.session_state.messages and st.session_state.messages[0].get("role") == "system":
        st.session_state.messages[0]["content"] = build_system_prompt(st.session_state.goal_setting, st.session_state.interest_area)

    if not st.session_state.chat_history:
        st.info("⚠️ 새로운 대화를 시작하려면 아래 입력창에 메시지를 입력해 주세요.")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if st.session_state.chat_ready:
        if prompt := st.chat_input("책에 대한 생각이나 느낌을 자유롭게 입력하세요..."):
            if not st.session_state.messages or st.session_state.messages[0].get("role") != "system":
                st.session_state.messages = [{"role": "system", "content": build_system_prompt(st.session_state.goal_setting, st.session_state.interest_area)}]
            else:
                st.session_state.messages[0]["content"] = build_system_prompt(st.session_state.goal_setting, st.session_state.interest_area)

            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                with st.spinner("AI가 생각을 정리하고 있습니다..."):
                    st.session_state.messages, ai_response = chat(prompt, st.session_state.messages, client)
                    st.write(ai_response)

            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

    st.write("")
    if st.button("💡 Insight 추출", type="secondary", use_container_width=False, key="insight_button"):
        if not st.session_state.book_info.get("title", "").strip():
            st.warning("⚠️ 인사이트를 추출하기 전에 책 제목을 먼저 입력해 주세요!")
        elif len(st.session_state.chat_history) < 2:
            st.warning("⚠️ 책에 대한 대화가 최소 한 번 이상 오고 간 뒤에 추출이 가능합니다.")
        else:
            st.session_state.step = 2
            st.rerun()
