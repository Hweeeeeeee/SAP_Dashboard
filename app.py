import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(layout="wide", page_title="License Management Dashboard")

# --- 스타일 정의 (Figma 스타일 근사화) ---
st.markdown("""
    <style>
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    .card h3 {
        color: #333;
        font-size: 18px;
        margin-bottom: 8px;
    }
    .card p {
        font-size: 28px;
        font-weight: bold;
        margin: 0;
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# --- 데이터 로드 ---
@st.cache_data
def load_data():
    return pd.read_csv("licenses.csv")

df = load_data()

# --- 타이틀 & 카드 요약 ---
st.title("🎫 License Management Dashboard")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
        <div class="card">
            <h3>Total Licenses</h3>
            <p>{len(df)}</p>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div class="card">
            <h3>Active</h3>
            <p>{df[df["Status"] == "Active"].shape[0]}</p>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
        <div class="card">
            <h3>Expired</h3>
            <p>{df[df["Status"] == "Expired"].shape[0]}</p>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
        <div class="card">
            <h3>Pending</h3>
            <p>{df[df["Status"] == "Pending"].shape[0]}</p>
        </div>
    """, unsafe_allow_html=True)

# --- 사이드바 필터 ---
with st.sidebar:
    st.header("🔍 Filter Licenses")
    name_filter = st.text_input("User Name")
    status_filter = st.selectbox("License Status", options=["All"] + df["Status"].unique().tolist())
    product_filter = st.multiselect("Product", options=df["Product"].unique())

# --- 필터 적용 ---
filtered_df = df.copy()
if name_filter:
    filtered_df = filtered_df[filtered_df["User Name"].str.contains(name_filter, case=False)]
if status_filter != "All":
    filtered_df = filtered_df[filtered_df["Status"] == status_filter]
if product_filter:
    filtered_df = filtered_df[filtered_df["Product"].isin(product_filter)]

# --- 차트 ---
st.subheader("📊 License Status Overview")
status_counts = filtered_df["Status"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]
fig = px.pie(status_counts, names="Status", values="Count", hole=0.4)
st.plotly_chart(fig, use_container_width=True)

# --- 테이블 ---
st.subheader("📋 License Details Table")
st.dataframe(filtered_df, use_container_width=True)
