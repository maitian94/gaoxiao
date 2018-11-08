#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

def parse():
    url = 'https://online-learning.harvard.edu/course/nazi-cinema-art-propaganda'
    result = {}
    res = requests.get(url)
    soup = bs(res.text,'html.parser')
    result['页面链接'] = ''
    result['课程标题'] = soup.select('.hero-title')[0].text.strip()
    result['课程概述'] = soup.select('.hero-blurb')[0].text.strip()
    result['封面图片'] = soup.select('.intro-top .span_4 img')[0].attrs['src'].strip()
    tables = soup.select('.course-header-stats table')
    for table in tables:
        label = table.select('th')[0].text.strip()
        value = table.select('td a')[0].text.strip()
        result[label] = value
    result['课程介绍'] = soup.select('.course-introduction')[0].text.replace('Introduction\n','').replace('\n','').strip()
    try:
        result['作者姓名'] = soup.select('.meet-the-author--author-name')[0].text.strip()
        result['作者职务'] = soup.select('.meet-the-author--author-title')[0].text.strip()
        result['作者介绍'] = soup.select('.meet-the-author--description p')[0].text.strip()
    except:
        result['作者姓名'] = ''
        result['作者职务'] = ''
        result['作者介绍'] = ''
    td_num = len(soup.select('.course-header-stats table'))
    result['证书'] = soup.select('td')[int(td_num)].text.strip()
    result['费用'] = soup.select('td')[int(td_num)+1].text.strip()
    # return result
    return [
        result.get('页面链接', ''),
        result.get('课程标题', ''),
        result.get('课程概述', ''),
        result.get('封面图片', ''),
        result.get('Category', ''),
        result.get('Faculty', ''),
        result.get('School', ''),
        result.get('Division', ''),
        result.get('课程介绍', ''),
        result.get('作者姓名', ''),
        result.get('作者职务', ''),
        result.get('作者介绍', ''),
        result.get('证书', ''),
        result.get('费用', '')
    ]





def main():
    result = parse()
    print(result)

if __name__ == '__main__':
    main()