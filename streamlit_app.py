import streamlit as st
from openai import OpenAI

# 시스템 프롬프트 정의
SYSTEM_PROMPT = """
당신은 경희대학교 입학처의 입시 안내 챗봇입니다.
오직 경희대학교 2026~2028학년도 대입전형에 관한 질문에만 답변하세요.

답변 범위:
- 수시/정시 모집 전형 종류 및 일정
- 지원 자격 및 전형 방법
- 학과별 모집 인원
- 제출 서류 및 면접 안내
- 수능 최저학력기준
- 장학금 및 등록금 관련 입시 정보

반드시 지켜야 할 규칙:
1. 위 범위를 벗어난 질문(예: 타 대학 입시, 일반 상식, 취업 등)에는 답변하지 말고, "저는 경희대학교 2026~2028학년도 대입전형 관련 질문만 답변할 수 있습니다 🙏"라고 안내하세요.
2. 정확하지 않은 정보는 추측하지 말고, "정확한 정보는 경희대학교 입학처(https://iphak.khu.ac.kr)에서 확인해 주세요 📌"라고 안내하세요.
3. 항상 한국어로 답변하세요.
4. 모든 답변에 이모티콘을 자연스럽게 활용하세요. 아래 가이드를 참고하세요.
   - 📋 전형 종류나 목록을 설명할 때
   - 📅 날짜나 일정을 안내할 때
   - ✅ 조건이나 자격 요건을 나열할 때
   - 📎 서류나 제출물을 안내할 때
   - 💡 팁이나 중요한 정보를 강조할 때
   - 🎓 합격, 전형 결과 관련 내용
   - ⚠️ 주의사항을 안내할 때
   - 👋 인사말이나 마무리 멘트
"""

# 제목 및 설명
st.title("🎓 경희대학교 입시 안내 챗봇")
st.write(
    "경희대학교 **2026~2028학년도 대입전형**에 관한 질문에 답변해 드립니다. "
    "입시 관련 궁금한 점을 자유롭게 물어보세요!"
)
st.caption("※ 정확한 최신 정보는 [경희대학교 입학처](https://iphak.khu.ac.kr)에서 반드시 확인하세요.")

# OpenAI API 키 입력
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("OpenAI API 키를 입력하면 챗봇을 사용할 수 있습니다.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 대화 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("경희대 입시에 대해 궁금한 점을 물어보세요!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # API 호출 시 시스템 프롬프트 포함
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            ],
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
