#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
import time
from utils import write2csv

def nexturl(url,current_page):
    data = {
        'memcached': 'disabled',
        'libId': '402834c3361fffed0136239dfe2f002d',
            'id': '402834c3361fffed0136239dfe2f002d',
    'singleLibList':'',
    'indexValue':'',
    'isPage': '0',
    'showName':'',
    'fieldValue':'',
    'resultInfo':'',
    'input':'',
    'Flag': 'simpleSearch',
    'subjectId': '402834c3361fffed0136239dfe2f002d',
    'treeTId':'',
    'orderSelected': 'default',
    'TITLE_input':'',
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
    'CAT4_rel': 'and',
    'CAT4_m': 'true',
    'CAT5_input':'',
    'CAT5_rel': 'and',
    'CAT5_m': 'true',
    'CAT6_input':'',
    'CAT6_rel': 'and',
    'CAT6_m': 'true',
    'CAT7_input':'',
    'CAT7_rel': 'and',
    'CAT7_m': 'true',
    'CAT8_input':'',
    'CAT8_rel': 'and',
    'CAT8_m': 'true',
    'CAT9_input':'',
    'CAT9_m': 'true',
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
    result['图片标题'] = title
    pictureurl = 'http://mylib.nlc.cn' + soup.select('.img_thumbnail_container img')[0].attrs['src'].strip()
    result['图片链接'] = pictureurl
    divs = soup.select('.item_single')
    for div in divs:
        label = div.select('.highlight')[0].text.strip()
        value = div.select('.item_content')[0].text.strip()
        result[label] = value
    result['页面链接'] = onepage_url
    return [
        result.get('图片标题', ''),
        result.get('图片链接', ''),
        result.get('著录编号', ''),
        result.get('责任者', ''),
        result.get('版本说明', ''),
        result.get('装帧形式', ''),
        result.get('典藏號', ''),
        result.get('收藏單位', ''),
        result.get('题跋印记', ''),
        result.get('页面链接','')
    ]


def main():
    url = 'http://mylib.nlc.cn/web/guest/zhonghuagujishanben?p_p_id=010453_WAR_system&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-3&p_p_col_pos=1&p_p_col_count=2&_010453_WAR_system_struts.portlet.action=%2Fsecondarysearch%2Fsecondarysearch%2FzhonghuagujiInitSearch&_010453_WAR_system_struts.portlet.mode=view'
    for i in range(325,350):
        print('正在爬取第%d页' %i)
        html = nexturl(url, i)
        # print(html)
        #获得当前页面所有详情页的链接
        soup = bs(html, 'html.parser')
        for j in range(len(soup.select('.result_item_img a'))):
            onepage_url = soup.select('.result_item_img a')[j].attrs['href'].strip()
            try:
                result = parser(onepage_url)
            except:
                time.sleep(8)
                result = parser(onepage_url)
            print(result)
            write2csv('中华古籍善本3.csv',result)



if __name__ == '__main__':
    main()