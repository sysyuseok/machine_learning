import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
url ="https://finance.naver.com/sise/sise_market_sum.naver"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' 

def get_stock_list():
    # 요청 
    response = requests.get(url, headers = {"User-Agent":user_agent})
    # 상태 코드 200 확인
    if response.status_code == 200: # 정상 응답 확인하기
        #print("정상 상태 코드 확인", response.status_code)
        # 요청 받아온거 뷰티풀 소프에 저장 -> 파싱하기 위해
        soup = BeautifulSoup(response.text, 'lxml')
        tag_list_com =soup.select("#contentarea > div.box_type_l > table.type_2 > tbody> tr a")
        tag_list = soup.select("#contentarea > div.box_type_l > table.type_2 > tbody > tr> td.number")
        # 긁어오기
        #print(tag_list_com)
        stock_list=[] # 값
        stock_li=[]
        stock_name=[] # 이름
        for comp in tag_list_com:
            stock_name.append(comp.get_text().strip())
        for i in stock_name:
            if i == "":
                stock_name.remove(i)
        li=[]

        #print(stock_name)
        for i in range(len(tag_list)):
            #print(tag_list[i])
            print("------\n""------\n""------\n")
            stock_li.append(tag_list[i].get_text().strip())
            if i%10==9:
                stock_list.append(stock_li)
                print(stock_list)
                stock_li.clear()

        #print(stock_list)
        # for i in range(len(stock_name)):
        #     li.append(stock_name[i])
        #     for j in range(10):
        #         li.append(stock_list[10*i+j])
        # print(li)
get_stock_list()




















# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import os
# import re
# url ="https://finance.naver.com/sise/sise_market_sum.naver"
# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' 

# def get_stock_list():
#     # 요청 
#     response = requests.get(url, headers = {"User-Agent":user_agent})
#     # 상태 코드 200 확인
#     if response.status_code == 200: # 정상 응답 확인하기
#         print("정상 상태 코드 확인", response.status_code)
#         # 요청 받아온거 뷰티풀 소프에 저장 -> 파싱하기 위해
#         soup = BeautifulSoup(response.text, 'lxml')
#         tag_list_com =soup.select("#contentarea > div.box_type_l > table.type_2 > tbody> tr a")
#         tag_list = soup.select("#contentarea > div.box_type_l > table.type_2 > tbody > tr> td.number")
#         # 긁어오기 
#         print(tag_list_com)
#         stock_list=[] # 값
#         stock_name=[] # 이름
#         for comp in tag_list_com:
#             stock_name.append(comp.get_text().strip())
#         for i in stock_name:
#             if i == "":
#                 stock_name.remove(i)

#         print(stock_name)
#         for tag in tag_list:
#             stock_list.append(tag.get_text().strip())
#         print(stock_list)




