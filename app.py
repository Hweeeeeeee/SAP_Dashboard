import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FUE License Management", layout="wide")

# --- 스타일 전체 적용 ---
st.markdown("""
<style>
/* 전체 배경 연한 회색 */
.main > div.block-container {
    padding-top: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
    background-color: #f5f6f8;
    min-height: 100vh;
}

/* 상단 타이틀바 */
.topbar {
    background-color: white;
    padding: 1rem 2rem;
    display: flex;
    align-items: center;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 700;
    font-size: 24px;
    color: #005fb8; /* SAP 파란색 계열 */
    box-shadow: 0 2px 4px rgb(0 0 0 / 0.1);
}

/* SAP 로고 느낌 텍스트 스타일 (간단히 텍스트로 대체) */
.topbar .sap-logo {
    font-weight: 900;
    margin-right: 12px;
    color: #0a53be;
}

/* 메뉴바 */
.menubar {
    background-color: white;
    padding-left: 2rem;
    padding-top: 0.5rem;
    display: flex;
    gap: 2rem;
    font-weight: 600;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 16px;
    border-bottom: 1px solid #e1e3e6;
}

/* 메뉴 아이템 기본 */
.menubar .menu-item {
    padding-bottom: 0.5rem;
    color: #606770;
    cursor: pointer;
    position: relative;
}

/* 현재 활성화된 메뉴 스타일 */
.menubar .menu-item.active {
    color: #005fb8;
    font-weight: 700;
}

/* 활성화 메뉴 밑 파란 언더라인 */
.menubar .menu-item.active::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background-color: #005fb8;
    border-radius: 3px 3px 0 0;
}

/* 컨텐츠 위젯 스타일 */
.widget {
    background-color: white;
    padding: 1.5rem;
    border: 1px solid #d4d7db; /* 연한 회색 테두리 */
    border-radius: 8px;
    box-shadow: 0 2px 8px rgb(0 0 0 / 0.05);
    margin-bottom: 2rem;
}

/* KPI 카드 스타일 */
.kpi-cards {
    display: flex;
    gap: 1.5rem;
}

.kpi-card {
    flex: 1;
    background-color: white;
    border: 1px solid #d4d7db;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgb(0 0 0 / 0.04);
    padding: 1rem 1.5rem;
    text-align: center;
}

.kpi-card h3 {
    margin-bottom: 0.4rem;
    font-weight: 600;
    color: #333;
    font-size: 18px;
}

.kpi-card p {
    margin: 0;
    font-size: 28px;
    font-weight: 700;
    color: #005fb8;
}

/* 차트 섹션 제목 */
.section-title {
    font-weight: 700;
    font-size: 22px;
    margin-bottom: 1rem;
    color: #222;
}

</style>
""", unsafe_allow_html=True)

# --- 상단 타이틀바 (SAP 로고 텍스트 대체) ---
st.markdown("""
<div class="topbar">
    <div class="sap-logo">SAP</div>
    FUE License Management
</div>
""", unsafe_allow_html=True)

# --- 메뉴바 ---
st.markdown("""
<div class="menubar">
    <div class="menu-item active">Home</div>
    <div class="menu-item">FUE License</div>
    <div class="menu-item">User</div>
    <div class="menu-item">My Account</div>
</div>
""", unsafe_allow_html=True)

# --- 데이터 로드 ---
@st.cache_data
def load_data():
    return pd.read_csv("licenses.csv")

df = load_data()

# --- KPI 카드 영역 (widget) ---
st.markdown('<div class="widget">', unsafe_allow_html=True)
st.markdown('<div class="kpi-cards">', unsafe_allow_html=True)

def kpi_card(title, value):
    return f'''
    <div class="kpi-card">
        <h3>{title}</h3>
        <p>{value}</p>
    </div>
    '''

kpi_html = ""
kpi_html += kpi_card("Total Licenses", len(df))
kpi_html += kpi_card("Active", df[df['Status']=='Active'].shape[0])
kpi_html += kpi_card("Expired", df[df['Status']=='Expired'].shape[0])
kpi_html += kpi_card("Pending", df[df['Status']=='Pending'].shape[0])

st.markdown(kpi_html, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Overview 차트 영역 (widget) ---
st.markdown('<div class="widget">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Overview - License Status</div>', unsafe_allow_html=True)

# 원형 차트
status_counts = df["Status"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]

fig_pie = px.pie(status_counts, names="Status", values="Count", hole=0.35,
                 color_discrete_map={
                     "Active": "#005fb8",
                     "Expired": "#d9534f",
                     "Pending": "#f0ad4e"
                 })

# 막대 차트
fig_bar = px.bar(status_counts, x="Status", y="Count", 
                 color="Status",
                 color_discrete_map={
                     "Active": "#005fb8",
                     "Expired": "#d9534f",
                     "Pending": "#f0ad4e"
                 },
                 text="Count"
                )
fig_bar.update_traces(textposition='outside')
fig_bar.update_layout(yaxis=dict(title="Count"), xaxis=dict(title="Status"), showlegend=False)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_pie, use_container_width=True)
with col2:
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- License Table 영역 (widget) ---
st.markdown('<div class="widget">', unsafe_allow_html=True)
st.markdown('<div class="section-title">License Table</div>', unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
