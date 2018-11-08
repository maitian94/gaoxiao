#coding=utf8
import time
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from utils import write2csv
import re

def getUrl():
    pass
    # url = 'http://apabi.szlib.com/List1.asp?lang=gb&act=SimpleQuery&DocGroupID=2&DisplayMode=ClassicDisplay&page=1'
    # res = requests.get(url)
    # soup = bs(res.text,'html.parser')
    # urls = []
    # for i in range(0,len(soup.select('.BookTableFrame a')),2):
    #     url = soup.select('.BookTableFrame a')[i].attrs['href']
    #     id_ = re.findall('.*?ID=(.*?)&',url)
    #     if id_ != []:
    #         url = 'http://apabi.szlib.com/Product2.asp?lang=gb&type=&DocGroupID=2&DocID=' + id_[0]
    #         urls.append(url)
    # print(urls)





def parse():
    result = {}
    for i in range(14742,72357):
    # for i in range(5,25):
        url = 'http://apabi.szlib.com/Product2.asp?lang=gb&type=&DocGroupID=2&DocID=' + str(i)
        try:
            res = requests.get(url)
            soup = bs(res.text,'html.parser')
            picture_url = soup.select('html body tr img')[0].attrs['src'].strip()
        except Exception as e:
            print(e)
            continue
        result['页面链接'] = url
        result['图片链接'] = picture_url
        trs = soup.select('html body tr table')[2].select('tr')
        for tr in trs:
            label = tr.select('td')[0].text.strip()
            value = tr.select('td')[1].text.replace('\n','').replace('\t','').replace('\r','').strip()
            result[label] = value
        print(result)
        write2csv('data/阿帕比电子图书.csv',[
                result.get('页面链接', ''),
                result.get('其它题名', ''),
                result.get('书名', ''),
                result.get('图片链接',''),
                result.get('责任者', ''),
                result.get('主要责任关系', ''),
                result.get('主题/关键词', ''),
                result.get('摘要', ''),
                result.get('出版社', ''),
                result.get('出版地', ''),
                result.get('出版日期', ''),
                result.get('标识', ''),
                result.get('标识类型', ''),
                result.get('价格', ''),
                result.get('纸书价格', ''),
                result.get('责任编辑',''),
                result.get('版次', ''),
                result.get('印次', ''),
                result.get('字数(千字)', ''),
                result.get('中图法分类号', ''),
                result.get('ISBN号', ''),
                result.get('附注',''),
                result.get('外币价格',''),
                result.get('相关文献与本文献的联系', ''),
                result.get('次要责任者', ''),
                result.get('次要责任关系', ''),
                result.get('Apabi分类号', ''),
            ])



# 'http://apabi.szlib.com/Product2.asp?lang=gb&type=&DocGroupID=2&DocID=72355'
# 'http://apabi.szlib.com/Product2.asp?lang=gb&type=&DocGroupID=2&DocID=72356'
if __name__ == '__main__':
    parse()


