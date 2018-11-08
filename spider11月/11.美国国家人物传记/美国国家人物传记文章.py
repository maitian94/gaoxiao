#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
from utils import *
from pprint import pprint

def parse():
    for i in range(1890,1957):
        page_url = 'http://www.anb.org/browse?btog=chap&isQuickSearch=true&page=' + str(i) + '&pageSize=10&sort=titlesort&type_4=subjectreference'
        print('正在处理第{0}页正在处理第{0}页正在处理第{0}页'.format(i))
        res = requests.get(page_url)
        soup = bs(res.text,'html.parser')
        ids = soup.select('#searchContent .contentItem')
        for id in ids:
            url = 'http://www.anb.org' + id.select('.itemTitle a')[0].attrs['href']
            print(url)
            info = id.select('.title-wrapper')[0].text.strip().replace('), ',';').replace(' (',';').split(';')
            name = info[0]
            try:
                time = info[1]
            except:
                time = ''
            try:
                career = info[2]
            except:
                career = ''
            try:
                author = id.select('.author')[0].text.strip()
            except:
                author = ''
            try:
                printdate = id.select('.printDate .c-List__item--secondary')[0].text.strip()
            except:
                printdate = ''
            try:
                onlinedate = id.select('.printDate .c-List__item--secondary')[0].text.strip()
            except:
                onlinedate = ''
            abstract = id.select('.abstract')[0].text.strip()
            result = [url, name, time, career, author, printdate, onlinedate, abstract]
            print(result)
            writeurl2txt('data/美国国家人物传记文章.txt',url)
            write2csv('data/美国国家人物传记文章.csv',result)



if __name__ == '__main__':
    # write2csv('data/美国国家人物传记文章.csv', ['url', 'name', 'time', 'career', 'author', 'printdate', 'onlinedate', 'abstract'])
    parse()