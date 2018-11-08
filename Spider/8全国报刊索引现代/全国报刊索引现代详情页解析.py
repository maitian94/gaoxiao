#coding=utf8
import requests
from bs4 import BeautifulSoup as bs

def parser():
    result = {}
    res = requests.get('http://www.cnbksy.com/search/detail/7de21b7fec3db682ed5245ea1fc9d1a9/8/5ba1eb5023b099657e9ac46c')
    soup = bs(res.text,'html.parser')
    trs = soup.select('.srTable tr')
    for tr in trs:
        label = tr.select('td')[0].text.strip().replace('\n','')
        value = tr.select('td')[1].text.strip().replace('\n','')
        result[label] = value
    return [
        result.get('题名：', ''),
        result.get('作者：', ''),
        result.get('文献来源：', ''),
        result.get('出版时间：', ''),
        result.get('卷期(页)：', ''),
        result.get('中图分类号：', ''),
        result.get('作者单位：', ''),
        result.get('主题词:', '')
    ]

def main():
    result = parser()
    print(result)

if __name__ == '__main__':
    main()