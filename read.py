# -*- encoding:utf-8 -*-
import requests
import json
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()
SEORUL_SERVICE_KEY = os.getenv('SEORUL_SERVICE_KEY')

# API 크롤링
def fetch_data(start, end):
    URL = f'http://openapi.seoul.go.kr:8088/{SEORUL_SERVICE_KEY}/json/tbLnOpendataRentV/{start}/{end}/'
    req = requests.get(URL)
    content = req.json()
    # 데이터 추출 및 DataFrame으로 변환
    return pd.DataFrame(content['tbLnOpendataRentV']['row'])


# 데이터 수집

data = None
start = 130001
end = 260000
for i in range(start, end+1, 1000):
    result = fetch_data(i, i+999)
    data = pd.concat([data, result], ignore_index=True)

data = data.reset_index(drop = True)
data.to_csv('./data/data1.csv', encoding='euc-kr', index = False)



# 데이터 합치기

data1 = pd.read_csv('./data/data1.csv', encoding='euc-kr')
data2 = pd.read_csv('./data/data2.csv', encoding='euc-kr')
data3 = pd.read_csv('./data/data3.csv')
data4 = pd.read_csv('./data/data4.csv')

merged_data = pd.concat([data1, data2, data3, data4], ignore_index=True)

merged_data.to_csv('./data/merged_data.csv', encoding='utf-8', index=False)
