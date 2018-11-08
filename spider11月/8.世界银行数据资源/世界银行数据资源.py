#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
from selenium import webdriver
import time
from utils import *



def parse():
    for j in range(46,2730):
        start_url = 'https://openknowledge.worldbank.org/browse?order=ASC&rpp=10&sort_by=1&etal=-1&offset=' + str(j*10) + '&type=title'
        print('正在处理第{0}页正在处理第{0}页正在处理第{0}页'.format(j))
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }

        res1 = requests.get(start_url, headers=headers)
        print(res1.status_code)
        time.sleep(8)
        soup1 = bs(res1.text, 'html.parser')
        for i in range(len(soup1.select('.item-wrapper'))):
            url = 'https://openknowledge.worldbank.org' + soup1.select('.item-wrapper')[i].attrs['data-href']
            print(url)
            writeurl2txt('data/世界银行数据资源.txt',url)
            res = requests.get(url, headers=headers)
            time.sleep(8)
            soup = bs(res.text,'html.parser')
            # driver = webdriver.Chrome(r'D:\Wangyuanyuan\工作\爬虫\chromedriver.exe')
            # driver.get(url)
            # soup = bs(driver.page_source,'html.parser')
            # print(soup)
            try:
                title = soup.select('.ds-div-head')[0].text.replace('\r\n','')
            except:
                writeurl2txt('data/failedurl.txt',url)
                continue
            title = re.sub(' {2,20}',' ',title).strip()
            try:
                pic_url = 'https://openknowledge.worldbank.org' + soup.select('#campaign-icon')[0].attrs['src'].strip()
            except:
                pic_url = ''
            try:
                abstract = soup.select('.col-sm-8 .abstract')[0].text.replace('\r\n','').strip()
                abstract = re.sub(' {2,20}','',abstract)
            except:
                abstract = ''
            try:
                try:
                    citation = soup.select('.citation')[0].text.replace('\r\n', '').strip()
                    citation = re.sub(' {2,20}', ' ', citation)
                except:
                    citation = soup.select('.googlescholar')[0].text.replace('Citations:', '').strip()
            except:
                citation = ''
            try:
                collections = []
                for i in range(len(soup.select('.ds-referenceSet-list li'))):
                    collection = soup.select('.ds-referenceSet-list li')[i].text.strip()
                    collections.append(collection)
                collections = ';'.join(collections)
            except:
                collections = ''
            try:
                downloads = []
                for j in range(len(soup.select('.bitstream-link-wrapper a'))):
                    download = 'https://openknowledge.worldbank.org' + soup.select('.bitstream-link-wrapper a')[j].attrs['href'].strip()
                    downloads.append(download)
                    downloads = '; '.join(downloads)
            except:
                downloads = ''
            try:
                published_time = soup.select('.simple-item-view-other')[0].text.strip()
            except:
                published_time = ''
            try:
                authors = []
                for z in range(len(soup.select('.authorprofile-item-view-link'))):
                    author = soup.select('.authorprofile-item-view-link')[z].text.replace('Author(s)','').strip()
                    authors.append(author)
                authors = ';'.join(authors)
            except:
                authors = ''
            result = [url, title, pic_url, abstract, citation, collections, downloads, published_time, authors]
            print(result)
            write2csv('data/世界银行数据资源.csv',result)


if __name__ == '__main__':
    # write2csv('data/世界银行数据资源.csv', ['页面链接', '标题', '图片链接', '摘要', 'citation', 'collections', '下载链接', 'published_time', 'author'])
    parse()