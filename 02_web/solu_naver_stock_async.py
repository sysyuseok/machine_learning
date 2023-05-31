# ##################################################################
# Naver 증권 -> 코스피 시가총액 순으로 조회
#    ROOT: URL: https://finance.naver.com/sise/sise_market_sum.naver
#    페이지 이동:     ?&page=2
#    총 41 페이지

# Table column 
# 1. NO
# 2. 종목명
# 3. 현재가
# 4. 전일비
# 5. 등락률
# 6. 액면가
# 7. 시가총액
# 8. 상장주식수
# 9. 외국인비율
# 10.거래량
# 11.PER
# 12.ROI
# 13.토론실 링크
# ##################################################################
import os
import time
from datetime import date
import asyncio

import pandas as pd
import aiohttp
from bs4 import BeautifulSoup

# 한페이지의 결과를 가져온다. #co-routine만드는 것은 객체 생성을 하는 것 #event-loop? i/o blocking?
async def run(session, url):

    
    async with session.get(url) as response:
        if response.status == 200:  
            txt = await response.text() ############# text() 메소드. html만 뽑는다.
            soup = BeautifulSoup(txt, 'lxml')
            tr_list = soup.select("table.type_2 > tbody > tr")
            
            result_list = []  # 현재 페이지의 테이블의 결과를 담는다.     
            
            for tr in tr_list:
                td_list = tr.find_all("td")
                if len(td_list) == 1: # 선을 그리는 용으로 사용된 tr
                    continue
                tr_content_list = [] # 한행의 조회결과를 담을(tr의 td들안의 텍스트들 값) 리스트
                for idx, td in enumerate(td_list):
                    txt = td.text.strip().replace(',','') # 숫자 단위 구분자 , 제거
                    if idx == 3: # 전일비는 content앞에 상승/하락 화살표 이미지가 있다. alt 속성을 조회해서 txt에 붙인다. 변동이 없는 경우는 image가 없이 0이다.
                        img_tag = td.find('img')
                        if img_tag != None: #상승 또는 하락의 경우
                            alt_attr = img_tag.get('alt')
                            if alt_attr == None: #<img>에 alt 속성이 없는 경우=>상한가/하한가 이미지
                                # <img>의 src 속성값을 조회
                                alt_attr = "상한" if img_tag.get('src').endswith("ico_up02.jpg") else "하한"
                            txt = alt_attr + txt
                    if idx == 12: # 토론실 링크는 저장하지 않는다.
                        continue       
                    tr_content_list.append(txt)   # 한행을 구성하는 컬럼값을 저장
                result_list.append(tr_content_list) # 한행을 저장.
    return result_list


# result_list 1페이지 당
# [
#     [1행 값들 (td),,,,,],
#     [2행 값들 (td),,,,,],
#     [3행 값들 (td),,,,,],
#     ,,,
#     [50행 값들 (td),,,,,]
# ]


async def main():
    url = "https://finance.naver.com/sise/sise_market_sum.naver?&page={}"
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    async with aiohttp.ClientSession(headers=headers) as session: #session 생성 url만 다르고 session은 같다
        tasks = [run(session, url.format(i)) for i in range(1, 42)]
        result = await asyncio.gather(*tasks) # event loop에 추가해서 실행하는 부분이 gather이다.
    return result
    
#gather는 list를 받는것이 아니라 개별로 받아야한다. *task처럼 가변인자로 되어있기 때문
#그래서 list에 있는것을 풀어서 넣어야한다. list나 tuple 앞에 *를 붙여주면 하나씩 가변인자 호출방식으로 사용가능

# result 는 1페이지 당 이 내용들로 41페이지까지 존재
# [  (41,50,12) 41페이지, 50개(행)의 값, 각 값 안에 12개의 내용(열)
#     [ #1페이지
#         [1행 값들 (td),,,,,],
#         [2행 값들 (td),,,,,],
#         [3행 값들 (td),,,,,],
#         ,,,
#         [50행 값들 (td),,,,,]
#     ],
#     [ #2페이지
#         [1행 값들 (td),,,,,],
#         [2행 값들 (td),,,,,],
#         [3행 값들 (td),,,,,],
#         ,,,
#         [50행 값들 (td),,,,,]
#     ]
# ]


if __name__ == "__main__":
    start = time.perf_counter()
    result = asyncio.run(main()) ##main co-routine 부른 부분
    print(f'걸린시간: {time.perf_counter() - start}') #걸린시간: 1.7499647
    # 저장
    result_list = []
    for r in result:
        result_list += r   
    col_names = ["NO","종목명","현재가","전일비","등락률","액면가","시가총액","상장주식수","외국인비율","거래량","PER","ROI"]
    df = pd.DataFrame(result_list, columns=col_names)


    fname = f"./02_web/stock_result/{date.today().strftime('%Y-%m-%d_시가총액순위')}.csv"
    df.to_csv(fname, index=False)