# apiproject2402
# 프로젝트 배경 🏚️
 - 대한민국의 서울의 집값은 굉장히 비싸기 때문에 서울에서 집을 알아보는 입장이라면 시세를 정확히 알고 원하는 지역과 원하는 컨디션의 집을 자세히 알아봐야하는데 직접 모든 집의 시세를
   일일히 발품을 팔기엔 시간이 많이 소요될 것입니다.  
   서울열린데이터 광장의 '서울시 부동산 전월세가 정보' 데이터를 활용하여 대시보드를 개발하는 목적은 서울의 자치구/법정동별/건물용도별 시세를 빠르게 파악할 수 있도록 시각화하고
   최근 거래된 주변 건물명 데이터까지 보여줌으로 궁금했던 건물시세까지 직접 파악해볼 수 있습니다.
   이를 통해 서울에서 집을 알아보는 사용자에게 직접 발품을 팔기 전 서울의 지역별 전/월세 가격을 쉽게 파악하고 최적의 계획을 수립할 수 있도록 도와주기 위함입니다.

 ## 팀원 소개 🧑‍🤝‍🧑
- 박지건  : 깃허브 주소 공유
- 정주영  : 깃허브 주소 공유
- 김진아  : 깃허브 주소 공유 
- 원주성  : 깃허브 주소 공유 
- 곽정근  : 깃허브 주소 공유 
  
## 1. 본 프로젝트에서 사용한 주요 개발환경 ![파이썬](https://img.shields.io/badge/-Python-007396?style=flat&logo=Java&logoColor=ffffff) ![Streamlit](https://img.shields.io/badge/-Streamlit-3178C6?style=flat-square&logo=Streamlit&logoColor=red)
  - OS : Windows 10 & Mac (Linux에서는 테스트 하지 않았습니다.)
  - Programming Languages : Python(ver. 3.12.1)
  - Web Framework : Streamlit (ver. 1.31.0)

## 주요 라이브러리 버전
  + [requirements.txt](requirements.txt) 파일 참조


# 데모페이지
- Streamlit에서 구현한 Demo는 다음과 같습니다.
  + https://prj-seoulrealestate-jgp.streamlit.app/ (일단 지건님 페이지 넣어놓은것) 
 

 # 주요 기능(수정해야함)
 - 본 프로젝트에서 자체 개발 및 활용한 주요 메서드는 다음과 같습니다. 

| Functions | Location | Description |
|---|---|---|
| main | app.py  | for deploy |
| load_api | data_collect.py | for collecting data from API |

### main()
- main 함수는 ~~~
```python
def main():
   # 코드 설명
```
- 결과 이미지가 있으면 표시 

### data_collect()
-  data_collect() 함수는 ~~~~

# 발표자료 PDF (수정해야함) 
- 발표자료 PDF는 아래와 같습니다.
  + [00발표자료_2024](portfolio.pdf)


# Release Notes (수정해야함) 
- 개발 릴리스 노트는 `Releases` 클릭하여 확인하여 주시기를 바랍니다.
  + 참조 : https://github.com/dschloe/streamlit-api/releases
  + 작성방법 : https://docs.github.com/ko/repositories/releasing-projects-on-github/managing-releases-in-a-repository

# License (수정해야함) 
- 라이선스 링크 아웃링크로 처리
- [MIT Licence](LICENSE) 