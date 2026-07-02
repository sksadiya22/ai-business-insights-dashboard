import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1] / 'python'))
from retail_data_pipeline import clean_sales_data, create_sample_dataset, load_csv_to_dataframe

st.set_page_config(page_title='AI Business Insights Dashboard', layout='wide')

st.title('AI Business Insights Dashboard')

st.sidebar.image('https://via.placeholder.com/250x120?text=Retail+Analytics', use_container_width=True)
st.sidebar.markdown('### Navigation')
page = st.sidebar.radio('Go to', ['Dashboard Home', 'Upload Dataset', 'Business KPIs', 'AI Insights', 'Download AI Report'])

if page == 'Dashboard Home':
    st.markdown('This demo project combines Python, SQL, Power BI, and Gemini to deliver a simple business insights workflow for retail sales data.')
    st.info('Use the sidebar to upload a CSV file or generate the sample dataset to explore the workflow.')

elif page == 'Upload Dataset':
    uploaded_file = st.file_uploader('Upload a retail sales CSV file', type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        cleaned = clean_sales_data(df)
        st.success('Dataset cleaned successfully.')
        st.dataframe(cleaned.head())
        st.download_button('Download cleaned CSV', data=cleaned.to_csv(index=False).encode('utf-8'), file_name='cleaned_retail_sales.csv', mime='text/csv')
    else:
        sample_path = create_sample_dataset()
        st.caption(f'Sample dataset ready at {sample_path}')
        df = pd.read_csv(sample_path)
        st.dataframe(df.head())

elif page == 'Business KPIs':
    sample_path = create_sample_dataset()
    df = load_csv_to_dataframe(sample_path)
    cleaned = clean_sales_data(df)
    st.subheader('Key Metrics')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Total Sales', f"${cleaned['Sales'].sum():,.2f}")
    col2.metric('Total Profit', f"${cleaned['Profit'].sum():,.2f}")
    col3.metric('Total Orders', f"{cleaned['Order ID'].nunique()}")
    col4.metric('Average Order Value', f"${(cleaned['Sales'].sum() / cleaned['Order ID'].nunique()):,.2f}")

    st.subheader('Tables')
    tab1, tab2, tab3 = st.tabs(['Top Products', 'Regional Sales', 'Category Performance'])
    with tab1:
        st.dataframe(cleaned.groupby('Product')['Sales'].sum().sort_values(ascending=False).reset_index().head(10))
    with tab2:
        st.dataframe(cleaned.groupby('Region')['Sales'].sum().sort_values(ascending=False).reset_index())
    with tab3:
        st.dataframe(cleaned.groupby('Category').agg(total_sales=('Sales', 'sum'), total_profit=('Profit', 'sum')).reset_index())

elif page == 'AI Insights':
    sample_path = create_sample_dataset()
    df = load_csv_to_dataframe(sample_path)
    cleaned = clean_sales_data(df)
    st.subheader('Gemini AI Business Summary')
    metrics = {
        'total_sales': round(float(cleaned['Sales'].sum()), 2),
        'total_profit': round(float(cleaned['Profit'].sum()), 2),
        'top_products': cleaned.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(3).to_dict(),
        'top_regions': cleaned.groupby('Region')['Sales'].sum().sort_values(ascending=False).head(3).to_dict(),
        'category_sales': cleaned.groupby('Category')['Sales'].sum().sort_values(ascending=False).to_dict(),
    }
    st.json(metrics)
    st.markdown('The app is ready for Gemini integration. Add your API key in the environment as GEMINI_API_KEY to enable AI summaries.')

elif page == 'Download AI Report':
    st.markdown('This section is ready to export a business summary report once the Gemini API key is configured.')
    st.download_button('Download sample report', data='Executive Summary\n- Sales performance is healthy.\n- Profitability is improving in key categories.\n', file_name='ai_business_report.txt', mime='text/plain')
