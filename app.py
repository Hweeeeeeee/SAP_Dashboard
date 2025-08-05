import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FUE License Management", layout="wide")

# --- CSS 스타일 (어두운 톤, 카드 스타일) ---
st.markdown("""
<style>
/* 페이지 배경과 텍스트 */
[data-testid="stAppViewContainer"] {
    background-color: #121212;
    color: #e0e0e0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 사이드바 배경 및 텍스트 */
[data-testid="stSidebar"] {
    background-color: #1f2937;
    color: #e0e0e0;
    padding-top: 2rem;
    font-weight: 600;
}

/* 사이드바 메뉴 아이템 */
.sidebar .sidebar-content > div {
    margin-bottom: 1rem;
}

.sidebar .sidebar-content div.stRadio > label {
    color: #cbd5e1;
    font-weight: 600;
}

.sidebar .sidebar-content div.stRadio > label:hover {
    color: #3b82f6;
}

/* 본문 영역 여백 */
.main > div.block-container {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
}

/* 카드 공통 스타일 */
.card {
    background-color: #1e293b;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    color: #e0e0e0;
    text-align: center;
}

/* 카드 제목 */
.card h3 {
    margin-bottom: 0.5rem;
    font-weight: 700;
    color: #60a5fa;
}

/* 카드 숫자 */
.card p {
    font-size: 28px;
    font-weight: 700;
    margin: 0;
    color: #3b82f6;
}

/* 섹션 제목 */
.section-title {
    font-weight: 700;
    font-size: 22px;
    margin-bottom: 1rem;
    color: #93c5fd;
}

/* Plotly 차트 배경 및 텍스트 맞춤 */
.js-plotly-plot .main-svg {
    background-color: #1e293b !important;
}

</style>
""", unsafe_allow_html=True)

# --- 사이드바 ---
with st.sidebar:
    st.markdown("# 🚀 FUE License")
    menu = st.radio("Menu", ["Home", "FUE License", "User", "My Account"])

    st.markdown("---")
    st.markdown("### User Profile")
    st.write("Jane Doe")
    st.write("jane.doe@example.com")

# --- 데이터 로드 ---
@st.cache_data
def load_data():
    # Figma 기반 예시 데이터 구조
    data = {
        "LicenseID": [1,2,3,4,5,6,7,8,9,10],
        "User": ["Alice","Bob","Carol","David","Eve","Frank","Grace","Hank","Ivy","Jack"],
        "Status": ["Active","Expired","Active","Pending","Active","Expired","Pending","Active","Active","Expired"],
        "StartDate": ["2023-01-10","2022-05-15","2023-03-12","2023-06-01","2023-02-20","2021-12-30","2023-07-10","2023-04-01","2023-05-05","2022-11-11"],
        "EndDate": ["2024-01-09","2023-05-14","2024-03-11","2023-07-01","2024-02-19","2022-12-29","2023-08-10","2024-04-01","2024-05-04","2023-11-10"],
    }
    return pd.DataFrame(data)

df = load_data()

# --- 본문 ---
st.title(f"FUE License Management - {menu}")

if menu == "Home":
    # KPI 카드 4개 가로 배치
    col1, col2, col3, col4 = st.columns(4, gap="large")
    with col1:
        st.markdown(f'''
        <div class="card">
            <h3>Total Licenses</h3>
            <p>{len(df)}</p>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div class="card">
            <h3>Active</h3>
            <p>{df[df['Status'] == 'Active'].shape[0]}</p>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
        <div class="card">
            <h3>Expired</h3>
            <p>{df[df['Status'] == 'Expired'].shape[0]}</p>
        </div>
        ''', unsafe_allow_html=True)
    with col4:
        st.markdown(f'''
        <div class="card">
            <h3>Pending</h3>
            <p>{df[df['Status'] == 'Pending'].shape[0]}</p>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-title">Overview - License Status</div>', unsafe_allow_html=True)
    status_counts = df['Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']

    # 원형 차트
    fig_pie = px.pie(status_counts, names='Status', values='Count', hole=0.5,
                     color_discrete_map={
                         "Active": "#3b82f6",
                         "Expired": "#ef4444",
                         "Pending": "#fbbf24"
                     })

    # 막대 차트
    fig_bar = px.bar(status_counts, x='Status', y='Count', color='Status',
                     color_discrete_map={
                         "Active": "#3b82f6",
                         "Expired": "#ef4444",
                         "Pending": "#fbbf24"
                     },
                     text='Count')
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(yaxis_title='Count', xaxis_title='Status', showlegend=False,
                          plot_bgcolor='#1e293b', paper_bgcolor='#1e293b',
                          font_color='#e0e0e0')

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    st.markdown('<div class="section-title">License Table</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

else:
    st.info("This menu content is under construction.")

