from selenium import webdriver
from bs4 import BeautifulSoup
import unicodedata
import time
import re

# 정보 수집


def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 본문 내용 가져오기
    try:
        content = soup.select('div.C4VMK > span')[0].text
        content = unicodedata.normalize('NFC', content)
    except:
        content = ' '

    # 본문 내용에서 해시태그 가져오기
    # content 변수의 본문 내용 중 #로 시작하고, # 뒤에 연속된 문자(공백이나 #,\ 기호가 아닌 경우)를 모두 찾아서 리스트 형태로 tags 변수에 저장
    tags = re.findall(r'#[^\s#,\\]+', content)

    # ④ 작성일자 정보 가져오기
    date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10]

    # ⑤ 좋아요 수 가져오기
    try:
        # 0~3번째가 '좋아요 '. 따라서 4번째부터 마지막까지
        like = soup.select('div._7UhW9')[0].text[4:-2]
    except:
        like = '공ㄱ'

    # ⑥ 위치정보 가져오기
    try:
        place = soup.select('div.M30cS')[0].text
        place = unicodedata.normalize('NFC', place)
    except:
        place = ''

    # ⑦ 수집한 정보 저장하기
    data = [content, date, like, place, tags]
    return data
