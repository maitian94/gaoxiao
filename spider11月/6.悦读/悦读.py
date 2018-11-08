#coding=utf8
import requests
from lxml import etree
from bs4 import BeautifulSoup as bs
import re
from pprint import pprint
from selenium import webdriver
import time
from utils import *

# def getUrl():
#     '''用selenium方法获取链接'''
#     url = 'http://yd.51zhy.cn/ebook/web/search/search4HomePage?tst=2&keywords=&queryType=single&classGrade=0&class4srch=&clc4srch=&orderType=DESC'
#     driver = webdriver.Chrome(r'D:\Wangyuanyuan\工作\爬虫\chromedriver.exe')
#     driver.get(url)
#     page = 1
#     detail_urls = []
#     while page < 762:
#         soup = bs(driver.page_source, 'html.parser')
#         lis = soup.select('.ebook-item ')
#         for li in lis:
#             detail_url = 'http://yd.51zhy.cn/ebook/web/newBook/queryNewBookById?id=' + li.select('input')[0].attrs[
#                 'value'].strip()
#             detail_urls.append(detail_url)
#             print(detail_url)
#             writeurl2txt('data/悦读_Url.txt',detail_url)
#         next_page = driver.find_element_by_link_text('下一页')
#         next_page.click()
#         time.sleep(1)
#         print('已经处理到第{0}页已经处理到第{0}页已经处理到第{0}页'.format(page))
#         page += 1
#     return detail_urls



def readTxt():
    with open(r'C:\Users\admin\PycharmProjects\spider11月\6.悦读\data\failedUrl.txt','r') as file:
        lines = file.readlines()
        urls = []
        for url in lines:
            url = url.replace('\n','').strip()
            urls.append(url)
        return urls

def parse():
    urls = readTxt()
    for url in urls:
        result = {}
        res = requests.get(url)
        soup = bs(res.text,'html.parser')
        print(url)
        id = re.findall('.*?id=(\d+)',url)
        result['页面链接'] = url
        try:
            pic_url = soup.select('.book-img img')[0].attrs['src'].strip()
        except:
            writeurl2txt('data/failedUrl.txt',url)
            continue
        result['图片链接'] = pic_url
        title = soup.select('.book-info .t')[0].text.strip()
        result['标题'] = title
        infos = soup.select('.book-info .txt')[0].text.split('\r\n')
        for info in infos:
            try:
                label = info.split('：')[0].strip()
                value = info.split('：')[1].strip()
                result[label] = value
                result['出版社分类'] = re.findall('(.*?)\n￥.*?',value)[0].strip()
            except:
                pass
        prize = soup.select('.book-info .txt span')[0].text.strip()
        result['价格'] = prize
        result['ISBN'] = soup.select('.isbn')[0].text.replace('ISBN：','').strip()
        result['简介'] = soup.select('#1')[0].text.replace('\n','').strip()
        # print(result)
        details = soup.select('.book-tab-box .txt')[1].text.split('\r\n')
        for detail in details:
            try:
                label = detail.split('：')[0].strip()
                value = detail.split('：')[1].strip()
                result[label] = value
            except:
                pass
        mulu_url = 'http://yd.51zhy.cn/ebook/web/newBook/getBoolMarksList'
        data = {
            'id': id
        }
        headers = {
            'Referer': url
        }
        res1 = requests.post(mulu_url, headers=headers, data=data)
        soup1 = bs(res1.text,'html.parser')
        a = []
        for i in range(len(soup1.select('#showAll .catalog-title'))):
            mulu = soup1.select('#showAll .catalog-title')[i].text.strip()
            a.append(mulu)
        mulus = ';'.join(a)
        result['目录'] = mulus
        print(result)
        write2csv('data/悦读.csv',[
            result.get('页面链接',''),
            result.get('图片链接', ''),
            result.get('标题', ''),
            result.get('作者', ''),
            result.get('其他责任人', ''),
            result.get('出版日期', ''),
            result.get('出版社', ''),
            result.get('页数', ''),
            result.get('中图分类', ''),
            result.get('出版社分类', ''),
            result.get('价格', ''),
            result.get('ISBN', ''),
            result.get('简介', ''),
            result.get('关键字', ''),
            result.get('开本', ''),
            result.get('目录', '')
        ])


if __name__ == '__main__':
    # write2csv('data/悦读.csv', ['页面链接', '图片链接', '标题', '作者', '其他责任人', '出版日期', '出版社', '页数', '中图分类',
    #                           '出版社分类','价格', 'ISBN', '简介', '关键字', '开本', '目录', ])
    parse()