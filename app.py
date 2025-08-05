import streamlit as st
import pandas as pd
import plotly.express as px

# --- 페이지 설정 ---
st.set_page_config(page_title="SAP License Dashboard", layout="wide")

# 사용자 정보 설정
user_name = "Kim Hwi-young"
user_initial = "KH"

# --- 스타일 + 헤더 바 ---
st.markdown(f"""
    <style>
    .topbar {{
        background-color: #001f3f;
        color: white;
        padding: 0.8rem 1.2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .logo {{
        font-size: 20px;
        font-weight: bold;
    }}
    .user-profile {{
        display: flex;
        align-items: center;
        gap: 1rem;
    }}
    .avatar {{
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background-color: #ffffff;
        color: #001f3f;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 16px;
    }}
    .footer {{
        background-color: #f2f2f2;
        padding: 12px;
        text-align: center;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        font-size: 14px;
        color: #888;
        z-index: 100;
    }}
    .card {{
        background-color: #f9fafb;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    }}
    .card h3 {{
        margin-bottom: 5px;
        color: #333;
        font-size: 16px;
    }}
    .card p {{
        margin: 0;
        color: #0070f3;
        font-size: 26px;
        font-weight: 600;
    }}
    </style>

    <div class="topbar">
        <div class="logo">🔷 SAP License Dashboard</div>
        <div class="user-profile">
            <input type="text" placeholder="Search..." style="padding:5px 10px; border-radius:6px; border:1px solid #ccc;">
            <div class="avatar">{user_initial}</div>
            <span>{user_name}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 데이터 로드 ---
@st.cache_data
def load_data():
    return pd.read_csv("licenses.csv")

df = load_data()

# --- Section: Overview ---
st.subheader("📊 Overview")
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"""<div class="card"><h3>Total Licenses</h3><p>{len(df)}</p></div>""", unsafe_allow_html=True)
col2.markdown(f"""<div class="card"><h3>Active</h3><p>{df[df['Status']=='Active'].shape[0]}</p></div>""", unsafe_allow_html=True)
col3.markdown(f"""<div class="card"><h3>Expired</h3><p>{df[df['Status']=='Expired'].shape[0]}</p></div>""", unsafe_allow_html=True)
col4.markdown(f"""<div class="card"><h3>Pending</h3><p>{df[df['Status']=='Pending'].shape[0]}</p></div>""", unsafe_allow_html=True)

# 상태 요약 차트
status_counts = df["Status"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]
fig = px.pie(status_counts, names="Status", values="Count", hole=0.4)
st.plotly_chart(fig, use_container_width=True)

# --- Section: License Table ---
st.subheader("📋 License Table")
st.dataframe(df, use_container_width=True)

# --- Footer ---
st.markdown("""
    <div class="footer">
        © 2025 SAP | License Management Tool • Terms • Privacy
    </div>
""", unsafe_allow_html=True)
