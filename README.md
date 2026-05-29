## Conbook

Conbook은 대화 내용을 저장하고, 그 안에서 insight를 뽑고, 마지막에 화면으로 보여주는 프로젝트입니다.

이 프로젝트의 목표는 크게 3가지입니다.

1. 대화 내용을 저장한다.
2. 대화에서 insight를 추출한다.
3. 결과를 시각화한다.

### 실행

```bash
uv run streamlit run streamlit_app.py
```

기본적으로 [result4.json](result4.json)을 읽어 보여주며, 파일 업로드나 JSON 직접 입력으로도 확인할 수 있습니다.

### 문서

구조와 데이터 흐름은 [docs/architecture.md](docs/architecture.md)를 참고하세요.
