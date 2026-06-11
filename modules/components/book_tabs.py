import time

import streamlit as st

MOCK_INSIGHT = {
    "summary": "알베르 카뮈의 '이방인'을 통해 주인공 뫼르소의 행동 양식과 사회적 관습의 충돌을 분석하고, 현대 사회에서 개인이 느끼는 소외감과 실존주의적 고뇌에 대해 심도 깊은 대화를 나누었습니다.",
    "interests": ["실존주의", "도덕 감수성 교육", "부조리", "사회적 관 관습"],
    "directions": [
        {
            "keyword": "실존주의",
            "summary": "삶의 무의미함 속에서 개인의 주체적 선택이 갖는 의미 추구",
            "flow": "사용자가 뫼르소의 태도에 공감하며 실존주의적 가치관에 대해 질문함.",
        },
        {
            "keyword": "도덕 감수성 교육",
            "summary": "사회가 요구하는 감정의 형태와 개인의 진실된 감정 간의 간극 이해",
            "flow": "사회의 관습적 슬픔 요구에 대한 비판적 시각 공유.",
        },
        {
            "keyword": "부조리",
            "summary": "합리성을 요구하는 인간과 불합리한 세계 사이의 충돌",
            "flow": "재판 과정에서 본질과 어긋나는 논쟁을 벌이는 부분에 대한 고찰.",
        },
    ],
    "timeline": [
        {
            "entity": "User",
            "description": "책의 첫 문장('오늘 엄마가 죽었다')이 준 충격과 뫼르소의 덤덤한 태도에 대해 언급함.",
        },
        {
            "entity": "AI",
            "description": "뫼르소의 태도를 '사회적 거짓말을 거부하는 인간'으로 해석하는 관점을 제시 (질문 방향: 철학적 접근).",
        },
        {
            "entity": "User",
            "description": "사회가 정해놓은 도덕적 잣대와 감정 표현의 의무에 대해 부조리함을 느낀다고 답변함.",
        },
        {
            "entity": "AI",
            "description": "이를 '도덕 감수성' 및 '실존주의' 맥락으로 확장하여 최종 인사이트 도출 궤도 안착.",
        },
    ],
}


def render_insight_page() -> None:
    book_title = st.session_state.book_info.get("title", "책 제목")
    book_author = st.session_state.book_info.get("author", "저자명")
    st.title(f"{book_title} · {book_author}")
    st.subheader("🚀 인사이트 추출")

    with st.status("인사이트 분석 파이프라인 가동 중...", expanded=True) as status:
        st.write("🔄 1단계 대화 기록 데이터 전처리 중 (a_messages.json)...")
        time.sleep(1.2)
        st.write("🧠 LLM 백엔드 로직 구동 중 (Summary, Interest, Direction 추출)...")
        time.sleep(1.5)
        st.write("🔍 `validate_insight` 함수를 통한 추출 JSON 스키마 구조 검증 중...")
        time.sleep(1.0)
        status.update(label="✅ 분석 및 JSON 구조 검증 완료!", state="complete", expanded=False)

    st.write("---")
    st.subheader("📝 핵심 인사이트")
    
    insight = st.session_state.get("action_result", {}).get("insight", "")
    if insight:
        st.markdown(insight)
    else:
        with st.expander("📌 이번 대화의 핵심 요약 보기", expanded=True):
            st.markdown(f"### {MOCK_INSIGHT['summary']}")

        st.write("")
        st.subheader("🏷️ 추출된 관심사 태그 (Interests)")
        selected_tags = st.multiselect(
            "필터링하거나 포커싱할 키워드를 선택하세요.",
            options=MOCK_INSIGHT["interests"],
            default=MOCK_INSIGHT["interests"],
        )

        st.write("")
        st.subheader("🗂️ 관심사별 상세 카드 (Directions)")
        cols = st.columns(len(MOCK_INSIGHT["directions"]))
        for idx, card in enumerate(MOCK_INSIGHT["directions"]):
            if card["keyword"] in selected_tags:
                with cols[idx]:
                    with st.expander(f"⭐ {card['keyword']}", expanded=True):
                        st.markdown(f"**방향성 요약:**\n{card['summary']}")
                        st.markdown(f"**발화 흐름 분석:**\n*{card['flow']}*")

    st.write("")
    if st.button("◀️ 대화로 돌아가기", type="secondary", use_container_width=True):
        st.session_state.step = 1
        st.rerun()
