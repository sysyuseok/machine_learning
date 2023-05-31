# daum_news_async.py
# 뉴스 목록 csv 파일에 저장된 링크들의 뉴스들을 aiohttp를 이용해서 크롤링
# 네트워크 작업을 비동기로 진행하기 위한 코드

import pandas as pd
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time

async def get_news(url, session):
    # url의 개별 뉴스를 크롤링하는 co-routine 함수
    # 연결 요청
    async with session.get(url) as response:
        if response.status == 200:
            html=await response.text()
            soup= BeautifulSoup(html,"lxml")
            p_list = soup.select("div.article_view p") #p tag들을 넘겨 받는다.

            article = [] # list에 p의 text들을 저장한다.
            for p in p_list: #p tag를 그대로 article에 넣어준다.
                article.append(p.get_text())
            #list 안의 text들을 합쳐서 하나의 문자열로 만든다.
            return "\n\n".join(article)
    
async def main(links):
    # main routine
    # news 링크 개수만큼 get_news() co-routine을 생성해서 event Loop을 이용해 실행
    
    async with aiohttp.ClientSession() as sess:
        #20개의 co-routine을 생성한 뒤에 event loop에 넣어서 실행
        result=await asyncio.gather(*[ get_news(link,sess) for link in links])
        #result:list - 에는 20개의 뉴스 기사
        print(type(result))
    return result

if __name__=="__main__":
    #csv 파일을 읽어서 DataFrame을 생성
    df=pd.read_csv("./02_web/daum_new_list_2023-04-19.csv")
    print(df)

    links=df["link"] #link 컬럼의 값들을 조회
    print(links)

    start = time.time()
    result= asyncio.run(main(links))
    end = time.time()
    print(end-start,"sec")
    



