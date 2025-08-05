import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FUE License Management", layout="wide")

# --- CSS 스타일 ---
st.markdown("""
<style>
/* 전체 배경 밝은 회색 */
.main > div.block-container {
    padding: 1.5rem 2rem;
    background-color: #f3f2f1;
    min-height: 100vh;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    color: #323130;
}

/* 상단 타이틀바 */
.topbar {
    background-color: white;
    padding: 1rem 2rem;
    display: flex;
    align-items: center;
    font-weight: 700;
    font-size: 24px;
    color: #0078d4; /* MS 블루 */
    box-shadow: 0 1px 3px rgb(0 0 0 / 0.1);
}

/* SAP 로고 느낌 텍스트 */
.topbar .sap-logo {
    font-weight: 900;
    margin-right: 12px;
    color: #0078d4;
    font-size: 28px;
}

/* 메뉴바 */
.menubar {
    background-color: white;
    padding-left: 2rem;
    padding-top: 0.5rem;
    display: flex;
    gap: 2rem;
    font-weight: 600;
    font-size: 16px;
    border-bottom: 1px solid #e1dfdd;
}

/* 메뉴 아이템 기본 */
.menubar .menu-item {
    padding-bottom: 0.5rem;
    color: #605e5c;
    cursor: pointer;
    position: relative;
}

/* 현재 활성화된 메뉴 스타일 */
.menubar .menu-item.active {
    color: #0078d4;
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
    background-color: #0078d4;
    border-radius: 3px 3px 0 0;
}

/* 위젯 박스 스타일 */
.widget {
    background-color: white;
    padding: 1.5rem;
    border: 1px solid #e1dfdd;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgb(0 0 0 / 0.05);
    margin-bottom: 1.8rem;
}

/* KPI 카드 컨테이너 - 가로 정렬 */
.kpi-cards {
    display: flex;
    flex-direction: row;
    gap: 1.5rem;
}

/* KPI 카드 */
.kpi-card {
    flex: 1;
    background-color: white;
    border: 1px solid #e1dfdd;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    text-align: center;
    box-shadow: 0 2px 6px rgb(0 0 0 / 0.04);
    transition: box-shadow 0.3s ease;
}

.kpi-card:hover {
    box-shadow: 0 6px 15px rgb(0 0 0 / 0.15);
}

.kpi-card h3 {
    margin-bottom: 0.4rem;
    font-weight: 600;
    color: #323130;
    font-size: 18px;
}

.kpi-card p {
    margin: 0;
    font-size: 28px;
    font-weight: 700;
    color: #0078d4;
}

/* 섹션 제목 */
.section-title {
    font-weight: 700;
    font-size: 22px;
    margin-bottom: 1rem;
    color: #323130;
}

/* Plotly 차트 배경 및 폰트 색상 */
.js-plotly-plot .main-svg {
    background-color: white !important;
}

/* 테이블 스타일은 Streamlit 기본 유지 */
</style>
""", unsafe_allow_html=True)

# --- 상단 타이틀바 ---
st.markdown("""
<div class="topbar">
    <div class="sap-logo">SAP</div>
    FUE License Management
</div>
""", unsafe_allow_html=True)

# --- 메뉴바 ---
menu_items = ["Home", "FUE License", "User", "My Account"]
selected_menu = st.session_state.get("selected_menu", "Home")

def set_menu(item):
    st.session_state.selected_menu = item

cols = st.columns(len(menu_items))
for i, item in enumerate(menu_items):
    is_active = (item == selected_menu)
    label_html = f'<div class="menu-item{" active" if is_active else ""}">{item}</div>'
    if cols[i].button(item, key=f"menu_{i}"):
        set_menu(item)
        st.experimental_rerun()
    cols[i].markdown(label_html, unsafe_allow_html=True)

# --- 데이터 로드 ---
@st.cache_data
def load_data():
    # Figma 참고 데이터 (예시)
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
if selected_menu == "Home":
    # KPI 카드 4개 가로 배치
    st.markdown('<div class="widget">', unsafe_allow_html=True)

    kpi_html = f'''
    <div class="kpi-cards">
        <div class="kpi-card">
            <h3>Total Licenses</h3>
            <p>{len(df)}</p>
        </div>
        <div class="kpi-card">
            <h3>Active</h3>
            <p>{df[df['Status']=="Active"].shape[0]}</p>
        </div>
        <div class="kpi-card">
            <h3>Expired</h3>
            <p>{df[df['Status']=="Expired"].shape[0]}</p>
        </div>
        <div class="kpi-card">
            <h3>Pending</h3>
            <p>{df[df['Status']=="Pending"].shape[0]}</p>
        </div>
    </div>
    '''
    st.markdown(kpi_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="widget">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Overview - License Status</div>', unsafe_allow_html=True)

    status_counts = df["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]

    fig_pie = px.pie(status_counts, names="Status", values="Count", hole=0.35,
                     color_discrete_map={
                         "Active": "#0078d4",
                         "Expired": "#d13438",
                         "Pending": "#ffb900"
                     })

    fig_bar = px.bar(status_counts, x="Status", y="Count", color="Status",
                     color_discrete_map={
                         "Active": "#0078d4",
                         "Expired": "#d13438",
                         "Pending": "#ffb900"
                     },
                     text="Count")
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(yaxis_title="Count", xaxis_title="Status", showlegend=False,
                          plot_bgcolor='white', paper_bgcolor='white',
                          font_color='#323130')

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_pie, use_container_width=True)
    with c2:
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="widget">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">License Table</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown(f'<div class="widget"><h2>{selected_menu} 페이지 준비중입니다.</h2></div>', unsafe_allow_html=True)
