#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
from utils import write2csv

def getUrl():
    urls = []
    for j in range(8):
        url = 'http://moocs.unipus.cn/course/explore?filter%5Btype%5D=all&filter%5Bprice%5D=all&filter%5BcurrentLevelId%5D=all&orderBy=recommendedSeq&page=' + str(j)
        res = requests.get(url)
        soup = bs(res.text,'html.parser')
        for i in range(len(soup.select('.col-lg-12 .course-info__pc a'))):
            url = 'http://moocs.unipus.cn' + soup.select('.col-lg-12 .course-info__pc a')[i].attrs['href'].strip()
            urls.append(url)
    return urls


def parse():
    urls = getUrl()
    for url in urls:
        try:
            result = {}
            res = requests.get(url)
            soup = bs(res.text,'html.parser')
            result['页面链接'] = url
            result['标题'] = soup.select('.course-detail__title')[0].text.strip()
            result['封面图片'] = soup.select('.course-detail-img img')[0].attrs['src'].strip()
            result['分类'] = soup.select('.breadcrumb-o li')[1].text.strip()
            result['价格'] = soup.select('.course-detail__price')[0].text.strip()
            try:
                result['课程来源'] = soup.select('.gray-dark')[0].text.strip()
                result['参与人数'] = soup.select('.gray-dark')[2].text.strip().replace('人已参与','')
            except:
                result['课程来源'] = ''
                result['参与人数'] = ''
            result['开课时间'] =soup.select('.panel-body p')[0].text.strip().replace('开始：','')
            result['结课时间'] = soup.select('.panel-body p')[1].text.strip().replace('截止：', '')
            details = soup.select('.es-piece')
            for i in range(len(soup.select('.es-piece'))):
                label = details[i].select('.piece-header')[0].text.strip()
                value = details[i].select('.piece-body')[0].text.strip().replace('\n','').replace('\xa0','').replace('\r','')
                result[label] = value
            result['开课时间'] = result['开课时间'].replace('/','-')
            result['结课时间'] = result['结课时间'].replace('/', '-')
            names = []
            for j in range(len(soup.select('.row .media-body .link-dark'))):
                names.append(soup.select('.row .media-body .link-dark')[j].text.strip())
            result['教学老师'] = ';'.join(names)
            print(result)
            write2csv('中国高校外语慕课平台.csv',[
                              result.get('页面链接', ''),
                              result.get('标题',''),
                              result.get('封面图片', ''),
                              result.get('分类', ''),
                              result.get('价格', ''),
                              result.get('课程来源', ''),
                              result.get('参与人数', ''),
                              result.get('开课时间', ''),
                              result.get('结课时间', ''),
                              result.get('课程概述', ''),
                              result.get('课程介绍', ''),
                              result.get('课程目标', ''),
                              result.get('适合人群', ''),
                              result.get('教学老师', '')
                      ])
        except Exception as e:
            print(e)
            print('*********网页犯病了*********')
        continue



def main():
    parse()

if __name__ == '__main__':
    main()