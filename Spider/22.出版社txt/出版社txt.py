#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import urllib3
from utils import writeurl2txt
import urllib.parse

def type():
    with open('C:\\Users\\admin\\Desktop\\出版社类别.txt','r') as file:
        lines = file.readlines()
        types = []
        for type in lines:
            type = type.strip()
            types.append(type)
        return types


def getUrl():
    types = type()
    print(types)
    print(len(types))
    for diftype in types:
        diftype = diftype.strip()
        print(diftype*3)
        diftype = urllib.parse.quote(diftype)
        url_ = 'https://book.douban.com/subject_search?search_text=' + diftype + '&cat=1001&start='
        failed_url = []
        for j in range(134):
            url = url_ + str(j*15)
            print(url)
            # service_args = [
            #     '--proxy=114.237.228.195:28422',
            #     '--proxy-type=http',
            #     '--load-images=no',
            #     '--disk-cache=yes',
            #     '--ignore-ssl-errors=true'
            # ]
            chrome_options = Options()
            chrome_options.add_argument('--headless--')
            chrome_options.add_argument('--disable-gpu')
            # path = r'D:\Wangyuanyuan\工作\爬虫\chromedriver.exe'
            # driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

            # phantomjsdriver = r'D:\Wangyuanyuan\工作\爬虫\phantomjs.exe'
            # driver = webdriver.PhantomJS(phantomjsdriver, service_args=service_args)

            driver = webdriver.PhantomJS(r'D:\Wangyuanyuan\工作\爬虫\phantomjs.exe')
            driver.get(url)
            time.sleep(0.2)
            soup = bs(driver.page_source,'html.parser')
            try:
                for i in range(15):
                    onepage_url = soup.select('.sc-bZQynM .item-root .detail .title a')[i].attrs['href']
                    print(onepage_url)
                    writeurl2txt('出版社txt.txt',onepage_url)
            except Exception as e:
                print(e)
                print('页面可能没有134页')
                failed_url.append(url)
                writeurl2txt('dailedurl.txt',url)
            continue


def main():
    getUrl()



if  __name__ == '__main__':
    main()