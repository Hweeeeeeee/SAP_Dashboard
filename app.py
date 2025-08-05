import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import io
import base64

# 기본 페이지 설정
st.set_page_config(
    page_title="FUE License Management",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일 추가
st.markdown("""
    <style>
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
        .stApp {
            background-color: #f8f9fa;
        }
    </style>
""", unsafe_allow_html=True)

# 타이틀바 영역
st.markdown(
    '<div class="title-bar">'
    '<div class="title-bar-left">'
    '<img src="https://upload.wikimedia.org/wikipedia/commons/5/59/SAP_2011_logo.svg" class="title-logo">'
    '<span class="title-text">FUE License Management</span>'
    '</div>'
    '<div class="title-bar-right">'
    '<input type="text" placeholder="Search" style="padding:5px 10px; border:1px solid #ccc; border-radius:4px">'
    '<img src="https://cdn-icons-png.flaticon.com/512/1827/1827392.png" width="24">'
    '<img src="https://cdn-icons-png.flaticon.com/512/847/847969.png" width="32" style="border-radius:50%">'
    '</div>'
    '</div>', unsafe_allow_html=True
)

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
            "font-weight": "bold",
            "background-color": "#0d6efd10"
        },
    }
)

# 카드 출력 함수 (높이 늘리고 flex로 중앙정렬 적용)
def render_card(title, value):
    html = f"""
    <div style='
        background-color:white;
        padding:20px;
        margin:10px;
        border:1px solid #ccc;
        box-shadow:0px 2px 4px rgba(0,0,0,0.1);
        border-radius:8px;
        text-align:center;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    '>
        <h4 style='margin-bottom:10px'>{title}</h4>
        <h1>{value}</h1>
    </div>
    """
    components.html(html, height=200)

st.write("\n")
col1, col2, col3 = st.columns(3)
with col1:
    render_card("Total Licenses", 128)
with col2:
    render_card("Used Licenses", 94)
with col3:
    render_card("Available Licenses", 34)

col4, col5, col6 = st.columns(3)
with col4:
    render_card("Active Users", 87)
with col5:
    render_card("Inactive Users", 13)
with col6:
    render_card("New Users (This Month)", 7)

# License by Department 차트 위젯
with st.container():
    buf = io.BytesIO()
    departments = ["Finance", "HR", "IT", "Sales"]
    counts = [30, 20, 45, 33]
    fig, ax = plt.subplots()
    ax.bar(departments, counts)
    ax.set_ylabel("Licenses")
    fig.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode()

    chart_html = f"""
    <div style='
        background-color:white;
        padding:20px;
        margin:10px;
        border:1px solid #ccc;
        box-shadow:0px 2px 4px rgba(0,0,0,0.1);
        border-radius:8px;
        text-align:center;
    '>
        <h4 style='margin-bottom:10px'>License by Department</h4>
        <img src='data:image/png;base64,{img_base64}'>
    </div>
    """
    components.html(chart_html, height=400)

# License Expiry Alerts 카드 (타이틀 + 테이블 같이)
with st.container():
    st.markdown("""
    <div style='
        background-color:white;
        padding:20px;
        margin:10px;
        border:1px solid #ccc;
        box-shadow:0px 2px 4px rgba(0,0,0,0.1);
        border-radius:8px;
    '>
        <h4>License Expiry Alerts</h4>
    """, unsafe_allow_html=True)

    df_alerts = pd.DataFrame({
        "User": ["user1", "user2", "user3"],
        "License": ["Professional", "Basic", "Viewer"],
        "Expires": ["2025-09-01", "2025-08-20", "2025-08-10"]
    })
    st.dataframe(df_alerts, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
