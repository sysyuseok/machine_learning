
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://news.daum.net"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'

def get_news_list():
    """
    daum 뉴스 목록 조회
    조회결과는 pandas의 DataFrame(표) 로 만들어서 반환.
    """

    # 요청 - 가장 중요한 부분!
    response = requests.get(url, headers={'User-Agent':user_agent})
    # 상태코드가 200 인지 확인.
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml') #마크업언어?
        #이하 내용은 원하는 내용 찾아내는 것이다.
        tag_list = soup.select("ul.list_newsissue > li strong > a") #f12 눌러서 보면서 원하는 정보가 어디 위치 한지 찾아내야한다.
        print(len(tag_list))
        link_list = []
        title_list = []
        for tag in tag_list:
            link_list.append(tag.get("href")) #링크는 여기
            title_list.append(tag.get_text().strip()) # 기사 제목은 여기 , tag사이에 중간 내용을 가져 오는 부분이고 공백을 제거한다.
            
        return pd.DataFrame({
            "title":title_list, #2열짜리 table을 만든것
            "link":link_list
        })
    else:
        print("문제발생:", response.status_code)

def get_news(url):
    """
    new 상세 기사 url을 받아서 new 내용을 return
    """
    response = requests.get(url,headers={"User-Agent":user_agent})
    if response.status_code==200:
        soup = BeautifulSoup(response.text,"lxml")
        p_list = soup.select("div.article_view p") #p tag들을 넘겨 받는다.

        article = [] # list에 p의 text들을 저장한다.
        for p in p_list: #p tag를 그대로 article에 넣어준다.
            article.append(p.get_text())
        #list 안의 text들을 합쳐서 하나의 문자열로 만든다.
        return " ".join(article)


        
if __name__ == "__main__":
    # news 목록을 저장
    from datetime import datetime 
    import os
    import re
    import time

    #########목록을 가져오는 부분###########
    d = datetime.now().strftime("%Y-%m-%d")  # strftime(): 날짜시간을 원하는 형태의 문자열로 변환.
    file_path = f"./02_web/daum_new_list_{d}.csv"
    print(file_path)
    result = get_news_list()
    # # csv 파일로 저장
    result.to_csv(file_path, index=False) #utf-8 형식으로 저장. 번호 넣는 것을 막는 부분

    ######### 개별 news 기사를 저장 ###############
    # result : DataFrame에서 link를 조회 
    links = result["link"] #표["column name"]==> column들의 값들을 반환

    start = time.time()
    result_news=[ get_news(link) for link in links]
    end=time.time()
    print("기사 가져오는데 걸리는 시간",end-start,"seconds")
    # print(len(result_news))
    # print(result_news[0])


    save_path=f"./02_web/news/{d}"
    # 날짜이름으로 news/directory를 생성
    os.makedirs(save_path,exist_ok=True) #이미 존재하면 만들지 않는데 오류 발생 하지 않음 (True 옵션으로)
    titles = result["title"] #news제목 #파일명에 '가 들어가는 문제가 생성
    for title,news in zip(titles, result_news):
        title = re.sub('[^\w]','',title)
        with open(f"{save_path}/{title}.txt","wt",encoding='utf-8') as fw: 
            fw.write(news)

    print("done")







