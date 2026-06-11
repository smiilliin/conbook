import streamlit as st

from modules.chat_client import chat
from modules.prompt import build_system_prompt
from modules.components.actions import ACTION_PROMPTS


def render_chat(client) -> None:
    if st.session_state.book_info.get("title"):
        book_title = st.session_state.book_info["title"]
        st.markdown(f"## 💬 *{book_title}* 에 대한 대화")
        if st.session_state.chat_ready:
            st.caption("어떤 생각이나 느낌도 좋아요.")
    else:
        st.warning("🚨 책 정보가 없습니다. 먼저 책 정보 입력 페이지로 돌아가 주세요.")

    if st.session_state.messages and st.session_state.messages[0].get("role") == "system":
        st.session_state.messages[0]["content"] = build_system_prompt(
            st.session_state.goal_setting,
            st.session_state.interest_area,
        )

    if not st.session_state.chat_history:
        st.info("😌 새로운 대화를 시작하려면 아래 입력창에 메시지를 입력해 주세요.")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if st.session_state.chat_ready:
        if prompt := st.chat_input("책에 대한 생각이나 느낌을 자유롭게 입력하세요..."):
            if not st.session_state.messages or st.session_state.messages[0].get("role") != "system":
                st.session_state.messages = [
                    {"role": "system", "content": build_system_prompt(st.session_state.goal_setting, st.session_state.interest_area)}
                ]
            else:
                st.session_state.messages[0]["content"] = build_system_prompt(
                    st.session_state.goal_setting,
                    st.session_state.interest_area,
                )

            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                with st.spinner("AI가 생각을 정리하고 있습니다..."):
                    st.session_state.messages, ai_response = chat(prompt, st.session_state.messages, client)
                    st.write(ai_response)

            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

    st.write("")

    actions = [
        "📑 줄거리 정리",
        "💡 깊이 있는 해석",
        "🗣️ 토론하기",
        "✍🏻 독후감 작성",
        "🚀 인사이트 추출",
    ]
    
    action_steps = {
        "📑 줄거리 정리": 3,
        "💡 깊이 있는 해석": 4,
        "🗣️ 토론하기": 5,
        "✍🏻 독후감 작성": 6,
        "🚀 인사이트 추출": 2,
    }
    
    action_keys = {
        "📑 줄거리 정리": "summary",
        "💡 깊이 있는 해석": "analysis",
        "🗣️ 토론하기": "discussion",
        "✍🏻 독후감 작성": "review",
        "🚀 인사이트 추출": "insight",
    }
    
    for idx, label in enumerate(actions):
        if st.button(label, key=f"action_{idx}", use_container_width=False):
            if not st.session_state.book_info.get("title", "").strip():
                st.warning("🚨 먼저 책 제목을 입력해 주세요!")
            elif len(st.session_state.chat_history) < 2:
                st.warning("🚨 책에 대한 대화가 최소 한 번 이상 오고 간 뒤에 사용이 가능합니다.")
            else:
                with st.spinner(f"{label} 생성 중입니다..."):
                    prompt = ACTION_PROMPTS[label]
                    action_messages = list(st.session_state.messages)
                    action_messages.append({"role": "user", "content": prompt})
                    _, action_result = chat(prompt, action_messages, client)
                                
                    if "action_result" not in st.session_state:
                        st.session_state.action_result = {}
                    st.session_state.action_result[action_keys[label]] = action_result
                    st.session_state.step = action_steps[label]
                    st.rerun()
