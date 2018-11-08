# coding=utf-8
import requests
from bs4 import BeautifulSoup as bs
from utils import write2csv,writeurl2txt
from pprint import pprint
import time

def next_page():
    urls = []
    for i in range(18,19):
        next_url = 'http://www.pharmnet.com.cn/tcm/zybb/index.cgi?p='+str(i)+'&f=&terms=&s1=&cate1=&cate2='
        res = requests.get(next_url)
        soup = bs(res.text,'html.parser')
        for j in range(0,24,2):
            url = 'http://www.pharmnet.com.cn' + soup.select('table .border td .border a')[j].attrs['href'].strip()
            urls.append(url)
            writeurl2txt('中药图谱url.txt',url)
    # return urls


def parser(url):
    result = {}
    try:
        res = requests.get(url)
        result['Url'] = url
        soup = bs(res.text, 'html.parser')
        # content = soup.select('#fontsize')[0].text
        # print(repr(content))
        # pprint(content.split('\r\n'))
        contents = soup.select('#fontsize')[0].text.strip().split('\r\n')
        ziduans = ['名称', '类别', '拼音：', '拉丁', '别名', '药用部位', '药材性状', '栽培要点', '产地', '采收加工',
                   '地道沿革', '性味归经', '功能主治', '用法用量', '禁忌']
        details = []
        for content in contents:
            for ziduan in ziduans:
                if ziduan in content:
                    details.append(content)
        for detail in details:
            detail = detail.split('：', 1)
            lable = detail[0].strip()
            value = detail[1].strip()
            result[lable] = value
        href = soup.select('.maintext a')[0].attrs['href']
        result['图片'] = href
        return [
            result.get('名称', ''),
            result.get('类别', ''),
            result.get('拼音', ''),
            result.get('拉丁', ''),
            result.get('别名', ''),
            result.get('药用部位', ''),
            result.get('药材性状', ''),
            result.get('栽培要点', ''),
            result.get('产地', ''),
            result.get('采收加工', ''),
            result.get('地道沿革', ''),
            result.get('性味归经', ''),
            result.get('功能主治', ''),
            result.get('用法用量', ''),
            result.get('禁忌', ''),
            result.get('图片', ''),
            result.get('Url','')
        ]
    except:
        time.sleep(20)
        parser(url)


def main():
    urls = next_page()
    for url in urls:
        print(url)
        result = parser(url)
        print(result)
        write2csv('csvFiles/中药图谱.csv', result)

if __name__ == '__main__':
    # main()
    next_page()