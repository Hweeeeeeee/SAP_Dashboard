import streamlit as st
import pandas as pd
import numpy as np

# --- 1. 페이지 설정 및 커스텀 CSS ---
st.set_page_config(layout="wide")

st.markdown("""
<style>
/* CSS 변수 설정 */
:root {
    --background-color: #f0f2f6; /* 본문 배경색 */
    --widget-bg-color: white; /* 위젯 배경색 */
    --primary-color: #007bff; /* 메뉴 선택 강조색 */
}

/* Streamlit 기본 스타일 숨기기 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* 전체 페이지 배경색 적용 */
.stApp {
    background-color: var(--background-color);
}

/* 2. 상단 타이틀바 (Figma 디자인 반영) */
.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: var(--widget-bg-color);
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    height: 50px;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 15px;
    font-size: 20px;
    font-weight: bold;
    color: #333;
}

.sap-logo {
    height: 30px;
}

.header-right {
    display: flex;
    align-items: center;
    gap: 20px;
}

.icon {
    font-size: 20px;
    color: #555;
    cursor: pointer;
}

.profile-circle {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: #007bff;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    cursor: pointer;
}

/* 2. 메뉴 영역 (Figma 디자인 반영) */
.menu-container {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    background-color: var(--widget-bg-color);
    padding: 0 20px;
    box-shadow: 0 2px 2px -2px rgba(0,0,0,0.1);
    position: fixed;
    top: 50px; /* 타이틀바 높이만큼 하단에 위치 */
    left: 0;
    right: 0;
    z-index: 999;
}

.menu-item {
    padding: 10px 15px;
    margin-right: 10px;
    cursor: pointer;
    font-weight: bold;
    color: #555;
    text-decoration: none;
    transition: color 0.2s, border-bottom 0.2s;
    user-select: none; /* 텍스트 선택 방지 */
}

.menu-item:hover {
    color: var(--primary-color);
}

.menu-item.selected {
    color: var(--primary-color);
    border-bottom: 3px solid var(--primary-color);
}

/* 4. 본문 및 위젯 스타일 (Figma 디자인 반영) */
.main-content {
    background-color: var(--background-color);
    padding: 20px;
    margin-top: 100px; /* 타이틀바+메뉴바 높이만큼 마진 */
}

.widget-container {
    background-color: var(--widget-bg-color);
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

.widget-title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 15px;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

# --- 2. 상태 관리 (메뉴 선택) ---
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# --- 3. UI 요소 함수 ---

def render_header():
    """Figma에 기반한 타이틀바 영역 렌더링"""
    st.markdown(
        f'<div class="header-container">'
        f'<div class="header-left">'
        f'<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/SAP_2011_logo.svg/1024px-SAP_2011_logo.svg.png" class="sap-logo">'
        f'<span>FUE License Management</span>'
        f'</div>'
        f'<div class="header-right">'
        f'<span class="icon">🔍</span>'
        f'<span class="icon">🔔</span>'
        f'<div class="profile-circle">JP</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )

def render_menu():
    """Figma에 기반한 메뉴 영역 렌더링"""
    menu_items = ['Home', 'FUE License', 'User', 'My account']
    
    st.markdown('<div class="menu-container">', unsafe_allow_html=True)
    
    # st.button 대신 HTML 버튼을 사용하여 커스텀 스타일 적용
    cols = st.columns(len(menu_items))
    for i, item in enumerate(menu_items):
        is_selected = " selected" if st.session_state.page == item else ""
        with cols[i]:
            if st.button(item, key=f"menu_{item}", type="secondary"):
                st.session_state.page = item
                st.rerun()

    # st.button의 기본 스타일을 CSS로 덮어쓰기
    st.markdown("""
    <style>
    .stButton>button {
        background-color: transparent !important;
        color: #555 !important;
        border: none !important;
        font-weight: bold !important;
        box-shadow: none !important;
        padding: 10px 15px !important;
        margin: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 선택된 메뉴 아이템에 대한 스타일 적용
    st.markdown(f"""
    <style>
    [data-testid="stButton-secondary"] button[kind="secondary"][aria-label="menu_{st.session_state.page}"] {{
        color: var(--primary-color) !important;
        border-bottom: 3px solid var(--primary-color) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. Figma 기반 가상 데이터 생성 ---
@st.cache_data
def generate_sample_data():
    """Figma에 있는 대시보드 위젯에 사용할 가상 데이터를 생성"""
    # Figma 데이터 기반으로 숫자 수정
    df_licenses = pd.DataFrame({
        "license_type": ["Professional", "Limited Professional", "Employee", "Developer"],
        "assigned": [100, 80, 75, 3],
        "available": [20, 20, 10, 2],
        "cost_per_year": [4000, 2500, 1500, 5000]
    })
    df_licenses['total_cost'] = df_licenses['assigned'] * df_licenses['cost_per_year']

    df_users = pd.DataFrame({
        "User_ID": [f"user{i+1}" for i in range(10)],
        "User_Name": [f"User {i+1}" for i in range(10)],
        "License_Type": np.random.choice(["Professional", "Limited Professional"], 10),
        "Last_Login_Date": pd.to_datetime(pd.Series(np.random.randint(pd.Timestamp('2024-01-01').value, pd.Timestamp('2024-07-31').value, 10)), unit='ns').dt.date
    })
    
    # Cost Savings Chart Data (Figma 참고)
    df_savings = pd.DataFrame({
        "Quarter": ["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023", "Q1 2024", "Q2 2024"],
        "Savings ($)": [15000, 25000, 20000, 18000, 30000, 35000]
    })

    return df_licenses, df_users, df_savings

df_licenses, df_users, df_savings = generate_sample_data()

# --- 5. 콘텐츠 페이지 함수 ---
def show_home():
    """Home 페이지 콘텐츠 (Figma 기반 위젯)"""
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">Dashboard Overview</div>', unsafe_allow_html=True)
    
    # 3개의 KPI 위젯 (Figma 참고)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="widget-container">', unsafe_allow_html=True)
        st.markdown('<div class="widget-title">Total Active Users</div>', unsafe_allow_html=True)
        st.metric(label="", value=f"{df_licenses['assigned'].sum()}", delta="3 users from last month")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="widget-container">', unsafe_allow_html=True)
        st.markdown('<div class="widget-title">Total License Cost</div>', unsafe_allow_html=True)
        total_cost = df_licenses['total_cost'].sum()
        st.metric(label="", value=f"${total_cost:,.0f}", delta=f"${-5000:,.0f} from last year")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="widget-container">', unsafe_allow_html=True)
        st.markdown('<div class="widget-title">Potential Savings</div>', unsafe_allow_html=True)
        st.metric(label="", value=f"$35,000", delta="30% of total cost")
        st.markdown('</div>', unsafe_allow_html=True)

    # 차트 위젯 (Figma 참고)
    col4, col5 = st.columns(2)
    with col4:
        st.markdown('<div class="widget-container">', unsafe_allow_html=True)
        st.markdown('<div class="widget-title">License Usage by Type</div>', unsafe_allow_html=True)
        st.bar_chart(df_licenses.set_index('license_type')[['assigned', 'available']])
        st.markdown('</div>', unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="widget-container">', unsafe_allow_html=True)
        st.markdown('<div class="widget-title">Historical Cost Savings</div>', unsafe_allow_html=True)
        st.bar_chart(df_savings.set_index('Quarter'))
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def show_fue_license():
    """FUE License 페이지 콘텐츠"""
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<div class="widget-container">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">License Details</div>', unsafe_allow_html=True)
    st.dataframe(df_licenses.set_index('license_type'), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_user():
    """User 페이지 콘텐츠"""
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<div class="widget-container">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">User Management</div>', unsafe_allow_html=True)
    st.dataframe(df_users, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_my_account():
    """My account 페이지 콘텐츠"""
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<div class="widget-container">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">Account Information</div>', unsafe_allow_html=True)
    st.write("사용자 정보와 설정을 관리하는 페이지입니다.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. 메인 앱 실행 로직 ---
render_header()
render_menu()

if st.session_state.page == 'Home':
    show_home()
elif st.session_state.page == 'FUE License':
    show_fue_license()
elif st.session_state.page == 'User':
    show_user()
elif st.session_state.page == 'My account':
    show_my_account()
