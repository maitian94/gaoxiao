#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
import re
from pprint import pprint
from selenium import webdriver
import time

def test():
    url = 'http://www.sinobook.com.cn/b2c/scrp/bookidxc4.cfm?&iPno=300&sCid=DB&iClass=3'
    # onepage_urls = []
    # for j in range(1,len(soup.select('.tblBrow tr'))-1):
    #     onepage_url = 'http://www.sinobook.com.cn/b2c/scrp/' + soup.select('.tblBrow tr')[j].select('a')[2].attrs['href']
    #     onepage_urls.append(onepage_url)
    # return onepage_urls
    driver = webdriver.Chrome(r'D:\Wangyuanyuan\工作\爬虫\chromedriver.exe')
    driver.get(url)
    time.sleep(0.1)
    page = 1
    while page < 3:
        soup = bs(driver.page_source, 'html.parser')
        nextpg = driver.find_element_by_link_text('下一页>')
        nextpg.click()
        time.sleep(4)

def main():
    test()

if __name__ == '__main__':
    main()