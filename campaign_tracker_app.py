"""
Marketing Campaign Performance Tracker (Streamlit)

Features:
- Upload your campaign CSV or use sample data
- Calculates CPA, ROI, Conversion Rate
- Visualizes campaign performance per channel and over time
- Download summary CSV report
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title='Campaign Performance Tracker', layout='wide')
st.title('📊 Marketing Campaign Performance Tracker')

# ---------- Sidebar ----------
st.sidebar.header('Data Options')
use_sample = st.sidebar.checkbox('Use sample campaign data', value=True)
uploaded_campaigns = st.sidebar.file_uploader('Upload your campaign CSV', type=['csv'])

# ---------- Sample Data ----------
def sample_campaigns():
    data = {
        'campaign_id': [f'camp_{i+1}' for i in range(6)],
        'start_date': pd.date_range('2025-01-01', periods=6, freq='7D'),
        'end_date': pd.date_range('2025-01-07', periods=6, freq='7D'),
        'channel': ['Facebook', 'Google', 'Instagram', 'Email', 'Google', 'Facebook'],
        'spend': [1200, 900, 700, 400, 1500, 1000],
        'conversions': [40, 30, 25, 15, 45, 35],
        'revenue': [4000, 3200, 2800, 1500, 5000, 3800]
    }
    df = pd.DataFrame(data)
    return df

# ---------- Load Data ----------
if use_sample:
    df_campaigns = sample_campaigns()
else:
    if uploaded_campaigns:
        df_campaigns = pd.read_csv(uploaded_campaigns)
    else:
        st.info('Please upload a CSV or use sample data')
        df_campaigns = None

# ---------- Campaign Overview ----------
if df_campaigns is not None:
    df_campaigns['start_date'] = pd.to_datetime(df_campaigns['start_date'])
    df_campaigns['end_date'] = pd.to_datetime(df_campaigns['end_date'])
    st.subheader('Campaign Data Preview')
    st.dataframe(df_campaigns)

    # ---------- Metrics ----------
    st.subheader('Campaign KPIs')
    df_campaigns['CPA'] = (df_campaigns['spend'] / df_campaigns['conversions']).round(2)
    df_campaigns['ROI'] = ((df_campaigns['revenue'] - df_campaigns['spend']) / df_campaigns['spend']).round(2)
    df_campaigns['Conversion_Rate'] = (df_campaigns['conversions'] / df_campaigns['conversions'].sum()).round(4)

    st.dataframe(df_campaigns[['campaign_id', 'channel', 'spend', 'conversions', 'CPA', 'ROI', 'Conversion_Rate']])

    # ---------- Visualization ----------
    st.subheader('ROI by Channel')
    roi_channel = df_campaigns.groupby('channel')['ROI'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots()
    roi_channel.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_ylabel('Average ROI')
    st.pyplot(fig)

    st.subheader('Conversions Over Time')
    conv_time = df_campaigns.groupby('start_date')['conversions'].sum()
    fig2, ax2 = plt.subplots()
    conv_time.plot(kind='line', marker='o', ax=ax2)
    ax2.set_ylabel('Conversions')
    ax2.set_xlabel('Start Date')
    st.pyplot(fig2)

    # ---------- Filters ----------
    st.subheader('Filter Campaigns')
    channels = df_campaigns['channel'].unique().tolist()
    selected_channels = st.multiselect('Select Channels', channels, default=channels)
    filtered_df = df_campaigns[df_campaigns['channel'].isin(selected_channels)]
    st.dataframe(filtered_df)

    # ---------- Download Summary ----------
    st.subheader('Download Summary Report')
    summary = filtered_df.groupby('channel').agg({
        'spend':'sum',
        'conversions':'sum',
        'revenue':'sum'
    }).reset_index()
    summary['CPA'] = (summary['spend'] / summary['conversions']).round(2)
    summary['ROI'] = ((summary['revenue'] - summary['spend']) / summary['spend']).round(2)

    csv_buf = summary.to_csv(index=False).encode('utf-8')
    st.download_button('Download Campaign Summary CSV', data=csv_buf, file_name='campaign_summary.csv', mime='text/csv')

st.markdown('---')
st.caption('This app helps marketing analysts track campaign performance and make data-driven decisions.')
