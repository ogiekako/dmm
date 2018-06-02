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
pref = yaml.load(f)

pref_id = pref['id']
pref_pass = pref['pass']
pref_time = pref['time']
pref_lesson_style = pref[
    'lessonStyle'] if 'lessonStyle' in pref else 'Original Materials'
pref_original_material = ''
if pref_lesson_style == 'Original Materials':
    pref_original_material = pref[
        'originalMaterial'] if 'originalMaterial' in pref else 'Daily News'


def get_target_datetime(time_str):
    t = datetime.datetime.strptime(time_str, '%H:%M')
    target_datetime = datetime.datetime.combine(datetime.date.today(),
                                                datetime.time(
                                                    hour=t.hour,
                                                    minute=t.minute))
    while target_datetime < datetime.datetime.now():
        target_datetime += datetime.timedelta(days=1)
    return target_datetime


target_datetime = get_target_datetime(pref_time)

options = webdriver.ChromeOptions()
if '--headless' in sys.argv:
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    options.add_argument('window-sizes=1920,1080')

driver = webdriver.Chrome(chrome_options=options)
driver.get(
    "https://www.dmm.com/my/-/login/=/path=DRVESVwZTldRDlBRRFdIUwwIGFVfVEs_")
login_id = driver.find_element_by_id("login_id")
login_id.send_keys(pref_id)
password = driver.find_element_by_id("password")
password.send_keys(pref_pass)
driver.find_element_by_tag_name("form").submit()

tmpl = "http://eikaiwa.dmm.com/list/?data[tab1][start_time]={}&data[tab1][end_time]={}&data[tab1][gender]=0&data[tab1][age]=年齢&data[tab1][free_word]=&date={}&tab=0&sort=4"
url = tmpl.format(pref_time, pref_time, target_datetime.strftime('%Y-%m-%d'))
driver.get(url)

buttons = driver.find_elements_by_class_name('bt-open')
for button in buttons:
    if not button.is_displayed():
        continue

    button.click()

    try:
        WebDriverWait(driver, 5).until(
            EC.url_contains('eikaiwa.dmm.com/book/index'))

        driver.find_element_by_id('lessonStyle').click()
        driver.find_element_by_css_selector(
            '#lessonStyle > [value = "{}"]'.format(pref_lesson_style)).click()
        if pref_original_material:
            driver.find_element_by_id('originalMaterial').click()
            driver.find_element_by_css_selector(
                '#originalMaterial > [value = "{}"]'.format(
                    pref_original_material)).click()

        driver.find_element_by_id('submitBox').submit()
        break
    except (TimeoutException):
        driver.find_element_by_id("close_btn").click()
        pass

driver.quit()
