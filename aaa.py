sample_messages = [
    {
        "role": "user",
        "content": "인간실격의 주인공이 너무 불쾌해 왜 그런 느낌을 받았을까?",
    },
    {
        "role": "assistant",
        "content": "주인공 요코타는 자아정체감이 흔들리고, 사회적 기대에 부응하지 못해 내면에서 자책과 불안이 끊이지요. 이런 갈등이 독자에게 불편한 감정을 불러일으키는 것 같아요. 혹시 그런 불쾌함이 개인적으로 경험한 사회적 압박과 비슷하다고 느끼시나요?",
    },
    {
        "role": "user",
        "content": "나는 사회적 압박에 부응하지 못하는 점보다는 그가 변화하지 않는 시스템 내에서 고민한다는 점을 지적하고 싶었어",
    },
    {
        "role": "assistant",
        "content": "아, 그 점이야말로 요코타가 놓인 ‘제국적 체계’ 속에서 가라앉는 한 점이라 생각됩니다. 그는 변화를 주지 않아도 되는 ‘먹이잽살’처럼 자신을 정부와 가족, 직장 같은 체제에 빗대어 방치했죠. 이런 맥락에서 불쾌함이 아니라 무시와 부정당해지는 한 존재?가 그런 감정을 일으킨 것 같은데, 이 ‘체제 안에서의 고민’이 오늘날 우리에게 특정한 연결고리를 제시한다고 보시나요?",
    },
    {"role": "user", "content": "제국적 체계가 뭐야? 좀더 자세히 설명해줘"},
    {
        "role": "assistant",
        "content": "제국적 체계는 ‘높은 권위와 권력 구조가 사회 전반을 지배하는 체제’를 말해요. 요코타가 서민 같은 존재로, 고정된 직장·결혼·자녀 여부 같은 “여기에 붙어야 한다”는 규칙 안에서 딜레마를 겪으며, 개인의 욕망보다 ‘체제’가 우선시되는 사회를 묘사한 거죠. 이 구조가 변화를 금지하고, 개인의 성장을 억제함으로써 요코타는 끊임없는 좌절을 맛보는 겁니다.",
    },
]

def messages_to_text(messages, exclude_system=True):
    """메시지 리스트를 텍스트로 변환"""
    parts = []
    entities = []
    for i, m in enumerate(messages):
        entity = f"uuid_s{i:03d}"
        if exclude_system and m.get("role") == "system":
            continue
        role = m.get("role", "")
        content = m.get("content", "")
        parts.append(f"entity: {entity}, {role}: {content}")
        entities.append(entity)
    return "\n".join(parts), entities