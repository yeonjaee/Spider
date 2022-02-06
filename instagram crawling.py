from selenium import webdriver
import pandas as pd
import unicodedata
import time
import re

driver = webdriver.Chrome('C:/Users/yj/Desktop/datasalon/chromedriver.exe')

driver.get('https://www.instagram.com')
time.sleep(2)

print('Please enter your INSTAGRAM ID: ')
id = input()
print('----' * 4)
input_id = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
input_id.clear()
input_id.send_keys(id)

print('Please enter your INSTAGRAM PASSWORD: ')
password = input()
input_pw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
input_pw.clear()
input_pw.send_keys(password)
input_pw.submit()
time.sleep(3)
