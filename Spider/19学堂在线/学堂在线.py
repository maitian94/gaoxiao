# coding=utf8
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
from utils import write2csv
from pprint import pprint


def parse():
    result = {}
    for j in range(115, 163):
        try:
            url = 'http://www.xuetangx.com/courses?credential=0&page_type=0&cid=0&process=0&org=0&course_mode=0&page=' + str(j)
            res = requests.get(url)
            print(url)
            soup = bs(res.text, 'html.parser')
            for i in range(len(soup.select('#list_style .list_inner'))):
                detail_url = 'http://www.xuetangx.com' + soup.select('.img a')[i].attrs['href'].strip()
                result['详情页面链接'] = detail_url
                result['封面图片'] = 'http://www.xuetangx.com' + soup.select('.img img')[i].attrs['src'].strip()
                result['课程标题'] = soup.select('.coursetitle')[i].text.strip()
                try:
                    try:
                        result['所属学科'] = ';'.join([soup.select('.coursename_ref')[i].select('.subject')[0].text.strip(),soup.select('.coursename_ref')[i].select('.subject')[1].text.strip()])
                    except:
                        result['所属学科'] = soup.select('.coursename_ref')[i].select('.subject')[0].text.strip()
                except:
                    result['所属学科'] = ''
                try:
                    result['简介'] = soup.select('.txt_all .txt')[i].text.strip().replace('简介', '').replace('\t', '').replace(
                        '\r\n', '').replace('\n', '')
                except:
                    result['简介'] = soup.select('.txt_all .ktxt')[i].text.strip().replace('简介', '').replace('\n', '')
                driver = webdriver.PhantomJS(r'D:\Wangyuanyuan\工作\爬虫\phantomjs.exe')
                driver.get(detail_url)
                time.sleep(0.1)
                soup1 = bs(driver.page_source, 'html.parser')
                result['课程来源'] = soup1.select('.courseabout_text a')[0].text.strip()
                result['课程描述'] = soup1.select('.course_intro .text')[0].text.strip()
                result['开课时间'] = soup1.select('.illustrate span span')[0].text.strip().replace('.', '-')
                result['结课时间'] = soup1.select('.illustrate span span')[1].text.strip().replace('.', '-')
                result['报名人数'] = soup1.select('.illustrate span span')[5].text.strip()
                teachers = soup1.select('.teacher_info .cf')
                teacher_info = []
                for teacher in teachers:
                    one_teacher = ','.join([teacher.select('.teacher_text span')[0].text.strip(),
                                            teacher.select('.teacher_text span')[1].text.strip()])
                    teacher_info.append(one_teacher)
                result['教师信息'] = ';'.join(teacher_info)
                print(result)
                write2csv('学堂在线.csv',[
                        result.get('详情页面链接', ''),
                        result.get('封面图片', ''),
                        result.get('课程标题', ''),
                        result.get('所属学科', ''),
                        result.get('简介', ''),
                        result.get('课程来源', ''),
                        result.get('课程描述', ''),
                        result.get('开课时间', ''),
                        result.get('结课时间', ''),
                        result.get('报名人数', ''),
                        result.get('教师信息', '')
                    ])
        except Exception as e:
            print(e)
            print('*********网页犯病了*********')
        continue


def test():
    detail_url = 'http://www.xuetangx.com/courses/course-v1:TsinghuaX+20220332X+sp/about'
    driver = webdriver.PhantomJS(r'D:\Wangyuanyuan\工作\爬虫\phantomjs.exe')
    driver.get(detail_url)
    time.sleep(0.1)
    soup1 = bs(driver.page_source, 'html.parser')
    a = soup1.select('.illustrate span span')[0].text.strip().replace('.', '-')
    print(a)



    # url = 'http://www.xuetangx.com/courses?credential=0&page_type=0&cid=0&process=0&org=0&course_mode=0&page=162'
    # res = requests.get(url)
    # soup = bs(res.text,'html.parser')
    # for i in range(len(soup.select('#list_style .list_inner'))):
    #     b = soup.select('.txt_all .ktxt')[i].text.strip().replace('简介', '').replace('\n', '')
    #     print(b)



def main():
    parse()
    # test()


if __name__ == '__main__':
    main()