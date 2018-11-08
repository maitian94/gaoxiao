#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
from utils import *
import re


def readTxt():
    with open(r'C:\Users\admin\PycharmProjects\spider11月\7.易阅通\易阅通_Url去重.txt','r') as file:
        lines = file.readlines()
        urls = []
        for url in lines:
            url = url.replace('\n','').strip()
            urls.append(url)
        return urls



def parse():
    result = {}
    urls = readTxt()
    print(len(urls))
    for url in urls:
        print(url)
        res = requests.get(url)
        soup = bs(res.text,'html.parser')
        result['页面链接'] = url
        try:
            try:
                title = soup.select('.w900')[0].text.replace('\u200e', '').strip()
            except:
                title = soup.select('.blue')[0].text.replace('\r\n','').strip()
            result['标题'] = title
        except:
            continue
        blocks = soup.select('.blockP')
        try:
            for block in blocks:
                label = block.select('.w110')[0].text.strip()
                value = block.select('span')[1].text.replace('：','').replace('\u200e','').strip()
                result[label] = value
        except:
            for block in blocks:
                label = block.select('.w100')[0].text.strip()
                try:
                    value = block.select('a')[0].text.replace('：', '').replace('\u200e', '').strip()
                except:

                    value = block.select('span')[1].text.replace('：', '').replace('\u200e', '').strip()
                result[label] = value
        try:
            pic_url = 'http://www.cnpereading.com' + soup.select('.table_img')[0].attrs['href']
        except:
            pic_url = ''
        result['图片链接'] = pic_url
        try:
            intro = soup.select('.fontFam')[0].text.strip()
        except:
            intro = ''
        result['简介'] = intro
        print(result)
        write2csv('data/易阅通.csv',[
                result.get('页面链接',''),
                result.get('图片链接', ''),
                result.get('Publication series', ''),
                result.get('标题', ''),
                result.get('Author：', ''),
                result.get('Publisher：', ''),
                result.get('Publication year：', ''),
                result.get('E-ISBN:', ''),
                result.get('P-ISBN(Paperback):', ''),
                result.get('E-ISSN：', ''),
                result.get('ISSN：', ''),
                result.get('Source：', ''),
                result.get('Subject：', ''),
                result.get('Keyword：', ''),
                result.get('Language：', ''),
                result.get('简介', '')

            ])



if __name__ == '__main__':
    # write2csv('data/易阅通.csv', ['页面链接', '图片链接','Publication series', '标题', 'Author：', 'Publisher：', 'Publication year：', 'E-ISBN:', 'P-ISBN(Paperback):', 'E-ISSN：', 'ISSN：', 'Source：', 'Subject：', 'Keyword：', 'Language：', '简介'])
    parse()
