import streamlit as st
import pandas as pd
import numpy as np

# --- 1. 페이지 설정 및 커스텀 CSS ---
# 전체 페이지 레이아웃을 넓게 설정
st.set_page_config(layout="wide")

# SAP UI 스타일을 위한 커스텀 CSS
st.markdown("""
<style>
/* Streamlit 기본 스타일 숨기기 (헤더, 푸터 등) */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* 전체 페이지 배경색 */
body {
    background-color: #f0f2f6; /* 아주 연한 회색 */
}

/* 1-1, 1-2. 최상단 타이틀바 영역 스타일 */
.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
}

.header-right {
    display: flex;
    align-items: center;
    gap: 20px;
}

.sap-logo {
    height: 30px;
}

.search-icon {
    font-size: 20px;
    cursor: pointer;
}

.alarm-icon {
    font-size: 20px;
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

/* 2, 3. 메뉴 영역 스타일 */
.menu-container {
    background-color: white;
    display: flex;
    justify-content: flex-start;
    padding: 0 20px;
    border-bottom: 1px solid #e0e0e0;
    box-shadow: 0 2px 4px -2px rgba(0,0,0,0.1);
    margin-top: 50px; /* 타이틀바 높이만큼 마진 */
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 999;
}

.menu-item {
    padding: 10px 15px;
    cursor: pointer;
    font-weight: bold;
    color: #555;
    text-decoration: none;
    transition: color 0.2s, border-bottom 0.2s;
}

.menu-item:hover {
    color: #007bff;
}

.menu-item.selected {
    color: #007bff;
    border-bottom: 3px solid #007bff;
}

/* 4. 본문 및 위젯 스타일 */
.main-content {
    background-color: #f0f2f6; /* 아주 연한 회색 */
    padding: 20px;
    margin-top: 100px; /* 타이틀바+메뉴바 높이만큼 마진 */
}

.widget-container {
    background-color: white;
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
    """타이틀바 영역 렌더링"""
    # 타이틀바는 고정되어야 하므로 st.columns로 구현하지 않고 HTML/CSS로 전체 영역을 정의
    st.markdown(
        f'<div class="header-container">'
        f'<div class="header-left">'
        f'<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/SAP_2011_logo.svg/1024px-SAP_2011_logo.svg.png" class="sap-logo">'
        f'<span style="font-size: 20px; font-weight: bold;">FUE License Management</span>'
        f'</div>'
        f'<div class="header-right">'
        f'<span class="search-icon">🔍</span>'
        f'<span class="alarm-icon">🔔</span>'
        f'<div class="profile-circle">JP</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )

def render_menu():
    """메뉴 영역 렌더링"""
    menu_items = ['Home', 'FUE License', 'User', 'My account']
    
    # HTML/CSS를 사용하여 메뉴 렌더링
    st.markdown('<div class="menu-container">', unsafe_allow_html=True)
    
    cols = st.columns(len(menu_items))
    for i, item in enumerate(menu_items):
        is_selected = " selected" if st.session_state.page == item else ""
        with cols[i]:
            if st.button(item, key=f"menu_{item}"):
                st.session_state.page = item
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. 가상 데이터 생성 ---
@st.cache_data
def generate_sample_data():
    """대시보드 위젯에 사용할 가상 데이터를 생성"""
    data = {
        "license_type": ["Professional", "Limited Professional", "Employee", "Developer"],
        "assigned": np.random.randint(10, 150, 4),
        "available": np.random.randint(20, 200, 4),
        "cost_per_year": [4000, 2500, 1500, 5000]
    }
    df_licenses = pd.DataFrame(data)
    df_licenses['total_cost'] = df_licenses['assigned'] * df_licenses['cost_per_year']

    df_users = pd.DataFrame({
        "User_ID": [f"user{i+1}" for i in range(10)],
        "User_Name": [f"User Name {i+1}" for i in range(10)],
        "License_Type": np.random.choice(data["license_type"], 10),
        "Last_Login_Date": pd.to_datetime(pd.Series(np.random.randint(pd.Timestamp('2023-01-01').value, pd.Timestamp('2024-07-31').value, 10)), unit='ns').dt.date
    })

    return df_licenses, df_users

df_licenses, df_users = generate_sample_data()

# --- 5. 콘텐츠 페이지 함수 ---
def show_home():
    """Home 페이지 콘텐츠"""
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">Dashboard Overview</div>', unsafe_allow_html=True)
    
    # 3개의 KPI 위젯 (Figma 참고)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="widget-container">', unsafe_allow_html=True)
        st.markdown('<div class="widget-title">Total Active Users</div>', unsafe_allow_html=True)
        st.metric(label="", value=f"{len(df_users)}", delta=f"{len(df_users) - 8} from last month")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="widget-container">', unsafe_allow_html=True)
        st.markdown('<div class="widget-title">Total License Cost</div>', unsafe_allow_html=True)
        total_cost = df_licenses['total_cost'].sum()
        st.metric(label="", value=f"${total_cost:,.0f}", delta=f"${-5000:,.0f} compared to last year")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="widget-container">', unsafe_allow_html=True)
        st.markdown('<div class="widget-title">Potential Savings</div>', unsafe_allow_html=True)
        st.metric(label="", value=f"$35,000", delta=f"30% of license cost")
        st.markdown('</div>', unsafe_allow_html=True)

    # 차트 위젯
    st.markdown('<div class="widget-container">', unsafe_allow_html=True)
    st.markdown('<div class="widget-title">License Usage by Type</div>', unsafe_allow_html=True)
    st.bar_chart(df_licenses.set_index('license_type')[['assigned', 'available']])
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
# 헤더와 메뉴 영역은 항상 표시
render_header()
render_menu()

# 선택된 페이지에 따라 콘텐츠 렌더링
if st.session_state.page == 'Home':
    show_home()
elif st.session_state.page == 'FUE License':
    show_fue_license()
elif st.session_state.page == 'User':
    show_user()
elif st.session_state.page == 'My account':
    show_my_account()
