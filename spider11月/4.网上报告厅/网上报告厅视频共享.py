#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
from utils import *

def parse():
    for i in range(1,40):
        url = 'http://www.wsbgt.com/videoshared/index?PageIndex=' + str(i)
        print('爬虫进行到第{0}页'.format(i))
        res = requests.get(url)
        soup = bs(res.text,'html.parser')
        videos = soup.select('.courseList .img')
        for video in videos:
            url = 'http://www.wsbgt.com' + video.select('a')[0].attrs['href'].strip()
            writeurl2txt('data/网上报告厅视频共享_Url.txt', url)
            title = video.select('a')[0].attrs['title'].replace('\n','').strip()
            pic = video.select('img')[0].attrs['src'].strip()
            result = [url, title, pic]
            write2csv('data/网上报告厅视频共享.csv',result)


if __name__ == '__main__':
    write2csv('data/网上报告厅视频共享.csv', ['详情页链接', '图片链接', '标题'])
    parse()