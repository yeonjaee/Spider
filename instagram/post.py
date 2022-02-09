from bs4 import BeautifulSoup
import time

# 첫 게시글 선택
def select_first(driver):
    first = driver.find_element_by_css_selector('div._9AhH0')
    first.click()

# 게시글 이동
def move_next(driver):
    right = driver.find_element_by_css_selector(
        "div.l8mY4.feth3")  # 주소 띄어쓰기는 . 으로 표시
    right.click()
    time.sleep(3)
