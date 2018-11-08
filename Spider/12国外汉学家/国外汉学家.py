#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
import time
from utils import write2csv

def nexturl(url, current_page):
    data = {
        'p_p_id': '010403_WAR_system',
            'p_p_lifecycle': '0',
    'p_p_state': 'normal',
    'p_p_mode': 'view',
    'p_p_col_id': 'column - 1',
    'p_p_col_count': '1',
    '_010403_WAR_system_struts.portlet.action': '/ secondarysearch / secondarysearch / conditionssearch',
    '_010403_WAR_system_struts.portlet.mode': 'view',
    'memcached': 'disabled',
    'libId': '40283415347ed8bd0134834e328f000f',
    'id': '40283415347ed8bd0134834e328f000f',
    'singleLibList': '1',
    'indexValue':'',
    'isPage': '0',
    'showName':'',
    'fieldValue':'',
    'resultInfo':'',
    'orderSelected': 'default',
    'resultFormality':'',
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
    'CAT4_rel': 'and',
    'CAT4_m': 'true',
    'NUM1_input':'',
    'NUM1_rel': 'and',
    'NUM1_m': 'true',
    'NUM2_input':'',
    'NUM2_rel': 'and',
    'NUM2_m': 'true',
    'NUM3_input':'',
    'NUM3_m': 'true',
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
    divs = soup.select('.metaContent_container .item_single')
    for div in divs:
        label = div.select('.item_title')[0].text.strip()
        value = div.select('.item_content')[0].text.strip().replace('<imgsrc','').replace('<br>','').replace('\u3000',' ')
        result[label] = value
    result['页面链接'] = onepage_url
    # return result
    return [
        result.get('姓名', ''),
        result.get('中文译名', ''),
        result.get('国籍', ''),
        result.get('生卒年月', ''),
        result.get('研究领域', ''),
        result.get('人物介绍', ''),
        result.get('主要研究成果', ''),
        result.get('参考文献', ''),
        result.get('页面链接','')
    ]


def main():
    url = 'http://mylib.nlc.cn/web/guest/search/searchresult?p_p_id=010403_WAR_system&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_010403_WAR_system_struts.portlet.action=%2Fsecondarysearch%2Fsecondarysearch%2Fconditionssearch&_010403_WAR_system_struts.portlet.mode=view'
    for i in range(2,16):
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
            write2csv('国外汉学家1.csv', result)

if __name__ == '__main__':
    main()