#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
from utils import *
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from pprint import pprint

def getUrl():
    with open(r'C:\Users\admin\PycharmProjects\spider11月\2.coursera网课\data\coursera_Url.txt','r') as file:
        lines = file.readlines()
        urls = []
        for url in lines:
            url = url.replace('\n','').strip()
            urls.append(url)
        return urls

def parse():
    urls = getUrl()
    print(len(urls))
    for url in urls:
        print(url)
        res = requests.get(url)
        soup = bs(res.content.decode('utf-8'),'html.parser')
        num = len(soup.select('.week'))
        if num == 0:
            writeurl2txt('data/failedurl.txt',url)
            continue
        title = soup.select('.display-3-text')[0].text.strip()
        categorys = []
        category_num = len(soup.select('.rc-BannerBreadcrumbs .item'))
        for i in range(1, category_num):
            category = soup.select('.rc-BannerBreadcrumbs .item')[i].text.strip()
            categorys.append(category)
        if category_num == 2:
            categorys_ = categorys[0]
        else:
            categorys_ = '>'.join(categorys)
        tips = []
        weeks = soup.select('.week')
        for week in weeks:
            tip = week.select_one('.headline-2-text').text.strip()
            tips.append(tip)
        tips = ';'.join(tips)
        introduction = soup.select('.course-description')[0].text.replace('\n', '').replace('关于此课程：', '').replace(
            'About this course:', '').strip()
        source = soup.select('.creator-names span')[1].text.strip()
        teachers = []
        lis = soup.select('.instructors-section li')
        for li in lis:
            teacher = li.select('.body-1-text a')[0].text.strip()
            teachers.append(teacher)
        teachers = ';'.join(teachers)
        language = soup.select('.rc-Language')[0].text.strip()
        try:
            stars = soup.select('.ratings-info .bt3-hidden-xs')[0].text.strip()
            stars = re.sub('[\u4e00-\u9fa5]', '', stars).strip()
        except:
            stars = ''
        result = [url, title, categorys_, stars, introduction, source, language, tips, teachers]
        print(result)
        write2csv('data/coursera的网课.csv',result)



if __name__ == '__main__':
    # write2csv('data/coursera的网课.csv',  ['页面链接', '标题', '分类', '星级', '课程介绍', '课程来源',  '授课语言', '授课大纲', '教学人员'])
    parse()

