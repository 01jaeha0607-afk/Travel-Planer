import streamlit as st
import google.generativeai as genai

# --- API 키 설정 본인의 키를 아래에 붙여넣으세요!) ---
API_KEY = "여기에_발급받은_API_키를_넣으세요입력" 

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash') 

st.set_page_config(page_title="AI 여행 플래너 Pro", page_icon="✈️", layout="wide")

st.title("✈️ 찐 AI 여행 플래너 (Pro 버전)")
st.markdown("조건과 세부 요청사항을 적어주시면, 일정부터 예상 경비까지 한 번에 뽑아드립니다!")

# --- 1. 사용자 입력(UI) 섹션 ---
st.subheader("📝 여행 기본 정보")
col1, col2, col3 = st.columns(3)

with col1:
    destination = st.text_input("📍 여행지 (예: 제주도, 삿포로, 파리)")
with col2:
    month = st.selectbox("📅 몇 월에 가시나요?", [f"{i}월" for i in range(1, 13)])
with col3:
    duration = st.number_input("⏳ 여행 기간 (일)", min_value=1, max_value=30, value=3)

st.subheader("💡 여행 디테일")
# ✨ [수정된 부분] 인원수를 넣기 위해 칸을 3개(col4, col5, col6)로 나누었습니다.
col4, col5, col6 = st.columns(3)

with col4:
    companion = st.selectbox("🙋 누구와 함께 가나요?", ["혼자", "연인과", "가족과", "친구들과", "아이와 함께"])
with col5:
    # ✨ [신규 기능] 인원수 입력창 추가
    num_people = st.number_input("👥 총 인원수 (명)", min_value=1, max_value=20, value=1)
with col6:
    style = st.selectbox("🎒 여행 스타일은?", ["힐링/휴양", "로컬 맛집 탐방", "액티비티/관광", "가성비 배낭여행", "사진 촬영/핫플"])

st.subheader("✍️ 특별한 요청사항 (선택)")
extra_request = st.text_area(
    "AI가 일정에 꼭 반영했으면 하는 내용을 자유롭게 적어주세요.", 
    placeholder="예: 해산물 알레르기가 있어요. 걷는 시간은 하루 2시간 이내로 해주세요. 숙소는 1박에 10만원 이하로 찾아주세요. 꼭 가고 싶은 곳: 디즈니랜드"
)

# --- 2. 결과 출력 (AI 연동) 섹션 ---
st.divider()

if st.button("✨ 내 여행 일정 & 예산 만들기", use_container_width=True):
    if not destination:
        st.warning("여행지를 입력해주세요!")
    elif API_KEY == "여기에_발급받은_API_키를_넣으세요":
        st.error("앗! 코드 상단에 API 키를 먼저 입력해야 AI가 작동합니다.")
    else:
        with st.spinner(f'AI가 {num_people}명 기준의 {destination} 맞춤 일정과 💰예상 경비를 계산 중입니다... 🔍'):
            
            # ✨ [수정된 부분] 프롬프트에 '총 인원' 추가 및 숙소/예산 조건 강화
            prompt = f"""
            당신은 10년 차 베테랑 여행 플래너이자 예산 관리 전문가입니다. 아래 조건에 맞춰서 완벽한 여행 일정과 예상 경비를 짜주세요.
            
            [여행 조건]
            - 여행지: {destination}
            - 시기: {month}
            - 기간: {duration}일
            - 동행인: {companion}
            - 총 인원: {num_people}명
            - 여행 스타일: {style}
            - 세부 요청사항: {extra_request if extra_request else '특별한 요청사항 없음'}
            
            [필수 포함 내용]
            1. {month} {destination} 여행 시 옷차림 및 주의할 팁
            2. {num_people}명({companion})이 함께 머물기 좋은 추천 숙소 위치 (구체적인 동네나 호텔 이름, 적합한 객실 형태)
            3. 일자별 상세 일정 (오전/오후/저녁으로 나누고, '세부 요청사항'을 완벽하게 반영할 것)
            4. {style}에 맞는 추천 맛집 및 동선
            5. 🚻 화장실 꿀팁: 일정 동선 근처의 무료 화장실 정보를 알려주세요. (특히 전 세계 어디서든 화장실 이용이 가장 편리한 '근처 스타벅스 매장'의 위치나 존재 여부를 반드시 포함할 것!)
            6. 💰 [예상 여행 경비 표]: 항공/교통, 숙박, 식비, 기타(관광 등) 항목으로 나누어 '{num_people}명 기준'의 총 예상 예산을 깔끔한 표(Table) 형태로 정리해 주세요. 화폐 단위는 원(KRW)으로 대략적으로 환산해서 보여주세요.
            
            답변은 읽기 편하게 마크다운(Markdown)과 이모지를 적절히 사용해서 출력해줘.
            """
            
            try:
                response = model.generate_content(prompt)
                
                st.success("🎉 맞춤형 여행 일정과 예산안이 완성되었습니다!")
                
                with st.container(border=True):
                    st.markdown(response.text)
                    
            except Exception as e:
                st.error(f"AI와 통신 중 에러가 발생했습니다: {e}")
