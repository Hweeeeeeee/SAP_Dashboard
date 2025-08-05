import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu

# 기본 페이지 설정
st.set_page_config(
    page_title="FUE License Management",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일 추가
st.markdown("""
    <style>
        /* 타이틀바 영역 */
        .title-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 30px;
            background-color: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .title-bar-left {
            display: flex;
            align-items: center;
        }
        .title-logo {
            height: 32px;
            margin-right: 15px;
        }
        .title-text {
            font-size: 20px;
            font-weight: bold;
        }
        .title-bar-right {
            display: flex;
            gap: 20px;
            align-items: center;
        }
        .menu-bar {
            background-color: white;
            border-bottom: 1px solid #ddd;
            box-shadow: 0px 2px 3px -2px rgba(0,0,0,0.1);
            padding: 5px 0;
        }
        .widget-box {
            background-color: white;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #eee;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
            border-radius: 6px;
        }
        .stApp {
            background-color: #f8f9fa;
        }
    </style>
""", unsafe_allow_html=True)

# 타이틀바 영역
st.markdown('<div class="title-bar">'
    '<div class="title-bar-left">'
    f'<img src="https://upload.wikimedia.org/wikipedia/commons/5/59/SAP_2011_logo.svg" class="title-logo">'
    '<span class="title-text">FUE License Management</span>'
    '</div>'
    '<div class="title-bar-right">'
    '<input type="text" placeholder="Search" style="padding:5px 10px; border:1px solid #ccc; border-radius:4px">'
    '<img src="https://cdn-icons-png.flaticon.com/512/1827/1827392.png" width="24">'
    '<img src="https://cdn-icons-png.flaticon.com/512/847/847969.png" width="32" style="border-radius:50%">'
    '</div>'
    '</div>', unsafe_allow_html=True)

# 메뉴 영역
selected = option_menu(
    menu_title=None,
    options=["Home", "Fue License", "User", "My account"],
    icons=["house", "key", "people", "person"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "white"},
        "icon": {"color": "#0d6efd", "font-size": "18px"},
        "nav-link": {
            "font-size": "16px",
            "margin": "0 15px",
            "padding": "8px 12px",
            "color": "#000000",
        },
        "nav-link-selected": {
            "color": "#0d6efd",
            "border-bottom": "2px solid #0d6efd",
            "font-weight": "bold"
        },
    }
)

# 본문 영역
st.write("\n")
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="widget-box">License Summary</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="widget-box">User Stats</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    st.markdown('<div class="widget-box">License by Department</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="widget-box">License Expiry Alerts</div>', unsafe_allow_html=True)

# 기타 필요한 위젯은 Figma 데이터 구조를 기준으로 추가 구성 가능
