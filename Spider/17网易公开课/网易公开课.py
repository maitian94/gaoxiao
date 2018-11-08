#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
from utils import write2csv,writeurl2txt
import re



def geturl():
    url = 'https://c.open.163.com/search/search.htm?query=&enc=#/search/course?ca=TED&sj=&sh='
    driver = webdriver.PhantomJS(r'D:\Wangyuanyuan\工作\爬虫\phantomjs.exe')
    driver.get(url)
    time.sleep(0.1)
    page = 1
    urlslist = []
    while page < 160:
        soup = bs(driver.page_source,'html.parser')
        for i in range(0, len(soup.select('.cnt a')), 2):
            urls = soup.select('.cnt a')[i].attrs['href']
            urlslist.append(urls)
        nextpg = driver.find_element_by_class_name('znxt')
        nextpg.click()
        # time.sleep(0.1)
        print('已翻到第%s页'%page)
        page += 1
    return urlslist


def parse():
    urlslist = geturl()
    print(urlslist)
    print(len(urlslist))
    for url in urlslist:
        print(url)
        try:
            if 'movie' in url:
                failedurl = []
                result = {}
                res = requests.get(url)
                soup = bs(res.text,'html.parser')
                result['页面链接'] = soup.select('.u-ptl-c a')[0].attrs['href'].strip()
                result['图片链接'] = soup.select('.u-ptl-c img')[0].attrs['src'].strip()
                result['标题'] = soup.select('.u-ptl-c a')[1].text.strip()
                for i in range(len(soup.select('.u-ptl-c p'))):
                    label = soup.select('.u-ptl-c p')[i].text.split('：',1)[0].strip()
                    value = soup.select('.u-ptl-c p')[i].text.split('：',1)[1].strip()
                    result[label] = value
                driver = webdriver.PhantomJS(r'D:\Wangyuanyuan\工作\爬虫\phantomjs.exe')
                driver.get(url)
                soup = bs(driver.page_source, 'html.parser')
                result['跟帖人数'] = soup.select('.tie-info a')[0].text.strip()
                result['参与人数'] = soup.select('.tie-info a')[1].text.strip()
                print(result)
                write2csv('网易公开课_movie.csv', [
                    result.get('页面链接', ''),
                    result.get('图片链接', ''),
                    result.get('标题', ''),
                    result.get('别名', ''),
                    result.get('学校', ''),
                    result.get('讲师', ''),
                    result.get('导演', ''),
                    result.get('制片国家/地区', ''),
                    result.get('集数', ''),
                    result.get('授课语言', ''),
                    result.get('类型', ''),
                    result.get('简介', ''),
                    result.get('课程简介', ''),
                    result.get('跟帖人数', ''),
                    result.get('参与人数', '')
                ])
            elif 'special' in url:
                result = {}
                print(url)
                failedurl = []
                driver = webdriver.PhantomJS(r'D:\Wangyuanyuan\工作\爬虫\phantomjs.exe')
                driver.get(url)
                time.sleep(0.1)
                soup = bs(driver.page_source, 'html.parser')
                result['课程标题'] = soup.select('.m-cdes h2')[0].text.strip()
                result['图片链接'] = soup.select('.m-cintro img')[0].attrs['src'].strip()
                jishu = soup.select('.m-cdes p')[0].text.strip()
                result['集数'] = re.findall('.*?(\d+).*?', jishu)[0].strip()
                result['课程介绍'] = soup.select('.m-cdes p')[2].text.strip()
                result['讲师图片'] = soup.select('.picText img')[0].attrs['src'].strip()
                details = soup.select('.picText')
                for detail in details:
                    for i in range(len(soup.select('.picText h6'))):
                        pp = detail.select('h6')[i].text
                        if pp:
                            try:
                                label = detail.select('h6')[i].text.split('：', 1)[0].strip()
                                value = detail.select('h6')[i].text.split('：', 1)[1].strip()
                                result[label] = value
                            except:
                                result[label] = ''
                result['学院介绍'] = soup.select('.cContent')[0].text.strip()
                result['跟帖人数'] = soup.select('.tie-info a')[0].text.strip()
                result['参与人数'] = soup.select('.tie-info a')[1].text.strip()
                result['页面链接'] = url
                    # print(result)
                write2csv('网易公开课_special.csv', [
                        result.get('页面链接', ''),
                        result.get('图片链接', ''),
                        result.get('课程标题', ''),
                        result.get('集数', ''),
                        result.get('课程介绍', ''),
                        result.get('讲师图片', ''),
                        result.get('名称', ''),
                        result.get('讲师', ''),
                        result.get('介绍', ''),
                        result.get('职业', ''),
                        result.get('学位', ''),
                        result.get('学院介绍', '')
                    ])
        except Exception as e:
            print(e)
            print('special网页结构不一样')
        continue




def main():
    parse()




if __name__ == '__main__':
    main()

