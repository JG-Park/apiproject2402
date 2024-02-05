import requests
import json
import pandas as pd
from dotenv import load_dotenv
import os
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv('./data/data.csv')
    data = df.loc[:, ['SGG_NM',  # 자치구명
    'BJDONG_NM',  # 법정동명
    'CNTRCT_DE',  # 계약일
    'RENT_GBN',  # 전월세 구분
    'RENT_AREA',  # 임대면적
    'RENT_GTN',  # 보증금(만원)
    'RENT_FEE',  # 임대료(만원)
    'BUILD_YEAR',  # 건축년도
    'HOUSE_GBN_NM',  # 건물용도
    'BEFORE_GRNTY_AMOUNT',  # 종전보증금
    'BEFORE_MT_RENT_CHRGE']]  # 종전임대료

    data['평수'] = data['RENT_AREA'] * 0.3025
    data['평수_범주'] = pd.cut(data['평수'], bins=[1, 10, 20, 30, 40, 50, 60, float('inf')], labels=['10평 이하', '10평대', '20평대', '30평대', '40평대', '50평대', '60평대 이상'])

    return data

# data.head()

# 전월세 자치구별 월평균 비용
def jeonse(data, GBN_options, HOUSE_GBN_NM_options, AREA_values):
    # 조건에 따라 데이터 필터링
    filtered_data = data[(data['RENT_GBN'] == GBN_options) & (data['HOUSE_GBN_NM'].isin(HOUSE_GBN_NM_options)) & (data['평수'].between(AREA_values[0], AREA_values[1]))]

    # 자치구별 평균 RENT_GTN 계산
    avg_rent_by_sgg = filtered_data.groupby('SGG_NM')['RENT_GTN'].mean().reset_index()

    # 바 그래프 표시
    fig = px.bar(avg_rent_by_sgg, x='SGG_NM', y='RENT_GTN', labels={'x': '자치구', 'y': '평균 RENT_GTN'})
    st.plotly_chart(fig)

def rent(data, GBN_options, HOUSE_GBN_NM_options, AREA_values):
    # 조건에 따라 데이터 필터링
    filtered_data = data[(data['RENT_GBN'] == GBN_options) & (data['HOUSE_GBN_NM'].isin(HOUSE_GBN_NM_options)) & (data['평수'].between(AREA_values[0], AREA_values[1]))]

    # 'SGG_NM'별 'RENT_GTN'과 'RENT_FEE'의 평균 계산
    avg_rent_by_sgg = filtered_data.groupby('SGG_NM')[['RENT_GTN', 'RENT_FEE']].mean().reset_index()

    # 바 및 선 그래프 표시
    fig = px.bar(avg_rent_by_sgg, x='SGG_NM', y='RENT_GTN', labels={'x': 'SGG_NM', 'y': '평균 임대료'})
    fig.add_trace(go.Scatter(x=avg_rent_by_sgg['SGG_NM'], y=avg_rent_by_sgg['RENT_FEE'], mode='lines', name='평균 임대료', yaxis='y2'))

    # 보조축 레이아웃 설정
    fig.update_layout(yaxis2=dict(title='평균 임대료', overlaying='y', side='right'))

    # 그래프 표시
    st.plotly_chart(fig)

def main():
    data = load_data()
    # 옵션 선택
    st.title(':house_with_garden:어떤 동네로 갈까?')
    st.subheader('자치구별 시세')

    GBN_options = st.selectbox(
        '전.월세',
        ['전세', '월세'],
        key = 'GBN_options')

    HOUSE_GBN_NM_options = st.multiselect(
        '건물용도',
        ['단독다가구', '아파트', '오피스텔', '연립다세대'],
        key = 'HOUSE_GBN_NM_options')


    max_value = int(max(data['평수']))
    AREA_values = st.slider(
        '평수',
        0, max_value, (10, 20),
        key = 'AREA_values')

    # 옵션별 그래프
    if GBN_options == "전세":
        jeonse(data, GBN_options, HOUSE_GBN_NM_options, AREA_values)
    elif GBN_options == "월세":
        rent(data, GBN_options, HOUSE_GBN_NM_options, AREA_values)
    else:
        st.write("전.월세 타입을 선택하세요")

    #법정동별 시세
    st.subheader('법정동별 시세')

    GBN_options = st.selectbox(
        '전.월세',
        ['전세', '월세'])

    SGG_NM_options = st.multiselect(
        '자치구',
        data['SGG_NM'].unique().tolist())

    HOUSE_GBN_NM_options = st.multiselect(
        '건물용도',
        ['단독다가구', '아파트', '오피스텔', '연립다세대'])

    AREA_values = st.slider(
        '평수',
        0, max_value, (10, 20))

if __name__ == "__main__":
    main()



