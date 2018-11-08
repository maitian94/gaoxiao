#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
import time
from utils import write2csv

def nexturl(url, current_page):
    data = {
        'memcached': 'disabled',
    'libId': '40283415347ed8bd0134834f9a650011',
    'id': '40283415347ed8bd0134834f9a650011',
    'singleLibList': '1',
    'indexValue': '',
    'isPage': '0',
    'showName':'' ,
    'fieldValue':'' ,
    'resultInfo':'' ,
    'orderSelected':'',
    'resultFormality':'' ,
    'TITLE_input':'' ,
    'TITLE_rel': 'and',
    'TITLE_m': 'true',
    'CREATE_USER_input':'',
    'CREATE_USER_rel': 'and',
    'CREATE_USER_m': 'true',
    'CAT1_input':'',
    'CAT1_rel': 'and',
    'CAT1_m': 'true',
    'CAT2_input':'',
    'CAT2_rel': 'and',
    'CAT2_m': 'true',
    'CAT3_input':'',
    'CAT3_rel': 'and',
    'CAT3_m': 'true',
    'CAT4_input':'',
    'CAT4_m': 'true',
    'order': 'default',
    'page.currentPage': current_page
    }
    try:
        res = requests.post(url,data=data)
        return res.text
    except:
        time.sleep(10)
        res = requests.post(url, data=data)
        return res.text


def parser(onepage_url):
    result = {}
    res = requests.get(onepage_url)
    soup = bs(res.text,'html.parser')
    title = soup.select('.meta_title')[0].text.strip()
    result['标题'] = title
    divs = soup.select('.metaContent_container .item_single')
    for div in divs:
        label = div.select('.item_title')[0].text.strip()
        value = div.select('.item_content')[0].text.strip().replace('@@@', ' ')
        result[label] = value
    result['页面链接'] = onepage_url
    return [
        result.get('标题', ''),
        result.get('主题词', ''),
        result.get('责任者', ''),
        result.get('出版时间', ''),
        result.get('ISSN', ''),
        result.get('刊名', ''),
        result.get('页面链接', '')
    ]


def main():
    url = 'http://mylib.nlc.cn/web/guest/search/searchresult?p_p_id=010403_WAR_system&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_010403_WAR_system_struts.portlet.action=%2Fsecondarysearch%2Fsecondarysearch%2Fconditionssearch&_010403_WAR_system_struts.portlet.mode=view'
    for i in range(113,122):
        html = nexturl(url, i)
        print('正在爬取第%d页' % i)
        soup = bs(html,'html.parser')
        for j in range(len(soup.select('.result_item_first a'))):
            onepage_url = soup.select('.result_item_first a')[j].attrs['href'].strip()
            try:
                result = parser(onepage_url)
            except:
                time.sleep(10)
                result = parser(onepage_url)
            print(result)
            write2csv('西夏著论资源.csv', result)

if __name__ == '__main__':
    main()