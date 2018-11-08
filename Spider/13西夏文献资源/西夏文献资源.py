#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
import time
from utils import write2csv

def nexturl(url, current_page):
    data = {
        'memcached': 'disabled',
    'libId': '40283415347ed8bd0134834d5232000e',
    'id': '40283415347ed8bd0134834d5232000e',
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
    'SUBJECT_input':'' ,
    'SUBJECT_rel': 'and',
    'SUBJECT_m': 'true',
    'RESERVE2_input':'' ,
    'RESERVE2_rel': 'and',
    'RESERVE2_m': 'true',
    'NUM1_input':'' ,
    'NUM1_rel': 'and',
    'NUM1_m': 'true',
    'NUM2_input':'' ,
    'NUM2_m': 'true',
    'order': 'default',
    'page.currentPage': current_page
    }
    try:
        res = requests.post(url,data=data)
        return res.text
    except:
        time.sleep(8)
        res = requests.post(url, data=data)
        return res.text


def parser(onepage_url):
    result = {}
    res = requests.get(onepage_url)
    soup = bs(res.text,'html.parser')
    title = soup.select('.meta_title_text')[0].text.strip()
    result['标题'] = title
    divs = soup.select('.metaContent_container .item_single')
    for div in divs:
        label = div.select('.item_title')[0].text.strip()
        value = div.select('.item_content')[0].text.strip()
        result[label] = value
    result['页面链接'] = onepage_url
    return [
        result.get('标题', ''),
        result.get('卷次', ''),
        result.get('文种', ''),
        result.get('版本', ''),
        result.get('出版年', ''),
        result.get('数量与尺寸', ''),
        result.get('版画情况', ''),
        result.get('主题词', ''),
        result.get('四部分类',''),
        result.get('页面链接', '')
    ]


def main():
    url = 'http://mylib.nlc.cn/web/guest/search/searchresult?p_p_id=010403_WAR_system&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_010403_WAR_system_struts.portlet.action=%2Fsecondarysearch%2Fsecondarysearch%2Fconditionssearch&_010403_WAR_system_struts.portlet.mode=view'
    for i in range(2,14):
        html = nexturl(url, i)
        print('正在爬取第%d页' % i)
        soup = bs(html,'html.parser')
        for j in range(len(soup.select('.result_item_first a'))):
            onepage_url = soup.select('.result_item_first a')[j].attrs['href'].strip()
            try:
                result = parser(onepage_url)
            except:
                time.sleep(8)
                result = parser(onepage_url)
            print(result)
            write2csv('西夏著论资源.csv', result)

if __name__ == '__main__':
    main()