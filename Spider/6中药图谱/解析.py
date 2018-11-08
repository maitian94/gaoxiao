# conding=utf8
import requests
from bs4 import BeautifulSoup as bs
import re
from utils import write2csv
from pprint import pprint

def next_page():
    urls = []
    for i in range(1,2):
        next_url = 'http://www.pharmnet.com.cn/tcm/zybb/index.cgi?p='+str(i)+'&f=&terms=&s1=&cate1=&cate2='
        res = requests.get(next_url)
        soup = bs(res.text,'html.parser')
        for j in range(0,72,2):
            url = 'http://www.pharmnet.com.cn' + soup.select('table .border td .border a')[j].attrs['href'].strip()
            urls.append(url)
    return urls


def parser(url):
    result = {}
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    # content = soup.select('#fontsize')[0].text
    # print(repr(content))
    # pprint(content.split('\r\n'))
    contents = soup.select('#fontsize')[0].text.strip().split('\r\n')
    print(repr(contents))
    ziduans = ['名称','类别','拼音','拉丁','别名','药用部位','药材性状','栽培要点','产地','采收加工',
              '地道沿革','性味归经','功能主治','用法用量','禁忌']
    details = []
    for content in contents:
        for ziduan in ziduans:
            if ziduan in content:
                details.append(content)
    print(details)
    for detail in details:
        detail = detail.split('：',1)
        lable = detail[0]
        value = detail[1]
        result[lable] = value
    href = soup.select('.maintext a')[0].attrs['href']
    result['图片'] = href
    return result



def main():
    url = 'http://www.pharmnet.com.cn/tcm/zybb/index.cgi?f=detail&id=670'
    result = parser(url)
    print(result)

if __name__ == '__main__':
    main()
