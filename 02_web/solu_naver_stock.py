
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

# css selector: 
##  테이블: table.type_2 > tbody > tr

# 주의
## 전일비: 화살표이미지 값
### 화살표: ▲ - 상승 - alt 속성의 값이 상승
###        ▼ - 하락 - alt 속성의 값이 하락
###        변경이 없을 경우 image가 없음
###        ↑ ↓ 은 상한 하한가로 alt 속성이 없음 => image명을 구분. (ico_up02.gif, ico_down02.gif)
# ##################################################################
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


# html에서 표는 table이라는 틀 사용
# 보통 맨위에는 정보를 담은 header값이 있음
# 아래와 같은 형식으로 구성되어 있다.
# <table>
#     <thead>
#         <tr>
#             <td>"1"</td>
#             <td>"삼성전자"</td>
#         </tr>
#     </thead>
#     <tbody>

#     </tbody>
#     <tfoot>

#     </tfoot>
# </table>


def main():
    headers={ 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
    urlo = "https://finance.naver.com/sise/sise_market_sum.naver?&page="
    #user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    #요청
    result_list=[]
    for page in range(1,42):
        url= urlo+str(page)
        #print(url)
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            soup = BeautifulSoup(response.text)
            #parser "lxml" 사용하면 beautifulsoup의 html.parser보다 속도가 빠르고 html 뿐 아니라 xml도 parsing가능
            #parsing은 원하는 data를 가져오는것
            tr_list=soup.select("table.type_2 > tbody > tr")

            for tr in tr_list:
                td_list = tr.find_all("td")
                if len(td_list)==1: #선을 그리는 용으로 사용된 tr
                    continue
                td_content_list = [] #한행의 조회결과를 담을 (td안의 테스트들 값) list
                for idx, td in enumerate(td_list):
                    txt=td.text.strip()
                    if idx == 3: #전일비 <td> #전일비에는 img tag가 존재하고 상한,하한,상승,하락,변동없음으로 5가지 종류가 있다.
                        img_tag=td.find("img")
                        if img_tag != None: #0이 아니라 img tag 존재
                            alt_attr=img_tag.get('alt') #alt라는 옵션이 존재
                            if alt_attr == None: # <img>에 alt 속성이 없는 경우, 상한가 or 하한가
                                # <img>의 src 속성값을 조회
                                alt_attr = "상한" if img_tag.get('src').endswith("ico_up02.jpg") else "하한"
                                # 그냥 상승 하강에도 src는 존재하고 endswith("ico_up.jpg") 이다.
                            txt = alt_attr + txt
                    elif idx==12:
                        continue
                    td_content_list.append(txt) #한행을 구성하는 컬럼값 저장
                result_list.append(td_content_list) #한행을 저장
            # print(result_list)
            # print(len(result_list))
                
        else:
            print(page,"th page fail")
    return result_list


if __name__ == '__main__':
    import time
    start = time.time()
    result=main()
    print(len(result))
    end=time.time()
    print("걸린시간:",end-start)

    save_path="./02_web/stocks"
    os.makedirs(save_path, exist_ok=True) #덮어쓰기 아님
    file_name=datetime.now().strftime("%Y-%m-%d_KOSPI information.csv")

    col_names = ["NO","종목명","현재가","전일비","등락률","액면가","시가총액","상장주식수","외국인비율","거래량","PER","ROI"]
    df = pd.DataFrame(result, columns=col_names)  
    df.to_csv(f"{save_path}/{file_name}", index=False)
#     df=pd.DataFrame(result)
#     df.to_csv(f"{save_path}/{file_name}",index=False) #columns=["No","종목명","현재가","전일비","등락률","액면가","시가총액","상장주식수","외국인비율","거래량","PER","ROE"])
# # <img src="이미지파일경로" alt="정보">