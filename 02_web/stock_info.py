#https://finance.naver.com/sise/sise_market_sum.naver?&page={} page뒤에 숫자를 조절해서 크롤링한다.
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

urlo = "https://finance.naver.com/sise/sise_market_sum.naver?&page="
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'


def get_info_list():
    
    """
    시가 총액 순으로 정렬된 주식 정보를 크롤링 41페이지 까지 존재
    """
    for i in range(1,42): # 1페이지부터 41페이지 까지
        url=urlo+str(i)
        print(url)
        # 요청 - 가장 중요한 부분!
        response = requests.get(url, headers={'User-Agent':user_agent}) #header 에는 본인정보 - window or android같은 os부터 검색 엔진까지
        #body에는 요청정보 - 어떤 정보를 얻을 것인지
        # 상태코드가 200 인지 확인.
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.text, 'lxml') #마크업언어? #parcing하기 위해 beautiful soup한다. 원본상태로 저장
            #이하 내용은 원하는 내용 찾아내는 것이다.
            
            tag_list = soup.select("div.box_type_1 tbody > tr") #f12 눌러서 보면서 원하는 정보가 어디 위치 한지 찾아내야한다.
            #적당 위치 잡고 copy selector 통해서 위치 관계 잡고 좀 더 세부적으로 찾기
            print(len(tag_list))
            print(tag_list)
            # link_list = []
            # title_list = []
            # for tag in tag_list:
            #     link_list.append(tag.get("href")) #링크는 여기
            #     title_list.append(tag.get_text().strip()) # 기사 제목은 여기 , tag사이에 중간 내용을 가져 오는 부분이고 공백을 제거한다.
            
            # return pd.DataFrame({
            #     "title":title_list, #2열짜리 table을 만든것
            #     "link":link_list
            # })
        else:
            print("문제발생:", response.status_code)


get_info_list()