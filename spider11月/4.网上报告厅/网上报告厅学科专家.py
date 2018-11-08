#coding=utf8
import requests
from bs4 import BeautifulSoup as bs

from utils import *

def parse():
    for i in range(1,329):
        url = 'http://www.wsbgt.com/Author?PageIndex=' + str(i)
        print('爬虫进行到第{0}页'.format(i))
        res = requests.get(url)
        soup = bs(res.text,'html.parser')
        uls = soup.select('.ulBox ul')
        for ul in uls:
            lis = ul.select('li')
            # print(lis)
            # print(len(lis))
            for li in lis:
                url = 'http://www.wsbgt.com' + li.select('.img')[0].attrs['href'].strip()
                writeurl2txt('data/网上报告厅学科专家_Url.txt', url)
                pic = li.select('.img img')[0].attrs['src'].replace('\n','').strip()
                name = li.select('.name')[0].text.replace('\n','').strip()
                #课时
                lesson = li.select('.light-gray')[0].text.replace('\n','').strip()
                introduction = li.select('p')[0].text.replace('\n','').strip()
                title = li.select('.taps')[0].text.replace('\n','').strip()
                result = [url, pic, name, lesson, introduction, title]
                print(result)
                write2csv('data/网上报告厅学科专家.csv', result)

if __name__ == '__main__':
    write2csv('data/网上报告厅学科专家.csv', ['详情页链接', '图片链接', '姓名', '课时', '简介', '标题'])
    parse()