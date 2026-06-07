import time

import pandas as pd
import streamlit as st

from modules.chat_client import chat
from modules.history import load_history_records
from modules.prompt import build_system_prompt

DEFAULT_PAST_SESSIONS = [
    {"title": "이방인", "author": "알베르 카뮈", "status": "다 읽음"},
    {"title": "사피엔스", "author": "유발 하라리", "status": "읽는 중"},
    {"title": "데미안", "author": "헤르만 헤세", "status": "다 읽음"},
]

MOCK_INSIGHT = {
    "summary": "알베르 카뮈의 '이방인'을 통해 주인공 뫼르소의 행동 양식과 사회적 관습의 충돌을 분석하고, 현대 사회에서 개인이 느끼는 소외감과 실존주의적 고뇌에 대해 심도 깊은 대화를 나누었습니다.",
    "interests": ["실존주의", "도덕 감수성 교육", "부조리", "사회적 관 관습"],
    "directions": [
        {"keyword": "실존주의", "summary": "삶의 무의미함 속에서 개인의 주체적 선택이 갖는 의미 추구", "flow": "사용자가 뫼르소의 태도에 공감하며 실존주의적 가치관에 대해 질문함."},
        {"keyword": "도덕 감수성 교육", "summary": "사회가 요구하는 감정의 형태와 개인의 진실된 감정 간의 간극 이해", "flow": "사회의 관습적 슬픔 요구에 대한 비판적 시각 공유."},
        {"keyword": "부조리", "summary": "합리성을 요구하는 인간과 불합리한 세계 사이의 충돌", "flow": "재판 과정에서 본질과 어긋나는 논쟁을 벌이는 부분에 대한 고찰."},
    ],
    "timeline": [
        {"entity": "User", "description": "책의 첫 문장('오늘 엄마가 죽었다')이 준 충격과 뫼르소의 덤덤한 태도에 대해 언급함."},
        {"entity": "AI", "description": "뫼르소의 태도를 '사회적 거짓말을 거부하는 인간'으로 해석하는 관점을 제시 (질문 방향: 철학적 접근)."},
        {"entity": "User", "description": "사회가 정해놓은 도덕적 잣대와 감정 표현의 의무에 대해 부조리함을 느낀다고 답변함."},
        {"entity": "AI", "description": "이를 '도덕 감수성' 및 '실존주의' 맥락으로 확장하여 최종 인사이트 도출 궤도 안착."},
    ],
}


def set_page_config():
    st.set_page_config(page_title="Conbook : 나만의 독서 기록장", page_icon="📚", layout="wide")


def init_session_state():
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "book_info" not in st.session_state:
        st.session_state.book_info = {"title": "", "author": "", "status": "읽는 중"}
    if "goal_setting" not in st.session_state:
        st.session_state.goal_setting = "선택(미설정)"
    if "interest_area" not in st.session_state:
        st.session_state.interest_area = ["선택(미설정)"]
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": build_system_prompt(st.session_state.goal_setting, st.session_state.interest_area)}]


def render_sidebar():
    with st.sidebar:
        st.title("⚙️ Conbook 설정")
        st.info("안내: 이 UI는 독서 대화 기록과 인사이트 추출을 돕기 위한 프로토타입입니다. 필요한 정보만 입력하세요.")

        st.subheader("🔮 Purpose / Interest 설정")
        st.session_state.goal_setting = st.selectbox(
            "Purpose",
            ["선택(미설정)", "정보 습득", "의사 결정", "자기 계발", "취미 독서"],
            index=["선택(미설정)", "정보 습득", "의사 결정", "자기 계발", "취미 독서"].index(st.session_state.goal_setting),
        )
        st.session_state.interest_area = st.multiselect(
            "Interest",
            ["선택(미설정)", "인문학", "사회과학", "자연과학", "공학", "의약학", "예술체육", "복합학"],
            default=st.session_state.interest_area,
        )

        st.markdown("<div style='height:10px; border-radius:8px; background:linear-gradient(90deg,#eef2ff,#f0fdf4); padding:8px; margin:10px 0;'></div>", unsafe_allow_html=True)

        st.subheader("📜 History")
        for s in DEFAULT_PAST_SESSIONS:
            name = f"{s['title']}_{s['author']}_{s['status']}"
            st.markdown(
                f"<div style='padding:10px; border:1px solid #e6eef8; border-radius:12px; margin-bottom:8px; background:#ffffff;'>"
                f"<strong>{name}</strong><br>"
                f"<span style='color:#556172; font-size:13px;'>이전 독서 기록을 참고할 수 있는 예시 목록입니다.</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.write("---")


def render_step1(client):
    st.title("Conbook : 나만의 독서 기록장 — 1단계: 대화 기록")
    st.info("환영합니다! 이 공간에서 책과 관련된 생각을 AI와 나누고, 인사이트를 추출할 수 있습니다.")
    st.caption("사용자가 AI와 책 이야기를 나누는 화면입니다. 오픈루터(OpenRouter) 연동 컨텍스트가 자동으로 반영됩니다.")

    st.subheader("📖 책 정보 입력")
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        book_title = st.text_input("책 제목 (필수)", value=st.session_state.book_info["title"], placeholder="예: 이방인")
    with c2:
        book_author = st.text_input("저자명 (선택)", value=st.session_state.book_info["author"], placeholder="예: 알베르 카뮈")
    with c3:
        book_status = st.radio(
            "읽기 상태",
            ["읽는 중", "다 읽음", "n회차 읽는 중"],
            index=["읽는 중", "다 읽음", "n회차 읽는 중"].index(st.session_state.book_info["status"]),
            horizontal=False,
        )
        st.markdown(
            f"<div style='display:inline-block; padding:6px 10px; background:#eef2ff; border-radius:12px; margin-top:10px;'><strong>{book_status}</strong></div>",
            unsafe_allow_html=True,
        )

    st.session_state.book_info = {"title": book_title, "author": book_author, "status": book_status}

    if st.session_state.messages and st.session_state.messages[0].get("role") == "system":
        st.session_state.messages[0]["content"] = build_system_prompt(st.session_state.goal_setting, st.session_state.interest_area)

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

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
    if st.button("Insight 추출 🚀", use_container_width=True):
        if not book_title:
            st.warning("⚠️ 인사이트를 추출하기 전에 책 제목을 먼저 입력해 주세요!")
        elif len(st.session_state.chat_history) < 2:
            st.warning("⚠️ 책에 대한 대화가 최소 한 번 이상 오고 간 뒤에 추출이 가능합니다.")
        else:
            st.session_state.step = 2
            st.rerun()


def render_step2():
    st.title("🚀 Conbook : 나만의 독서 기록장 — 2단계: Insight 추출")
    st.caption("노트북(main.ipynb) 백엔드 파이프라인이 작동하며 LLM 분석 및 JSON 검증을 수행하는 단계입니다.")

    with st.status("인사이트 분석 파이프라인 가동 중...", expanded=True) as status:
        st.write("🔄 1단계 대화 기록 데이터 전처리 중 (a_messages.json)...")
        time.sleep(1.2)
        st.write("🧠 LLM 백엔드 로직 구동 중 (Summary, Interest, Direction 추출)...")
        time.sleep(1.5)
        st.write("🔍 `validate_insight` 함수를 통한 추출 JSON 스키마 구조 검증 중...")
        time.sleep(1.0)
        status.update(label="✅ 분석 및 JSON 구조 검증 완료!", state="complete", expanded=False)

    st.write("---")
    st.subheader("📝 전체 요약 (Summary)")
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

    st.write("---")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("🔄 재분석 (파이프라인 재실행)"):
            st.toast("파이프라인을 다시 실행합니다.")
            st.rerun()
    with col_b2:
        if st.button("📊 시각화 및 리마인더 확인하러 가기 ➡️", type="primary"):
            st.session_state.step = 3
            st.rerun()


def render_step3():
    st.title("🌐 Conbook : 나만의 독서 기록장 — 3단계: 시각화 및 리마인더")
    st.caption("지식의 확장 방향성 시각화와 맥락 기반 복기를 지원하는 화면입니다.")

    tab1, tab2 = st.tabs(["🌐 생각의 지도", "⏰ 대화 리마인더"])

    with tab1:
        st.subheader("🗺️ 지식 확장 지형도 (네트워크 그래프)")
        st.info("💡 프로토타입 버전에서는 대화 데이터 기반 Plotly 노드-링크 구조 지형도로 시각화 요소를 대체합니다.")

        center_title = st.session_state.book_info['title'] if st.session_state.book_info['title'] else '이방인'
        soft_tags = MOCK_INSIGHT["interests"][:4]

        st.markdown(
            "<div style='padding:12px; border-radius:18px; background:linear-gradient(135deg,#eef6ff,#f7f3ff); border:1px solid #dbe4ff;'>"
            "<strong>🌿 감성적인 키워드 맵</strong><br>"
            "책의 중심축과 연결된 관심사가 잔잔하게 흐르도록 정리한 화면입니다.</div>",
            unsafe_allow_html=True,
        )

        col_left, col_right = st.columns([1.1, 1.2])
        with col_left:
            st.markdown(
                f"<div style='background:#ffffff; border-radius:18px; padding:14px; border:1px solid #e5e7eb; box-shadow: 0 6px 18px rgba(148,163,184,0.18);'>"
                f"<div style='font-size:16px; color:#4f46e5; font-weight:700;'>📚 중심 도서</div>"
                f"<div style='font-size:18px; margin-top:6px;'><strong>{center_title}</strong></div>"
                f"<div style='margin-top:8px; color:#475569;'>이번 대화의 핵심 축을 중심으로, 잔잔한 연결을 따라 생각을 넓혀가세요.</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

        with col_right:
            for tag in soft_tags:
                st.markdown(
                    f"<div style='background:linear-gradient(135deg,#f8fbff,#eefbf7); border:1px solid #dbeafe; border-radius:16px; padding:11px 12px; margin-bottom:8px;'>"
                    f"🌱 <strong>{tag}</strong><br>"
                    f"<span style='color:#475569; font-size:13px;'>책의 분위기와 생각을 잔잔하게 연결하는 키워드입니다.</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

        st.write("")
        st.info("💡 기존 대화 데이터와 관심사 키워드를 연결해 보면, 이 책이 사용자에게 어떤 감정적·지적 여백을 남겼는지 더 선명하게 보입니다.")
        st.write("🔍 **현재 연결 흐름 예시:**")
        st.code(f"[{center_title}] ➡️ [실존주의] ➡️ [도덕 감수성 교육] ➡️ [부조리 맥락 추적]")

    with tab2:
        st.subheader("⏳ 맥락 기반 대화 타임라인")
        filter_keyword = st.selectbox("🎯 특정 관심사 연결 발화만 필터링", ["전체 보기"] + MOCK_INSIGHT["interests"])
        st.write("")
        for idx, tl in enumerate(MOCK_INSIGHT["timeline"]):
            if filter_keyword != "전체 보기" and idx % 2 == 1:
                continue
            icon = "👤" if tl["entity"] == "User" else "🤖"
            st.markdown(
                f"<div style='background-color: #f0f2f6; padding: 15px; border-left: 5px solid #4f46e5; border-radius: 5px; margin-bottom: 12px;'>"
                f"<strong>{icon} {tl['entity']}_005</strong><br>"
                f"<span style='color: #31333F;'>{tl['description']}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
        st.write("---")
        with st.expander("📂 원본 구조화 데이터 보기 (result*.json)", expanded=False):
            st.json(MOCK_INSIGHT)

    st.write("---")
    if st.button("📜 과거 기록 한눈에 보기", type="primary"):
        st.session_state.step = 4
        st.rerun()

    st.write("---")
    if st.button("↩️ 새 책으로 대화 시작하기 (1단계로)"):
        st.session_state.step = 1
        st.session_state.chat_history = []
        st.session_state.book_info = {"title": "", "author": "", "status": "읽는 중"}
        st.rerun()


def render_step4():
    st.title("📜 Conbook : 나만의 독서 기록장 — 4단계: 과거 기록 한눈에 보기")
    st.caption("기존 result*.json 파일을 불러와, 여러 세션의 핵심 요약과 키워드를 한 화면에서 확인합니다.")

    records = load_history_records()
    if not records:
        st.info("현재 불러올 수 있는 과거 기록 파일이 없습니다.")
        return

    st.subheader("📊 세션 요약 카드")
    cols = st.columns(min(3, len(records)))
    for idx, rec in enumerate(records):
        with cols[idx % len(cols)]:
            st.markdown(
                f"<div style='background:linear-gradient(135deg,#f8fbff,#eefbf7); border:1px solid #dbeafe; border-radius:18px; padding:14px; margin-bottom:10px;'>"
                f"<div style='font-size:12px; color:#6366f1;'>📄 {rec['file_name']}</div>"
                f"<div style='font-size:16px; font-weight:700; margin-top:4px;'>{rec['summary'][:60]}...</div>"
                f"<div style='color:#475569; font-size:13px; margin-top:6px;'>{rec['summary'][60:140]}...</div>"
                f"<div style='margin-top:8px; color:#0f766e;'>키워드 {rec['count']}개 · {', '.join(rec['keywords'][:3])}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.write("")
    st.subheader("📈 키워드 분포")
    chart_df = pd.DataFrame(
        [{"세션": rec["file_name"], "핵심 키워드 수": rec["count"]} for rec in records]
    )
    st.bar_chart(chart_df.set_index("세션"), use_container_width=True)

    st.write("")
    st.subheader("🧭 과거 세션 상세")
    for rec in records:
        with st.expander(f"{rec['file_name']} · {rec['timestamp'][:10] if rec['timestamp'] else 'timestamp 없음'}", expanded=False):
            st.write(rec['summary'])
            st.write("핵심 키워드:", ", ".join(rec['keywords']) or "없음")
            st.write("보조 태그:", ", ".join(rec['tag_pool']) or "없음")

    st.write("---")
    col_back, col_home = st.columns(2)
    with col_back:
        if st.button("⬅️ 3단계로 돌아가기"):
            st.session_state.step = 3
            st.rerun()
    with col_home:
        if st.button("↩️ 새 책으로 시작하기"):
            st.session_state.step = 1
            st.session_state.chat_history = []
            st.session_state.book_info = {"title": "", "author": "", "status": "읽는 중"}
            st.rerun()
