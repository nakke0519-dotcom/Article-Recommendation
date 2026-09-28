import streamlit as st
import google.generativeai as genai

# Streamlit Secrets에서 API 키 불러오기 (또는 직접 입력)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("📚 영문 학술지 집필 AI 어시스턴")
st.write("자신의 진로와 관심사, 평균 영어 등급을 입력하면 AI가 맞춤형 영문 학술 자료를 추천해 드립니다.")

# 학생 입력 폼
major = st.text_input("희망 분야 / 전공 / 진로", placeholder="예: 생명공학, 컴퓨터공학, 경영학 등")
details = st.text_area("관심 있는 구체적 내용", placeholder="예: CRISPR 유전자 가위 기술의 윤리적 문제와 최신 적용 사례")
grade = st.selectbox("2학년 영어 모의고사 평균 등급", ["1~2등급", "3~4등급", "5등급 이하"])

if st.button("추천 자료 검색하기"):
    if not major or not details:
        st.warning("희망 분야와 관심 내용을 모두 입력해 주세요.")
    else:
        with st.spinner("학생의 수준과 관심사에 맞는 자료를 찾고 있습니다..."):
            # 학생 등급별 난이도 지침 설정
            difficulty_guide = {
                "1~2등급": "Nature, Science, NYT 수준의 원문 학술 아티클/초록 수준",
                "3~4등급": "ScienceDaily, National Geographic 수준의 대중 학술 기사 수준",
                "5등급 이하": "VOA Learning English, Easy English News 수준의 쉬운 영어 아티클"
            }
            
            prompt = f"""
            너는 고등학생의 영어 수행평가를 돕는 학술 탐구 멘토야.
            학생이 작성할 영문 학술지 집필 활동을 위해 아래 조건에 맞춰 읽을 만한 영문 기사나 학술 자료 3가지를 추천해줘.

            [학생 정보]
            - 희망 진로: {major}
            - 관심 구체 내용: {details}
            - 영어 수준: {grade} ({difficulty_guide[grade]})

            [응답 양식]
            각 추천 자료마다 아래 내용을 포함해서 한국어로 깔끔하게 정리해줘:
            1. 자료 제목 (영문 원제 & 한글 번역)
            2. 추천 이유 및 주요 내용 요약 (3~4줄)
            3. 검색 팁 또는 추천 키워드 (Google Scholar나 DBpia 검색용)
            4. 탐구 활동 아이디어 (학생이 보고서나 학술지를 쓸 때 다룰 만한 핵심 질문 1가지)
            """

            # Gemini 모델 호출
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            
            st.success("추천이 완료되었습니다!")
            st.markdown(response.text)
