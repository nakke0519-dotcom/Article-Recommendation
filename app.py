import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="영문 학술지 집필 AI 어시스턴트", layout="centered")

# 🔑 Streamlit Secrets에서 선생님의 개인 API 키를 불러옵니다.
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 타이틀 및 하단 설명
st.title("📚 영문 학술지 집필 AI 어시스턴트")
st.write("관심 분야와 영어 등급을 입력하면, 적절한 수준의 영문 아티클을 추천해 드립니다.")

# 학생 입력 폼
major = st.text_input("희망 분야 / 전공 / 진로", placeholder="예: 생명공학, 컴퓨터공학, 경영학, 체육 등")
details = st.text_area("관심 있는 구체적 내용", placeholder="예: 유전자 가위 기술의 윤리적 문제, 인공지능과 저작권, 마케팅 심리학 등")
grade = st.selectbox("2학년 영어 모의고사 평균 등급", ["1~2등급", "3~4등급", "5등급 이하"])

if st.button("추천 자료 검색하기"):
    if not major or not details:
        st.warning("희망 분야와 관심 내용을 모두 입력해 주세요.")
    else:
        with st.spinner("학생의 독해 수준과 진로에 딱 맞는 탐구 주제 및 풍부한 학술 정보를 분석 중입니다..."):
            
            difficulty_guide = {
                "1~2등급": """
                    - 수준: 고교 영어 수능/모의고사 1등급 수준 ~ 청소년/교양 과학·시사 아티클 수준
                    - 추천 매체 예시: Science News Explores, Live Science, BBC Science Focus, The Conversation
                    - 문장 구조가 다소 복잡하더라도 구문 분석을 통해 고2 최상위권 학생이 깊이 있게 다룰 수 있는 수준
                """,
                "3~4등급": """
                    - 수준: 고등학교 영어 II 교과서 ~ 모의고사 3~4등급 수준 (지문 길이 300~500단어 내외)
                    - 추천 매체 예시: VOA Learning English, Wonderopolis, Smithsonian Magazine for Kids, Breaking News English (Level 4-5)
                    - 전문 용어는 적고, 학생들이 맥락을 파악하며 독해 및 탐구할 수 있는 글
                """,
                "5등급 이하": """
                    - 수준: 고등학교 영어 I 교과서 ~ 중학교 성인/청소년 기초 뉴스 수준
                    - 추천 매체 예시: Breaking News English (Level 2-3), News in Levels (Level 2), Simple English Wikipedia
                    - 쉬운 단어로 구성되어 있고 문장이 짧아 영어에 자신감이 없는 학생도 도전할 수 있는 글
                """
            }
            
            prompt = f"""
            너는 대한민국 고등학교 2학년 학생들의 영어 수행평가 및 영문 학술지 집필을 돕는 전문 탐구 멘토야.
            불확실한 인터넷 URL 링크를 제공하는 대신, 실제로 유용한 학술·시사 아티클 주제 3가지를 선정하고, 학생이 깊이 있는 수행평가 보고서를 작성할 수 있도록 '풍부한 탐구 정보'와 '다양한 작성 아이디어'를 대폭 확대하여 제공해줘.

            [학생 정보]
            - 희망 진로: {major}
            - 세부 관심 내용: {details}
            - 영어 독해 수준: {grade}

            [난이도 설정 지침]
            {difficulty_guide[grade]}
            ※ 주의: 실제 학술 논문 원문(Abstract 포함)이나 전문 학술지(Nature, Science 등)는 고등학생에게 너무 어려우므로 절대로 추천하지 마. 대중적이고 직관적인 과학/시사/교양 아티클 수준으로 다룰 것.

            [응답 양식]
            각 추천 자료마다 아래 형식에 정확히 맞추어 한국어로 풍부하게 작성해줘:

            ### 📄 추천 1. [자료 영문 정확한 풀제목] ([한글 번역 제목])
            - **추천 매체/출처**: (예: Science News Explores, VOA Learning English 등)
            - **이 아티클을 추천하는 이유**: (학생의 진로 및 관심사와 어떻게 결합되는지 2줄 설명)
            - **핵심 정보 및 개념 요약**: (기사에서 다루는 핵심 학술 개념, 사례, 현황 등을 4~5줄로 상세히 설명)
            - **💡 풍부한 탐구 및 영문 학술지 집필 아이디어 (5가지)**:
              1) [원인 분석형] (이 주제와 관련하여 영문 보고서에서 다룰 만한 세부 질문)
              2) [비교/대조형] (서로 다른 관점이나 사례를 비교 분석할 수 있는 질문)
              3) [윤리/사회적 영향형] (사회적 문제나 윤리적 이슈와 연계한 탐구 질문)
              4) [적용/해결책 제안형] (실생활이나 미래 기술에 적용할 수 있는 해결책 탐구 질문)
              5) [영문 결론 작성 팁] (학생이 영문 학술지를 마무리할 때 강조하면 좋은 핵심 키워드 및 표현)
            - **추천 검색 키워드**: (학생이 구글이나 사전에서 직접 검색해볼 때 쓸 수 있는 영문 키워드 조합 2~3개)
            """

            try:
                model = genai.GenerativeModel('gemini-3.8-flash')
                response = model.generate_content(prompt)
                
                st.success("학생의 영문 학술지 집필을 위한 맞춤형 탐구 주제와 정보가 준비되었습니다!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
