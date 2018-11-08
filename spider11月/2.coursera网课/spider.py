# -*- coding: utf-8 -*- 
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from utils import *
import time


def searchOneTime(kword):
    url = 'https://www.coursera.org/courses?query=%s' % kword
    profile_directory = r'C:\Users\Xuejx\AppData\Roaming\Mozilla\Firefox\Profiles\gvocaw6l.default'
    profile = webdriver.FirefoxProfile(profile_directory)
    profile.set_preference('permissions.default.image', 2)
    driver = webdriver.Firefox(executable_path=r'D:\geckodriver.exe', firefox_profile=profile)
    driver.get(url)
    time.sleep(3)
    #将滚动条移动到页面的底部
    while 1:
        js = "var q=document.documentElement.scrollTop=100000"
        driver.execute_script(js)
        time.sleep(1)
        try:
            show_more_btn = driver.find_element_by_class_name('ais-InfiniteHits-loadMore').click()
        except:
            break
    cards = driver.find_elements_by_class_name('rc-AlgoliaSearchCard')
    for card in cards:
        href = card.get_attribute('href')
        print(href)
        if href.startswith('https://www.coursera.org/learn/'):
            writeurl2txt('data/coursera_Url.txt',href)
    driver.quit()
if __name__ == '__main__':
    quchong('data/coursera_Url2.txt','data/coursera_Url.txt')