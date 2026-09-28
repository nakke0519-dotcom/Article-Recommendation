import streamlit as st
import google.generativeai as genai
import time

# Streamlit Secrets에서 API 키 불러오기
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("📚 영문 학술지 집필 AI 어시스턴트")
st.write("진로 및 관심사와 영어 등급을 입력하면, 적절한 수준의 영문 자료를 추천해 드립니다.")

# 학생 입력 폼
major = st.text_input("희망 분야 / 전공 / 진로", placeholder="예: 생명공학, 컴퓨터공학, 경영학, 미디어학 등")
details = st.text_area("관심 있는 구체적 내용", placeholder="예: 유전자 가위 기술의 윤리적 문제, 인공지능과 저작권, 마케팅 심리학 등")
grade = st.selectbox("2학년 영어 모의고사 평균 등급", ["1~2등급", "3~4등급", "5등급 이하"])

if st.button("추천 자료 검색하기"):
    if not major or not details:
        st.warning("희망 분야와 관심 내용을 모두 입력해 주세요.")
    else:
        with st.spinner("학생의 실제 영어 독해 수준에 맞는 최적의 자료를 찾고 있습니다..."):
            
            # 고2 현실적 수준에 맞춘 난이도 지침
            difficulty_guide = {
                "1~2등급": """
                    - 수준: 고교 영어 수능/모의고사 1등급 수준 ~ 청소년/교양 과학·시사 아티클 수준
                    - 추천 출처 예시: Science News Explores, Live Science, BBC Science Focus, The Conversation
                    - 문장 구조가 다소 복잡하더라도 구문 분석과 사전 검색을 통해 고2 최상위권 학생이 충분히 읽어낼 수 있는 정도의 글
                """,
                "3~4등급": """
                    - 수준: 고등학교 영어 II 교과서 ~ 모의고사 3~4등급 수준 (지문 길이 300~500단어 내외)
                    - 추천 출처 예시: VOA Learning English, Wonderopolis, Smithsonian Magazine for Kids, Breaking News English (Level 4-5)
                    - 전문 용어는 적고, 학생들이 구글 번역기나 사전의 도움을 받아 맥락을 파악하며 읽을 수 있는 글
                """,
                "5등급 이하": """
                    - 수준: 고등학교 영어 I 교과서 ~ 중학교 성인/청소년 기초 뉴스 수준
                    - 추천 출처 예시: Breaking News English (Level 2-3), News in Levels (Level 2), Simple English Wikipedia
                    - 쉬운 단어로 구성되어 있고 문장이 짧아 영어에 자신감이 없는 학생도 도전할 수 있는 글
                """
            }
            
            prompt = f"""
            너는 대한민국 고등학교 2학년 학생들의 영어 수행평가를 돕는 친절한 영어 교육 전문가이자 탐구 멘토야.
            학생이 스스로 읽고 요약/분석하여 '자신만의 영문 학술지'를 집필할 수 있도록, 아래 학생의 조건에 꼭 맞는 영문 아티클 및 학술 자료 3가지를 추천해줘.

            [학생 정보]
            - 희망 진로: {major}
            - 세부 관심 내용: {details}
            - 영어 독해 수준: {grade}

            [난이도 설정 지침 - 매우 중요!]
            {difficulty_guide[grade]}
            ※ 주의: 실제 학술 논문 원문(Abstract 포함)이나 전문 학술지(Nature, Science 등)는 고등학생에게 너무 어려우므로 절대로 추천하지 마. 학생들이 사전의 도움을 받아 직접 독해할 수 있는 청소년/대중용 과학·시사 아티클 위주로 추천할 것.

            [응답 양식]
            각 추천 자료마다 아래 형식에 정확히 맞추어 한국어로 친절하게 작성해줘:

            ### 📄 추천 1. [자료 영문 제목] ([한글 번역 제목])
            - **추천 매체/출처**: (예: Science News Explores, VOA Learning English 등)
            - **이 자료를 추천하는 이유**: (학생의 관심사와 어떻게 연결되는지 2줄 설명)
            - **주요 내용 요약**: (아티클에서 다루는 핵심 내용 3~4줄 요약)
            - **탐구 및 집필 아이디어**:
              1) (학생이 보고서나 영문 학술지를 쓸 때 다룰 만한 핵심 질문 또는 탐구 주제 1)
              2) (학생이 보고서나 영문 학술지를 쓸 때 다룰 만한 핵심 질문 또는 탐구 주제 2)
              3) (학생이 보고서나 영문 학술지를 쓸 때 다룰 만한 핵심 질문 또는 탐구 주제 3)
            - **원문 바로가기 (링크)**: (해당 아티클을 바로 읽을 수 있는 실제 웹 URL)
            """

            # 사용자가 설정하신 gemini-3.8-flash 모델 사용
            model = genai.GenerativeModel('gemini-3.8-flash')
            
            # 분당 5회 제한(429 오류)을 방지하기 위한 자동 재시도 루프
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = model.generate_content(prompt)
                    st.success("학생 수준에 맞춘 추천 자료가 준비되었습니다!")
                    st.markdown(response.text)
                    break
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "Quota" in error_msg or "ResourceExhausted" in error_msg:
                        if attempt < max_retries - 1:
                            st.info("요청이 몰려 10초 후 자동으로 재시도합니다. 잠시만 기다려 주세요...")
                            time.sleep(10)
                        else:
                            st.error("Google API 분당 사용 한도에 도달했습니다. 약 30초 후 다시 '추천 자료 검색하기' 버튼을 눌러주세요.")
                    else:
                        st.error(f"오류가 발생했습니다: {e}")
                        break
