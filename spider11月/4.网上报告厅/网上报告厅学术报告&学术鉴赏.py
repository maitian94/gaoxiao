#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from utils import *


def parse():
    for i in range(1,145):
        page_url = 'http://www.wsbgt.com/Course?firstcId=0&cataType=xsjs&PageIndex=' + str(i)
        print('爬虫进行到第{0}页'.format(i))
        res = requests.get(page_url)
        soup = bs(res.text,'html.parser')
        # driver = webdriver.Chrome(r'D:\Wangyuanyuan\工作\爬虫\chromedriver.exe')
        # driver.get(url)
        # soup = bs(driver.page_source,'html.parser')
        dls = soup.select('.courseListVer dl')
        for dl in dls:
            url = 'http://www.wsbgt.com' + dl.select('dt a')[0].attrs['href'].strip()
            writeurl2txt('data/网上报告厅学术报告&学术鉴赏_Url.txt',url)
            picture_url = dl.select('dt img')[0].attrs['src'].strip()
            title = dl.select('dd h3')[0].text.strip()
            #主讲
            zhujiang = dl.select('.info .light-gray333')[0].text.strip()
            #分类
            category = dl.select('.info .light-gray333')[1].text.strip()
            #课时
            lessons = dl.select('.info .light-gray333')[2].text.strip()
            #发布时间
            time = dl.select('.info .light-gray333')[3].text.replace('/','-').strip()
            introduction = dl.select('.desc')[0].text.replace('\r\n','').replace('\r','').replace('\n','').replace('简介：','').strip()
            #分课程
            tips = []
            for i in range(len(dl.select('.showMore a'))):
                tip = dl.select('.showMore a')[i].text.strip()
                tips.append(tip)
            tips = ';'.join(tips)
            type_ = '学术鉴赏'
            result = [type_, url, picture_url, title, zhujiang, category, lessons, time, introduction, tips]
            print(result)
            write2csv('data/网上报告厅学术报告&学术鉴赏.csv',result)





if __name__ == '__main__':
    # write2csv('data/网上报告厅学术报告&学术鉴赏.csv',['类别' ,'详情页链接' ,'图片链接' , '标题', '主讲' ,'分类' ,'课时' , '发布时间','简介' ,'小标题' ])
    parse()