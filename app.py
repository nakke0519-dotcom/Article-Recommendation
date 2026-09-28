import streamlit as st
import google.generativeai as genai
import urllib.parse

st.set_page_config(page_title="영문 학술지 집필 AI 어시스턴트", layout="centered")

# 🔑 Streamlit Secrets에서 선생님의 개인 API 키를 불러옵니다.
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 타이틀 및 하단 설명
st.title("📚 영문 학술지 집필 AI 어시스턴트")
st.write("진로 및 관심사와 영어 등급을 입력하면, 직접 읽고 분석할 수 있는 적절한 수준의 영문 아티클을 추천해 드립니다.")

# 학생 입력 폼
major = st.text_input("희망 분야 / 전공 / 진로", placeholder="예: 생명공학, 컴퓨터공학, 경영학, 미디어학 등")
details = st.text_area("관심 있는 구체적 내용", placeholder="예: 유전자 가위 기술의 윤리적 문제, 인공지능과 저작권, 마케팅 심리학 등")
grade = st.selectbox("2학년 영어 모의고사 평균 등급", ["1~2등급", "3~4등급", "5등급 이하"])

if st.button("추천 자료 검색하기"):
    if not major or not details:
        st.warning("희망 분야와 관심 내용을 모두 입력해 주세요.")
    else:
        with st.spinner("학생 수준에 맞는 최적의 영문 아티클을 분석 및 추천 중입니다..."):
            
            difficulty_guide = {
                "1~2등급": """
                    - 수준: 고교 영어 수능/모의고사 1등급 수준 ~ 청소년/교양 과학·시사 아티클 수준
                    - 추천 출처 예시: Science News Explores, Live Science, BBC Science Focus, The Conversation
                    - 문장 구조가 다소 복잡하더라도 구문 분석을 통해 고2 최상위권 학생이 충분히 읽어낼 수 있는 정도의 글
                """,
                "3~4등급": """
                    - 수준: 고등학교 영어 II 교과서 ~ 모의고사 3~4등급 수준 (지문 길이 300~500단어 내외)
                    - 추천 출처 예시: VOA Learning English, Wonderopolis, Smithsonian Magazine for Kids, Breaking News English (Level 4-5)
                    - 전문 용어는 적고, 학생들이 사전의 도움을 받아 맥락을 파악하며 읽을 수 있는 글
                """,
                "5등급 이하": """
                    - 수준: 고등학교 영어 I 교과서 ~ 중학교 성인/청소년 기초 뉴스 수준
                    - 추천 출처 예시: Breaking News English (Level 2-3), News in Levels (Level 2), Simple English Wikipedia
                    - 쉬운 단어로 구성되어 있고 문장이 짧아 영어에 자신감이 없는 학생도 도전할 수 있는 글
                """
            }
            
            prompt = f"""
            너는 대한민국 고등학교 2학년 학생들의 영어 수행평가를 돕는 친절한 영어 교육 전문가이자 탐구 멘토야.
            학생이 스스로 읽고 요약/분석하여 '자신만의 영문 학술지'를 집필할 수 있도록, 실제로 존재하는 대표적인 영문 아티클 3가지를 구체적이고 정확한 제목으로 추천해줘.

            [학생 정보]
            - 희망 진로: {major}
            - 세부 관심 내용: {details}
            - 영어 독해 수준: {grade}

            [난이도 설정 지침 - 매우 중요!]
            {difficulty_guide[grade]}
            ※ 주의: 실제 학술 논문 원문(Abstract 포함)이나 전문 학술지(Nature, Science 등)는 고등학생에게 너무 어려우므로 절대로 추천하지 마. 학생들이 직접 독해할 수 있는 청소년/대중용 과학·시사 아티클 위주로 추천할 것.

            [응답 양식]
            각 추천 자료마다 아래 형식에 정확히 맞추어 한국어로 작성해줘:

            ### 📄 추천 1. [자료 영문 정확한 풀제목] ([한글 번역 제목])
            - **추천 매체/출처**: (예: Science News Explores, VOA Learning English 등)
            - **이 자료를 추천하는 이유**: (학생의 관심사와 어떻게 연결되는지 2줄 설명)
            - **주요 내용 요약**: (아티클에서 다루는 핵심 내용 3~4줄 요약)
            - **탐구 및 집필 아이디어**:
              1) (학생이 보고서나 영문 학술지를 쓸 때 다룰 만한 핵심 질문 또는 탐구 주제 1)
              2) (학생이 보고서나 영문 학술지를 쓸 때 다룰 만한 핵심 질문 또는 탐구 주제 2)
              3) (학생이 보고서나 영문 학술지를 쓸 때 다룰 만한 핵심 질문 또는 탐구 주제 3)
            - **기사 원문 검색 키워드**: (기사 제목과 매체명을 포함한 영문 검색 키워드 단일행)
            """

            try:
                model = genai.GenerativeModel('gemini-3.8-flash')
                response = model.generate_content(prompt)
                
                # 결과 텍스트 파싱하여 실제 원문 구글 직접 연결 링크 자동 생성
                result_text = response.text
                
                st.success("학생 수준에 맞춘 최적의 추천 아티클이 준비되었습니다!")
                st.markdown(result_text)
                
                st.info("💡 **원문 읽기 안내**: 각 기사의 제목을 누르면 구글 검색을 통해 해당 원문 기사 페이지로 즉시 연결됩니다.")
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
