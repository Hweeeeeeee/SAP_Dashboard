import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="License Dashboard")

# 스타일 CSS
st.markdown("""
<style>
.card { background-color: #f9fafb; padding:20px; border-radius:8px;
         text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.1); }
.card h3 { margin-bottom:5px; color:#333; font-size:16px; }
.card p { margin:0; color:#0070f3; font-size:26px; font-weight:600; }
table[data-testid="styledTable"] { width:100%; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("licenses.csv")

df = load_data()

st.title("🔑 License Management Dashboard")

# 요약 카드 레이아웃
cards = [
    ("Total", len(df),),
    ("Active", df[df.Status=="Active"].shape[0]),
    ("Expired", df[df.Status=="Expired"].shape[0]),
    ("Pending", df[df.Status=="Pending"].shape[0])
]
cols = st.columns(4)
for col, (label, val) in zip(cols, cards):
    col.markdown(f"""<div class="card"><h3>{label}</h3><p>{val}</p></div>""", unsafe_allow_html=True)

st.markdown("---")

# 사이드바 필터
with st.sidebar:
    st.header("🔍 Filters")
    name = st.text_input("User Name")
    status = st.selectbox("License Status", options=["All"]+sorted(df.Status.unique().tolist()))
    product = st.multiselect("Product", options=sorted(df.Product.unique().tolist()))

# 필터 적용
fd = df.copy()
if name:
    fd = fd[fd["User Name"].str.contains(name, case=False)]
if status != "All":
    fd = fd[fd.Status == status]
if product:
    fd = fd[fd.Product.isin(product)]

# 차트
st.subheader("📊 Status Overview")
st.plotly_chart(
    px.pie(fd.reset_index().groupby("Status").size().rename("Count").reset_index(),
           names="Status", values="Count", hole=0.4),
    use_container_width=True
)

# 상세 테이블
st.subheader("📋 License Details")
st.dataframe(fd)
