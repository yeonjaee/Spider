from selenium import webdriver
import instagram_def as idef    # 함수 파일 참조
import pandas as pd
import unicodedata
import time
import re

# 주의
# python myscript.py 로 실행하면 화면 안꺼짐.

# login
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(
    'C:/Users/yj/Desktop/datasalon/chromedriver.exe', options=options)
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
url = idef.insta_searching(word)
driver.get(url)
