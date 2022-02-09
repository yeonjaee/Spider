from tqdm import tqdm
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import url
import post
import contents
import time

# 주의
# python myscript.py 로 실행하면 화면 안꺼짐.

# login
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
options = webdriver.ChromeOptions()
options.add_experimental_option(
    "excludeSwitches", ["enable-logging"])  # 에러메시지 출력 X,
options.add_argument("headless")  # 크롬 창 띄우기 X

driver = webdriver.Chrome(
    'C:/Users/yj/Desktop/chromedriver.exe', options=options)
driver.get('https://www.instagram.com')

time.sleep(3)

id = input("Please enter your INSTAGRAM ID: ")
input_id = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
input_id.clear()
input_id.send_keys(id)

password = input("Please enter your INSTAGRAM PASSWORD: ")
input_pw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
input_pw.clear()
input_pw.send_keys(password)
input_pw.submit()

time.sleep(3)
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

# search
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
word = input("Please enter the keyword to search: ")
print(f"'{word}'의 검색 결과를 검색합니다..")
driver.get(url.insta_searching(word))

time.sleep(10)

target = int(input("탐색할 게시글 수를 입력하세요: "))
post.select_first(driver)

time.sleep(5)

results = []


for i in tqdm(range(target)):
    try:
        data = contents.get_content(driver)
        results.append(data)
        post.move_next(driver)
    except:
        time.sleep(4)
        post.move_next(driver)


results_df = pd.DataFrame(results)
results_df.columns = ['content', 'date', 'like', 'place', 'tags']
results_df.to_excel('C:/Users/yj/Desktop/test.xlsx', index=False)
time.sleep(5)

driver.quit()
