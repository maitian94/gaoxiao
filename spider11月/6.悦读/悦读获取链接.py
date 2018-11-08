#coding=utf8
import requests
from lxml import etree
from bs4 import BeautifulSoup as bs
import re
from pprint import pprint
from selenium import webdriver
import time
from utils import *



def getUrl(url, currentpage):
    data = {
        'tst':'m5',
        'orderColumn':'score',
        'orderType':'DESC',
        'currentPage': currentpage ,
        'countsOfPerPage':'15'
            }
    res = requests.post(url, data=data)
    soup = bs(res.text, 'html.parser')
    return soup


if __name__ == '__main__':
    url = 'http://yd.51zhy.cn/ebook/web/search/search4HomePage'
    detail_urls = []
    for i in range(1,762):
        soup = getUrl(url,i)
        print('已经处理到第{0}页已经处理到第{0}页已经处理到第{0}页'.format(i))
        lis = soup.select('.ebook-item ')
        for li in lis:
            detail_url = 'http://yd.51zhy.cn/ebook/web/newBook/queryNewBookById?id=' + li.select('input')[0].attrs[
                        'value'].strip()
            detail_urls.append(detail_url)
            print(detail_url)
            writeurl2txt('data/悦读_Url.txt',detail_url)
