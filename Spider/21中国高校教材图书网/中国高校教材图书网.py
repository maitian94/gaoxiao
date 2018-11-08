#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
import re
from pprint import pprint
from utils import write2csv
import time

def typeUrls():
    url = 'http://www.sinobook.com.cn/b2c/scrp/bookidxc3.cfm?sCid=QT&iClass=3'
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    type_urls = []
    for i in range(len(soup.select('.tblBookIdx li'))):
        type_url = 'http://www.sinobook.com.cn/b2c/scrp/' + soup.select('.tblBookIdx li a')[i].attrs['href']
        type_urls.append(type_url)
    return type_urls

def fanye(url, currentpage):
    data = {
        'iPage': currentpage
    }
    res = requests.post(url, data=data)
    soup = bs(res.text, 'html.parser')
    return soup


def allUrls():
    type_urls = typeUrls()
    print(type_urls)
    all_urls = []
    for url in type_urls:
        print(url)
        res = requests.get(url)
        soup = bs(res.text,'html.parser')
        try:
            page_num = re.findall('\d+',soup.select('.a1')[-2].next_sibling)[0]
        except:
            if soup.select('.tblBrow tr'):
                page_num = 1
            else:
                page_num = 0
        for i in range(1, int(page_num)+1):
            print('正在处理第%d页'%i)
            soup1 = fanye(url,i)
            for j in range(1, len(soup1.select('.tblBrow tr')) - 1):
                onepage_url = 'http://www.sinobook.com.cn/b2c/scrp/' + soup1.select('.tblBrow tr')[j].select('a')[2].attrs[
                    'href']
                all_urls.append(onepage_url)
    return all_urls

def parse():
    all_urls = allUrls()
    print(all_urls)
    for url in all_urls:
        print(url)
        time.sleep(1.2)
        try:
            result = {}
            res = requests.get(url)
            soup = bs(res.text,'html.parser')
            # print(soup)
            for i in range(1,len(soup.select('.tblBrow')[0].select('td')),2):
                label = soup.select('.tblBrow')[0].select('td')[i].text.strip()
                value = soup.select('.tblBrow')[0].select('td')[i+1].text.replace('\r\n','').replace('\t','').replace('相关图书','').replace('\n','').replace('页','').strip()
                result[label] = value
            prizes = re.findall('￥(.*?)折扣价：￥(.*?)折扣：(.*?)节.*?',result['定价：'])
            result['定价：'] = prizes[0][0].strip()
            result['折扣价'] = prizes[0][1].strip()
            result['折扣'] = prizes[0][2].strip()
            result['图片'] = 'http://www.sinobook.com.cn' + soup.select('.tblBrow img')[0].attrs['src']
            for j in range(len(soup.select('.tblBrow')[1].select('.tdCaptionD'))):
                label = soup.select('.tblBrow')[1].select('.tdCaptionD')[j].text.strip()
                value = soup.select('.tblBrow')[1].select('.Text')[j].text.replace('\r\n','').replace('\t','').replace('\n','').replace('�','').strip()
                result[label] = value
            result['分类'] = '其他'
            result['页面链接'] = url
            # return result
            print(result)
            write2csv('中国高校教材图书网131313.csv', [
                    result.get('页面链接', ''),
                    result.get('书名：', ''),
                    result.get('图片', ''),
                    result.get('分类', ''),
                    result.get('ISBN：', ''),
                    result.get('条码：', ''),
                    result.get('作者：', ''),
                    result.get('装订：', ''),
                    result.get('印次：', ''),
                    result.get('开本：', ''),
                    result.get('定价：', ''),
                    result.get('折扣', ''),
                    result.get('折扣价', ''),
                    result.get('字数：', ''),
                    result.get('出版社：', ''),
                    result.get('页数：', ''),
                    result.get('发行编号：', ''),
                    result.get('每包册数：', ''),
                    result.get('出版日期：', ''),
                    result.get('内容简介：', ''),
                    result.get('作者简介：', ''),
                    result.get('章节目录：', ''),
                    result.get('精彩片段：', ''),
                    result.get('书\u3000\u3000评：',''),
                    result.get('其\u3000\u3000它：', '')
            ])
        except Exception as e:
            print(e)
            print('*********网页犯病了*********')
        continue


def main():
    parse()


if __name__ == '__main__':
    main()

