#coding=utf8
import requests
from lxml import etree
from bs4 import BeautifulSoup as bs
from utils import *

def parse():
    for i in range(1043,1382):
        page_url = 'https://hk.lexiscn.com/legal_news?page={0}'.format(i)
        print('正在处理第{0}页'.format(i))
        res = requests.get(page_url)
        html = etree.HTML(res.text)
        lis = html.xpath("//ul[@class='list']/li")
        for li in lis:
            url = li.xpath(".//a/@href")[0].strip()
            print(url)
            writeurl2txt('data/律商网_Url.txt',url)
            title = li.xpath(".//a/text()")[0].strip()
            date = li.xpath(".//span/text()")[0].replace('[','').replace(']','').strip()
            try:
                summary = li.xpath(".//div[@class='summary']/p/text()")[1].strip()
            except:
                summary = ''
            res1 = requests.get(url)
            html1 = res1.content.decode('utf-8')
            soup1 = bs(html1,'html.parser')
            chinese_page = soup1.select('.news-article')[0].text.replace('\t','').replace('\r\n','').replace('英文版\n','').strip()
            try:
                english_url = 'https://hk.lexiscn.com' + soup1.select('.version_select')[0].attrs['href'].strip()
            except:
                english_url = ''
                continue
            try:
                res2 = requests.get(english_url)
                html2 = res2.content.decode('utf-8')
                soup2 = bs(html2,'html.parser')
                english_page = soup2.select('.news-article')[0].text.replace('\t','').replace('\r\n','').replace('Chinese version\n','').strip()
            except:
                continue
            result = [url, title, date, summary, chinese_page, english_page]
            print(result)
            write2csv('data/律商网.csv',result)


if __name__ == '__main__':
    # write2csv('data/律商网.csv',['页面链接', '标题', '日期', '摘要', '中文版页面', '英文版页面'])
    parse()

