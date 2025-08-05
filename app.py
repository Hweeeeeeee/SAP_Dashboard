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

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Licenses", len(df))
col2.metric("Active", df[df['Status'] == 'Active'].shape[0])
col3.metric("Expired", df[df['Status'] == 'Expired'].shape[0])
col4.metric("Pending", df[df['Status'] == 'Pending'].shape[0])

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

