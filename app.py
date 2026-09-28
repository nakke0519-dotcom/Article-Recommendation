import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="영문 학술지 집필 AI 어시스턴트", layout="centered")

# 🔑 Streamlit Secrets에서 선생님의 개인 API 키를 불러옵니다.
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 타이틀 및 하단 설명
st.title("📚 영문 학술지 집필 AI 어시스턴트")
st.write("관심 분야와 영어 등급을 입력하면, 적절한 수준의 영문 아티클 추천부터 맞춤형 탐구 설계까지 도와드립니다.")

# 세션 상태 초기화 (1단계 결과 및 2단계 진행 상태 저장)
if "step1_result" not in st.session_state:
    st.session_state.step1_result = None
if "selected_major" not in st.session_state:
    st.session_state.selected_major = ""
if "selected_grade" not in st.session_state:
    st.session_state.selected_grade = ""

st.markdown("---")
st.subheader("1단계: 맞춤형 영문 아티클 및 탐구 소재 추천")

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
            
            prompt_step1 = f"""
            너는 대한민국 고등학교 2학년 학생들의 영어 수행평가 및 영문 학술지 집필을 돕는 전문 탐구 멘토야.
            학생이 깊이 있는 수행평가 보고서를 작성할 수 있도록 '풍부한 탐구 정보'와 '다양한 작성 아이디어'를 제공해줘.

            [학생 정보]
            - 희망 진로: {major}
            - 세부 관심 내용: {details}
            - 영어 독해 수준: {grade}

            [난이도 설정 지침]
            {difficulty_guide[grade]}
            ※ 주의: 실제 학술 논문 원문(Abstract 포함)이나 전문 학술지(Nature, Science 등)는 고등학생에게 너무 어려우므로 절대로 추천하지 마. 대중적이고 직관적인 과학/시사/교양 아티클 수준으로 다룰 것.

            [응답 양식]
            각 추천 자료마다 아래 형식에 정확히 맞추어 한국어로 작성해줘:

            ### 📄 추천 1. [자료 영문 정확한 풀제목] ([한글 번역 제목])
            - **추천 매체/출처**: (예: Science News Explores, VOA Learning English 등)
            - **이 아티클을 추천하는 이유**: (학생의 진로 및 관심사와 어떻게 결합되는지 2줄 설명)
            - **핵심 정보 및 개념 요약**: (기사에서 다루는 핵심 학술 개념, 사례, 현황 등을 4~5줄로 상세히 설명)
            - **💡 풍부한 탐구 및 영문 학술지 집필 아이디어 (5가지)**:
              1) [원인 분석형] (세부 질문)
              2) [비교/대조형] (세부 질문)
              3) [윤리/사회적 영향형] (세부 질문)
              4) [적용/해결책 제안형] (세부 질문)
              5) [영문 결론 작성 팁] (핵심 키워드 및 표현)
            - **추천 검색 키워드**: (영문 키워드 조합 2~3개)
            """

            try:
                model = genai.GenerativeModel('gemini-3.8-flash')
                response = model.generate_content(prompt_step1)
                
                # 1단계 결과 및 입력정보 세션 저장
                st.session_state.step1_result = response.text
                st.session_state.selected_major = major
                st.session_state.selected_grade = grade
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

# 1단계 결과가 있을 경우 화면에 표시
if st.session_state.step1_result:
    st.success("학생의 영문 학술지 집필을 위한 맞춤형 탐구 주제와 정보가 준비되었습니다!")
    st.markdown(st.session_state.step1_result)
    
    # ---------------------------------------------------------
    # 2단계: 학생 개별 탐구 방향 설정 및 심화 가이드
    # ---------------------------------------------------------
    st.markdown("---")
    st.subheader("💡 2단계: 나만의 탐구 방식 및 집필 계획 설계하기")
    st.info("위 추천 내용 중 하나를 선택하거나, 아이디어를 바탕으로 학생이 직접 결정한 탐구 주제와 방향을 작성해 주세요!")
    
    user_topic = st.text_input(
        "탐구할 세부 주제를 입력하세요", 
        placeholder="예: 스포츠 선수의 부상 예방을 위한 Wearables 기술 활용과 영문 기사 분석"
    )
    user_direction = st.text_area(
        "어떤 방향이나 방식으로 탐구하고 싶은지 간략히 적어주세요 (선택사항)", 
        placeholder="예: 체육교과와 연계하여 학생들의 인식 설문조사를 실시하고, 영문 기사의 핵심 기술 관련 용어를 정리해서 보고서를 쓰고 싶어요."
    )
    
    if st.button("🚀 나만의 맞춤형 탐구 플랜 생성하기"):
        if not user_topic:
            st.warning("탐구할 세부 주제를 먼저 입력해 주세요!")
        else:
            with st.spinner("고등학생 수준에 최적화된 주도적 탐구 방법 및 영문 보고서 구성을 설계 중입니다..."):
                
                prompt_step2 = f"""
                너는 대한민국 고등학교 영어 교과 세부능력 및 특기사항(세특)과 학술 탐구 보고서 집필을 전문적으로 지도하는 영어 교육 전문가야.
                학생이 제시한 주제와 방향성을 바탕으로, 고등학교 2학년 수준에서 최고 수준의 역량(자기주도성, 탐구력, 학업역량)을 보여줄 수 있는 구체적인 탐구 설계안을 작성해줘.

                [학생 기초 정보]
                - 희망 진로: {st.session_state.selected_major}
                - 영어 독해 수준: {st.session_state.selected_grade}
                - 학생이 결정한 탐구 주제: {user_topic}
                - 학생이 희망하는 탐구 방향: {user_direction}

                [필수 고려 요소 - 가이드 작성 시 반드시 반영할 것]
                1. **고교생 수준 적합성**: 무리한 대학 수준 논문 작성 대신, 고교 교육과정 수준에서 유의미하고 구체적인 주제로 정제해줄 것.
                2. **영문 자료 심화 탐독 과정**: 영어 교과 세특에 명확히 기록될 수 있도록 영문 아티클 독해, 핵심 구문/어휘 정리, 영문 요약(Abstract) 집필 프로세스를 포함할 것.
                3. **주도적 추가 활동 설계**: 단지 읽기에서 그치지 않고, 학생의 역량이 드러나는 실천적 활동(설문조사, 학생/교사/전문가 인터뷰, 관련 도서 탐독, 교내 실태 조사, 간단한 데이터 비교 분석 등)을 적극 제안할 것.

                [응답 양식]
                아래 목차 양식에 맞춰 학생에게 건네는 친절한 멘토링 말투로 작성해줘:

                ## 🎯 [학생 주제] 맞춤형 탐구 및 집필 가이드

                ### 1. 📌 주제 평가 및 고교생 맞춤 구체화
                - **주제 적합성**: (고등학교 수준에서 이 주제가 왜 훌륭하고 유의미한지 평가)
                - **추천 탐구 제목**: (영문 학술지 제출용 정교한 한글/영문 제목 제안)

                ### 2. 📖 영문 자료 탐독 및 영어 역량 강화 방안 (영어 세특 핵심)
                - **영문 읽기 전략**: (학생의 독해 등급({st.session_state.selected_grade})을 고려한 아티클 읽기 팁)
                - **세특에 녹여낼 영문 집필 요소**: (아티클 핵심 문장 분석, 주요 전문 학술 어휘집(Glossary) 작성법, 100단어 영문 요약문(Abstract) 작성 가이드)

                ### 3. 🔍 학생 주도적 추가 탐구 활동 추천 (택 1~2개 활용)
                - **[추천 1] 실천적 조사 활동**: (설문조사, 학교 내 현황 조사, 인터뷰 질문지 작성 등 구체적 실행법)
                - **[추천 2] 연계 도서/자료 탐독**: (같이 읽으면 좋은 관련 한글/영문 서적 매칭 및 비교 포인트)
                - **[추천 3] 데이터/사례 비교 분석**: (실제 뉴스나 통계 자료를 바탕으로 한 비교 가이드)

                ### 4. 📝 영문 학술지(보고서) 목차 및 작성 단계
                - **I. 서론 (Introduction)**: (문제 제기 및 탐구 동기)
                - **II. 본론 1 (Literature Review)**: (영문 아티클에서 찾은 핵심 이론 및 현황)
                - **III. 본론 2 (Active Investigation)**: (학생이 진행한 추가 활동/조사 결과)
                - **IV. 결론 및 제언 (Conclusion)**: (시사점 및 영문 느낀 점 작성 방향)
                """

                try:
                    model = genai.GenerativeModel('gemini-3.8-flash')
                    response_step2 = model.generate_content(prompt_step2)
                    
                    st.success("학생만의 주도적 탐구 플랜이 성공적으로 생성되었습니다!")
                    st.markdown(response_step2.text)
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
