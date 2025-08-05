import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(layout="wide", page_title="License Dashboard")

# --- Sample CSV 읽기 (예시) ---
@st.cache_data
def load_data():
    # 여기에 실제 CSV 경로를 넣으세요.
    return pd.read_csv("licenses.csv")

df = load_data()

# --- 상단 타이틀 및 요약 카드 ---
st.markdown("""
    <style>
    .stMetric {
        background-color: #f2f2f2;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background-color: #f2f2f2; padding: 20px; border-radius: 10px; text-align: center;">
        <h3 style="color: #333333;">Total Licenses</h3>
        <p style="font-size: 24px; font-weight: bold;">120</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: #eaf8ea; padding: 20px; border-radius: 10px; text-align: center;">
        <h3 style="color: #2e7d32;">Active</h3>
        <p style="font-size: 24px; font-weight: bold;">93</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background-color: #fff3e0; padding: 20px; border-radius: 10px; text-align: center;">
        <h3 style="color: #ef6c00;">Expired</h3>
        <p style="font-size: 24px; font-weight: bold;">27</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- 사이드 필터 ---
with st.sidebar:
    st.header("🔎 Filters")
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
st.markdown("### 📊 License Status Overview")
status_counts = filtered_df["Status"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]
fig = px.pie(status_counts, names="Status", values="Count", hole=0.4)
st.plotly_chart(fig, use_container_width=True)

# --- 테이블 ---
st.markdown("### 📋 License Table")
st.dataframe(filtered_df, use_container_width=True)


