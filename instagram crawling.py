from selenium import webdriver
import pandas as pd
import unicodedata
import time
import re

driver = webdriver.Chrome('C:/Users/yj/Desktop/datasalon/chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
driver.get('https://www.instagram.com')
time.sleep(3)

print('Please enter your INSTAGRAM PASSWORD: ')
id = input()
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
