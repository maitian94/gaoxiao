#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
from utils import *

def get(url, currentpage):
    data = {
        'curpage': currentpage
    }
    res = requests.post(url, data=data)
    soup = bs(res.text,'html.parser')
    return soup

def getUrl():
    url = 'http://www.cnpereading.com/index/advancedSearchSubmit?taxonomy=T%20%E5%B7%A5%E4%B8%9A%E6%8A%80%E6%9C%AF'
    detail_urls = []
    for i in range(44962):
        soup = get(url, i)
        print('正在处理第{0}页正在处理第{0}页正在处理第{0}页正在处理第{0}页'.format(i))
        details = soup.select('.w700')[1:]
        for detail in details:
            detail_url = 'http://www.cnpereading.com' + detail.select('.a_title')[0].attrs['href'].strip()
            detail_urls.append(detail_url)
            writeurl2txt('data/易阅通_UrlT.txt',detail_url)
            print(detail_url)


if __name__ == '__main__':
    getUrl()