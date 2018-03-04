#!/usr/bin/env python
# encoding: utf-8

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import datetime
import os
import sys
import yaml

f = open(
    os.path.join(os.getcwd(), os.path.dirname(__file__), 'config.yaml'), 'r+')
data = yaml.load(f)

options = webdriver.ChromeOptions()
if '--headless' in sys.argv:
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    options.add_argument('window-sizes=1920,1080')

driver = webdriver.Chrome(chrome_options=options)
driver.get(
    "https://www.dmm.com/my/-/login/=/path=DRVESVwZTldRDlBRRFdIUwwIGFVfVEs_")
login_id = driver.find_element_by_id("login_id")
login_id.send_keys(data['id'])
password = driver.find_element_by_id("password")
password.send_keys(data['pass'])
driver.find_element_by_tag_name("form").submit()

time = data['time']
day = datetime.datetime.today()  #+ datetime.timedelta(days=1)

tmpl = "http://eikaiwa.dmm.com/list/?data[tab1][start_time]={}&data[tab1][end_time]={}&data[tab1][gender]=0&data[tab1][age]=年齢&data[tab1][free_word]=&date={}&tab=0&sort=4"
url = tmpl.format(time, time, day.strftime('%Y-%m-%d'))
driver.get(url)

buttons = driver.find_elements_by_class_name('bt-open')
for button in buttons:
    if not button.is_displayed():
        continue

    button.click()

    try:
        WebDriverWait(driver, 5).until(
            EC.url_contains('eikaiwa.dmm.com/book/index'))
        driver.find_element_by_id('submitBox').submit()
        break
    except (TimeoutException):
        driver.find_element_by_id("close_btn").click()
        pass

driver.quit()
