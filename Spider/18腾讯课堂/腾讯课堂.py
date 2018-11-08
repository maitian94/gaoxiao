#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
import re
from utils import write2csv,writeurl2txt

def title_url():
    title_urls = []
    # lists1 = ['2003','2004', '2005', '2043', '2009', '2010', '2002', '2008', '2006', '2007', '2001']
    # for list in lists1:
    #     url = 'https://ke.qq.com/course/list?mt=1001' + '&st=' + list
    #     title_urls.append(url)
    # lists2 = ['2011','2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2041']
    # for list in lists2:
    #     url = 'https://ke.qq.com/course/list?mt=1002' + '&st=' + list
    #     title_urls.append(url)
    # lists3 = ['2020', '2021', '2022', '2023', '2024', '2025']
    # for list in lists3:
    #     url = 'https://ke.qq.com/course/list?mt=1003' + '&st=' + list
    #     title_urls.append(url)
    # lists4 = ['2027', '2046', '2028', '2039', '2029', '2044']
    # for list in lists4:
    #     url = 'https://ke.qq.com/course/list?mt=1004' + '&st=' + list
    #     title_urls.append(url)
    lists5 = ['2031', '2042', '2032', '2033', '2034']
    for list in lists5:
        url = 'https://ke.qq.com/course/list?mt=1005' + '&st=' + list
        title_urls.append(url)
    lists6 = ['2035', '2047', '2037', '2049', '2036', '2038']
    for list in lists6:
        url = 'https://ke.qq.com/course/list?mt=1006' + '&st=' + list
        title_urls.append(url)
    return title_urls

def get_allurl():
    title_urls = title_url()
    print(title_urls)
    allurls = []
    for url in title_urls:
        # print(url)
        res = requests.get(url)
        soup = bs(res.text, 'html.parser')
        pagenum = soup.select('.sort-page a')[-2].text.strip()
        for z in range(int(pagenum)+1):
            urls = url + '&task_filter=0000000&&page=' + str(z)
            # print(urls)
            res1 = requests.get(urls)
            soup1 = bs(res1.text,'html.parser')
            try:
                for i in range(len(soup1.select('li .item-img-link')) - 12):
                    onepage_url = 'https:' + soup1.select('.course-card-item .item-tt a')[i].attrs['href'].strip()
                    print(onepage_url)
                    allurls.append(onepage_url)
            except:
                for j in range(len(soup1.select('.c-list li'))):
                    onepage_url = 'https:' + soup1.select('.c-list .c-item-left')[j].attrs['href']
                    print(onepage_url)
                    allurls.append(onepage_url)
    return allurls
    # print(allurls)
    # print(len(allurls))

def ppp():
    url ='https://ke.qq.com/course/336177'
    res = requests.get(url)
    soup = bs(res.text,'html.parser')
    a =soup.select('.tree-list span')[2].attrs['data-num'].strip()
    print(a)







def parse():
    allurls = get_allurl()
    print(allurls)
    print(len(allurls))
    result = {}
    for url in allurls:
        print(url)
        if 'package' not in url:
            writeurl2txt('腾讯课堂url.txt',url)
            try:
                res = requests.get(url)
                soup = bs(res.text,'html.parser')
                result['封面图片'] = 'https://' + soup.select('.img-left--wrap img')[0].attrs['src'].strip()
                result['课程名称'] = soup.select('.title-main')[0].text.strip()
                try:
                    zuijinzaixue = soup.select('#js-statistics-apply')[0].text.strip()
                    result['最近在学人数'] = re.findall('\d+',zuijinzaixue)[0]
                    result['累计报名'] = soup.select('.js-apply-num')[0].text.strip()
                except:
                    result['购买人数'] = soup.select('#js-statistics-apply')[0].text.strip().replace('人 购买','')
                result['好评度'] = soup.select('.rate-num')[0].text.strip()
                result['课程价格'] = soup.select('.course-price-info ')[0].text.strip().replace('¥','')
                tnames = []
                for teacher in soup.select('.teacher-list .teacher-item'):
                    tname = teacher.select('.js-teacher-name')[0].text.strip()
                    tnames.append(tname)
                result['讲师姓名'] = ';'.join(tnames)
                result['课程介绍'] = soup.select('.tb-course td')[0].text.strip()
                result['授课机构名称'] = soup.select('.js-agency-name')[0].text.strip()
                result['机构好评度'] = soup.select('.tree-list span')[0].text.strip()
                result['机构课程数'] = soup.select('.tree-list span')[1].attrs['data-num'].strip()
                result['学习人次'] = soup.select('.tree-list span')[2].attrs['data-num'].strip()
                result['机构介绍'] = soup.select('.agency-summary')[0].text.strip()
                contacts = []
                for i in range(len(soup.select('.contact-list p'))):
                    contacts.append(soup.select('.contact-list p')[i].text.strip())
                result['联系方式'] = ';'.join(contacts)
                result['页面链接'] = url
                print(result)
                write2csv('腾讯课堂.csv', [
                    result.get('页面链接', ''),
                    result.get('封面图片', ''),
                    result.get('课程名称', ''),
                    result.get('最近在学人数', ''),
                    result.get('累计报名', ''),
                    result.get('购买人数', ''),
                    result.get('好评度', ''),
                    result.get('课程价格', ''),
                    result.get('讲师姓名', ''),
                    result.get('课程介绍', ''),
                    result.get('授课机构名称', ''),
                    result.get('机构好评度', ''),
                    result.get('机构课程数', ''),
                    result.get('学习人次', ''),
                    result.get('机构介绍', ''),
                    result.get('联系方式', '')
                ])
            except Exception as e:
                print(e)








def main():
    # title_url()
    parse()
    # get_allurl()
    # ppp()

if __name__ == '__main__':
    main()
