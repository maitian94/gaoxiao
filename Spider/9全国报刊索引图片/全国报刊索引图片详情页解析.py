#coding=utf8
import requests
from bs4 import BeautifulSoup as bs

def parser():
    result = {}
    res = requests.get('http://www.cnbksy.com/search/picDetail/25191e2d38fb12765898e03409f8e5e5/15/5ba205f123b099657e9b5e0d')
    soup = bs(res.text,'html.parser')
    pictureurl = 'http://www.cnbksy.com' + soup.select('.detailContainer div img')[0].attrs['src'].strip()
    result['图片链接'] = pictureurl
    tds = soup.select('.srTable tr td')
    for i in range(0,len(tds)-1,2):
        label = tds[i].text.strip().replace('\n','')
        value = tds[i+1].text.strip().replace('\n','')
        result[label] = value
    # return result
    return [
        result.get('图片链接', ''),
        result.get('图片标题：', ''),
        result.get('图片来源：', ''),
        result.get('图片类型：', ''),
        result.get('出版年份：', ''),
        result.get('收录卷期：', ''),
        result.get('图片大小：', ''),
        result.get( '图片尺寸：', ''),
        result.get('图片厘米尺寸：', ''),
    ]



def main():
    result = parser()
    print(result)

if __name__ == '__main__':
    main()