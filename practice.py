# -*- encoding:utf-8 -*-
import requests
import json
import pandas as pd
from dotenv import load_dotenv
import os
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv('./data/data.csv', parse_dates=['CNTRCT_DE'])
    data = df.loc[:, ['SGG_NM',  # 자치구명
    'BJDONG_NM',  # 법정동명
    'CNTRCT_DE',  # 계약일
    'RENT_GBN',  # 전월세 구분
    'RENT_AREA',  # 임대면적
    'RENT_GTN',  # 보증금(만원)
    'RENT_FEE',  # 임대료(만원)
    'BLDG_NM', #건물명
    'BUILD_YEAR',  # 건축년도
    'HOUSE_GBN_NM',  # 건물용도
    'BEFORE_GRNTY_AMOUNT',  # 종전보증금
    'BEFORE_MT_RENT_CHRGE']]  # 종전임대료

    data['BLDG_NM'] = data['BLDG_NM'].fillna(data['HOUSE_GBN_NM'])  #건물명 비어있는 데이터는 건물용도 값 채워주기
    data['평수'] = data['RENT_AREA'] * 0.3025
    data['평수_범주'] = pd.cut(data['평수'], bins=[1, 10, 20, 30, 40, 50, 60, float('inf')], labels=['10평 이하', '10평대', '20평대', '30평대', '40평대', '50평대', '60평대 이상'])

    return data

def load_recent_data():
    data = load_data()
    # 데이터 중에서 가장 최근의 날짜 찾기
    latest_date = data['CNTRCT_DE'].max()
    # 최근 한 달 데이터 선택
    recent_data = data[data['CNTRCT_DE'] >= (latest_date - pd.DateOffset(days=30))]
    return recent_data


# 전세 자치구별 월평균 비용
def SGG_NM_jeonse(recent_data, GBN_options, HOUSE_GBN_NM_options, AREA_values):
    # 조건에 따라 데이터 필터링
    filtered_data = recent_data[(recent_data['RENT_GBN'] == GBN_options) 
                                & (recent_data['HOUSE_GBN_NM'].isin(HOUSE_GBN_NM_options)) 
                                & (recent_data['평수'].between(AREA_values[0], AREA_values[1]))]

    # 자치구별 평균 RENT_GTN 계산
    avg_rent_by_sgg = filtered_data.groupby('SGG_NM')['RENT_GTN'].mean().reset_index()

    # 바 그래프 표시
    fig = px.bar(avg_rent_by_sgg, x='SGG_NM', y='RENT_GTN', labels={'x': '자치구', 'y': '평균 RENT_GTN'})
    st.plotly_chart(fig)

# 월세 자치구별 월평균 비용
def SGG_NM_rent(recent_data, GBN_options, HOUSE_GBN_NM_options, AREA_values):
    # 조건에 따라 데이터 필터링
    filtered_data = recent_data[(recent_data['RENT_GBN'] == GBN_options) 
                                & (recent_data['HOUSE_GBN_NM'].isin(HOUSE_GBN_NM_options)) 
                                & (recent_data['평수'].between(AREA_values[0], AREA_values[1]))]

    # 'SGG_NM'별 'RENT_GTN'과 'RENT_FEE'의 평균 계산
    avg_rent_by_sgg = filtered_data.groupby('SGG_NM')[['RENT_GTN', 'RENT_FEE']].mean().reset_index()

    # 바 및 선 그래프 표시
    fig = px.bar(avg_rent_by_sgg, x='SGG_NM', y='RENT_GTN', labels={'x': 'SGG_NM', 'y': '평균 임대료'})
    fig.add_trace(go.Scatter(x=avg_rent_by_sgg['SGG_NM'], y=avg_rent_by_sgg['RENT_FEE'], mode='lines', name='평균 임대료', yaxis='y2'))

    # 보조축 레이아웃 설정
    fig.update_layout(yaxis2=dict(title='평균 임대료', overlaying='y', side='right'))

    # 그래프 표시
    st.plotly_chart(fig)

# 전월세별 법정동 데이터
def BJDONG_df(recent_data, GBN_options2, SGG_NM_options, HOUSE_GBN_NM_options2, AREA_values2):
    filtered_data2 = recent_data[(recent_data['RENT_GBN'] == GBN_options2) 
                            & (recent_data['SGG_NM'].isin(SGG_NM_options)) 
                            & (recent_data['HOUSE_GBN_NM'].isin(HOUSE_GBN_NM_options2))
                            & (recent_data['평수'].between(AREA_values2[0], AREA_values2[1]))]
    avg_rent_by_sgg2 = filtered_data2.groupby('BJDONG_NM').agg({'RENT_GTN': 'mean', 'RENT_FEE': 'mean'}).reset_index()
    avg_rent_by_sgg2 = avg_rent_by_sgg2.rename(columns={'BJDONG_NM' : '법정동','RENT_GTN': '평균 보증금', 'RENT_FEE': '평균 임대료'})
    st.table(avg_rent_by_sgg2)

def BLDG_df(recent_data, GBN_options3, SGG_NM_options2, HOUSE_GBN_NM_options3, BJDONG_NM_options, AREA_values3):
    filtered_data3 = recent_data[(recent_data['RENT_GBN'] == GBN_options3) 
                        & (recent_data['SGG_NM'].isin(SGG_NM_options2)) 
                        & (recent_data['HOUSE_GBN_NM'].isin(HOUSE_GBN_NM_options3))
                        & (recent_data['BJDONG_NM'].isin(BJDONG_NM_options))
                        & (recent_data['평수'].between(AREA_values3[0], AREA_values3[1]))]
    avg_rent_by_sgg3 = filtered_data3.groupby('BLDG_NM').agg({'RENT_GTN': 'mean', 'RENT_FEE': 'mean'}).reset_index()

    # recent_data에서 필요한 열을 선택하고, 'BJDONG_NM' 열을 추가
    additional_column = recent_data[['BLDG_NM', 'BJDONG_NM']]
    filtered_data3 = pd.merge(avg_rent_by_sgg3, additional_column, on='BLDG_NM', how='left')
    # 열 이름 변경 및 행 순서 변경
    avg_rent_by_sgg3 = filtered_data3.rename(columns={'BLDG_NM' : '건물명', 'BJDONG_NM' : '법정동명', 'RENT_GTN': '평균 보증금', 'RENT_FEE': '평균 임대료'})[['건물명', '법정동명', '평균 보증금', '평균 임대료']]
    st.table(avg_rent_by_sgg3)

def recent_value(recent_data, GBN_options4, SGG_NM_options3, HOUSE_GBN_NM_options4, BJDONG_NM_options2, AREA_values4, BLDG_NM_options):
    filtered_data4 = recent_data[(recent_data['RENT_GBN'] == GBN_options4) 
                    & (recent_data['SGG_NM'].isin(SGG_NM_options3)) 
                    & (recent_data['HOUSE_GBN_NM'].isin(HOUSE_GBN_NM_options4))
                    & (recent_data['BJDONG_NM'].isin(BJDONG_NM_options2))
                    & (recent_data['평수'].between(AREA_values4[0], AREA_values4[1]))
                    & (recent_data['BLDG_NM'].isin(BLDG_NM_options))]
    filtered_data4 = filtered_data4.loc[:, ['CNTRCT_DE', 'BLDG_NM', 'RENT_GTN', 'RENT_FEE']].reset_index(drop=True)
    filtered_data4 = filtered_data4.rename(columns={'CNTRCT_DE': '날짜', 'BLDG_NM' : '건물명', 'RENT_GTN': '보증금', 'RENT_FEE': '임대료'})
    st.table(filtered_data4)
    

def page1(recent_data):
    # 자치구별 시세
    st.title(':house_with_garden:어떤 동네로 갈까?')
    st.subheader('자치구별 시세')

    GBN_options = st.selectbox(
        '전.월세',
        recent_data['RENT_GBN'].unique(),
        key='selectbox_GBN')

    HOUSE_GBN_NM_options = st.multiselect(
        '건물용도',
        recent_data['HOUSE_GBN_NM'].unique(),
        key='multiselect_HOUSE_GBN_NM')

    max_value = int(max(recent_data['평수']))
    AREA_values = st.slider(
        '평수',
        0, max_value, (10, 20),
        key = 'slider_AREA')

    # 옵션별 그래프
    if GBN_options == "전세":
        SGG_NM_jeonse(recent_data, GBN_options, HOUSE_GBN_NM_options, AREA_values)
    elif GBN_options == "월세":
        SGG_NM_rent(recent_data, GBN_options, HOUSE_GBN_NM_options, AREA_values)
    else:
        st.write("전.월세 타입을 선택하세요")

#법정동별 시세
    st.subheader('법정동별 시세')

    GBN_options2 = st.selectbox(
    '전.월세',
    recent_data['RENT_GBN'].unique(),
    key='selectbox_GBN2')  

    SGG_NM_options = st.multiselect(
        '자치구',
        recent_data['SGG_NM'].unique().tolist(),
        key='multiselect_HOUSE_SGG_NM')

    HOUSE_GBN_NM_options2 = st.multiselect(
        '건물용도',
        recent_data['HOUSE_GBN_NM'].unique(),
        key='multiselect_HOUSE_GBN_NM2')

    AREA_values2 = st.slider(
        '평수',
        0, max_value, (10, 20),
        key='slider_AREA2')
    
    BJDONG_df(recent_data, GBN_options2, SGG_NM_options, HOUSE_GBN_NM_options2, AREA_values2)

def page2(recent_data):
    st.title(':house_with_garden:어떤 집이 좋을까?')
    st.subheader('건물별 평균 시세')

    GBN_options3 = st.selectbox(
        '전.월세',
        recent_data['RENT_GBN'].unique(),
        key='selectbox_GBN3')  

    SGG_NM_options2 = st.multiselect(
        '자치구',
        recent_data['SGG_NM'].unique().tolist(),
        key='multiselect_HOUSE_SGG_NM2')
    
    BJDONG_NM_options = st.multiselect(
        '법정동',
        recent_data['BJDONG_NM'].unique().tolist(),
        key='multiselect_BJDONG_NM')

    HOUSE_GBN_NM_options3 = st.multiselect(
        '건물용도',
        recent_data['HOUSE_GBN_NM'].unique(),
        key='multiselect_HOUSE_GBN_NM3')

    max_value = int(max(recent_data['평수']))
    AREA_values3 = st.slider(
        '평수',
        0, max_value, (10, 20),
        key='slider_AREA3')
    
    BLDG_df(recent_data, GBN_options3, SGG_NM_options2, HOUSE_GBN_NM_options3, BJDONG_NM_options, AREA_values3)

def page3(recent_data):
    st.title('최근 거래 현황')

    GBN_options4 = st.selectbox(
        '전.월세',
        recent_data['RENT_GBN'].unique(),
        key='selectbox_GBN4')  

    SGG_NM_options3 = st.multiselect(
        '자치구',
        recent_data['SGG_NM'].unique().tolist(),
        key='multiselect_HOUSE_SGG_NM3')
    
    BJDONG_NM_options2 = st.multiselect(
        '법정동',
        recent_data['BJDONG_NM'].unique().tolist(),
        key='multiselect_BJDONG_NM2')

    HOUSE_GBN_NM_options4 = st.multiselect(
        '건물용도',
        recent_data['HOUSE_GBN_NM'].unique(),
        key='multiselect_HOUSE_GBN_NM4')
    
    BLDG_NM_options = st.multiselect(
        '건물명',
        recent_data['BLDG_NM'].unique(),
        key='multiselect_BLDG_NM')

    max_value = int(max(recent_data['평수']))
    AREA_values4 = st.slider(
        '평수',
        0, max_value, (10, 20),
        key='slider_AREA4')
    
    recent_value(recent_data, GBN_options4, SGG_NM_options3, HOUSE_GBN_NM_options4, BJDONG_NM_options2, AREA_values4, BLDG_NM_options)
    
    



def main():

    with st.sidebar:
        choice = option_menu("Menu", ["동네별 시세", "건물별 시세", "최근 거래 현황"],
                            icons=['house', 'kanban'],
                            menu_icon="app-indicator", default_index=0,
                            styles={
            "container": {"padding": "4!important", "background-color": "#fafafa"},
            "icon": {"color": "black", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
            "nav-link-selected": {"background-color": "#08c7b4"},
        }
        )

    recent_data = load_recent_data()

    if choice == "동네별 시세":
        page1(recent_data)
    
    if choice == "건물별 시세":
        page2(recent_data)

    if choice == "최근 거래 현황":
        page3(recent_data)



if __name__ == "__main__":
    main()



