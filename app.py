import streamlit as st
import pandas as pd
import altair as alt
from io import StringIO

# --- CSS 스타일 (카드 스타일링 등) ---
st.markdown(
    """
    <style>
    .card {
        background: white;
        padding: 20px;
        margin: 10px 5px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .title {
        font-size: 22px;
        font-weight: 700;
        color: #333333;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 14px;
        color: #666666;
        margin-bottom: 20px;
    }
    .stat {
        font-size: 18px;
        font-weight: 600;
        color: #0078D4;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- 샘플 데이터 ---
license_summary_csv = """
License_Type,Total_Licenses,Used,Remaining,Expiry_Date,Status
Office365,1000,800,200,2025-12-31,Active
Adobe,500,450,50,2025-09-30,Active
SAP,300,280,20,2024-06-30,Expired
"""

df_summary = pd.read_csv(StringIO(license_summary_csv))

# --- 타이틀 ---
st.title("License Management Dashboard")
st.markdown("---")

# --- 카드 UI로 라이선스 요약 ---
st.header("License Summary")

cols = st.columns(len(df_summary))  # 카드 가로 배치

for idx, row in df_summary.iterrows():
    with cols[idx]:
        st.markdown(f"""
        <div class="card">
            <div class="title">{row['License_Type']}</div>
            <div class="subtitle">Expiry: {row['Expiry_Date']}</div>
            <div>Total Licenses: <span class="stat">{row['Total_Licenses']}</span></div>
            <div>Used: <span class="stat">{row['Used']}</span></div>
            <div>Remaining: <span class="stat">{row['Remaining']}</span></div>
            <div>Status: <span class="stat">{row['Status']}</span></div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# --- 간단한 Altair 차트 예시 ---
st.header("License Usage Trend")

license_trend_csv = """
Date,License_Type,Used_Count
2025-01-01,Office365,750
2025-02-01,Office365,770
2025-03-01,Office365,800
2025-01-01,Adobe,420
2025-02-01,Adobe,430
2025-03-01,Adobe,450
2025-01-01,SAP,270
2025-02-01,SAP,275
2025-03-01,SAP,280
"""

df_trend = pd.read_csv(StringIO(license_trend_csv))
df_trend['Date'] = pd.to_datetime(df_trend['Date'])

chart = alt.Chart(df_trend).mark_line(point=True).encode(
    x='Date:T',
    y='Used_Count:Q',
    color='License_Type:N',
    tooltip=['Date:T', 'License_Type:N', 'Used_Count:Q']
).properties(
    width=700,
    height=350
).interactive()

st.altair_chart(chart)

st.markdown("---")

# --- 상세 테이블 (심플 스타일) ---
st.header("License Details")

license_detail_csv = """
License_ID,License_Type,Assigned_User,Assigned_Date,Expiry_Date,Status
0001,Office365,kim@company.com,2024-01-01,2025-12-31,Active
0002,Adobe,lee@company.com,2024-03-15,2025-09-30,Active
0003,SAP,park@company.com,2023-07-10,2024-06-30,Expired
0004,Office365,choi@company.com,2024-05-22,2025-12-31,Active
"""

df_detail = pd.read_csv(StringIO(license_detail_csv))
df_detail['Assigned_Date'] = pd.to_datetime(df_detail['Assigned_Date'])
df_detail['Expiry_Date'] = pd.to_datetime(df_detail['Expiry_Date'])

st.dataframe(df_detail.style.set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0078D4'), ('color', 'white')]},
    {'selector': 'tbody tr:hover', 'props': [('background-color', '#f0f8ff')]},
]))