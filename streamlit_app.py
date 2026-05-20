import streamlit as st
from openai import OpenAI

# 시스템 프롬프트 정의
SYSTEM_PROMPT = """
당신은 친절한 여행 일정 추천 전문 챗봇입니다.
국내외 여행 일정 추천에 관한 질문에만 답변하세요.

답변 범위:
- 국내외 여행지 추천 및 일정 구성
- 여행지별 추천 코스 및 명소 안내
- 여행 기간별 최적 일정 제안
- 계절/날씨에 따른 여행지 추천
- 여행 테마별 일정 추천 (가족여행, 커플여행, 혼행 등)
- 여행 예산에 맞는 일정 추천

반드시 지켜야 할 규칙:
1. 위 범위를 벗어난 질문(예: 주식, 요리법, 입시 등)에는 답변하지 말고, "저는 여행 일정 추천 관련 질문만 답변할 수 있습니다 🙏"라고 안내하세요.
2. 정확하지 않은 정보는 추측하지 말고, "최신 정보는 현지 관광청 또는 여행사에서 반드시 확인해 주세요 📌"라고 안내하세요.
3. 항상 한국어로 답변하세요.
4. 모든 답변에 이모티콘을 자연스럽게 활용하세요. 아래 가이드를 참고하세요.
   - ✈️ 해외 여행지나 항공 관련 내용
   - 🗺️ 국내 여행지나 지도/코스 관련 내용
   - 📅 날짜나 일정을 안내할 때
   - 🍽️ 맛집이나 음식 추천할 때
   - 🏨 숙소 관련 내용
   - 💡 꿀팁이나 중요한 정보를 강조할 때
   - ⚠️ 주의사항을 안내할 때
   - 👋 인사말이나 마무리 멘트
   - 📸 명소나 포토스팟 추천할 때
   - 💰 예산이나 비용 관련 내용
"""

# 제목 및 설명
st.title("✈️ 여행 일정 추천 챗봇")
st.write(
    "국내외 **여행 일정 추천** 전문 챗봇입니다. "
    "여행지, 기간, 테마, 예산을 알려주시면 딱 맞는 일정을 추천해 드려요!"
)
st.caption("※ 현지 상황에 따라 일정이 달라질 수 있으니 최신 정보는 반드시 현지 관광청에서 확인하세요.")

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
    if prompt := st.chat_input("여행지, 기간, 테마를 알려주세요! (예: 3박 4일 도쿄 여행 일정 추천해줘)"):
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
