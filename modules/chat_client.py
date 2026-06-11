import os

try:
    import dotenv
except ImportError:
    dotenv = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def create_client():
    if dotenv is not None:
        dotenv.load_dotenv()
    try:
        if OpenAI is None:
            return None

        return OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("API_KEY") or "",
        )
    except Exception:
        return None


def chat(user_input, messages, client=None):
    client = client or create_client()

    if not client or not client.api_key:
        return messages, (
            "현재 OpenRouter API 키가 설정되어 있지 않아, 기본 응답으로 안내합니다. "
            "환경 변수 API_KEY를 등록하면 실제 AI 대화가 연결됩니다."
        )

    messages = list(messages)
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=messages,
    )

    assistant_message = response.choices[0].message.content or ""
    messages.append({"role": "assistant", "content": assistant_message})
    return messages, assistant_message
