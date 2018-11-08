#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
from selenium import webdriver
import time
from utils import *



def parse():
    result = {}
    category_dic = {
        'Accounting, Finance & Economics': [
            'https://www.emeraldinsight.com/action/showPublications?category=10.1555%2Fcategory.40056886']
        # 'Business, Management & Strategy': [
        #     'https://www.emeraldinsight.com/action/showPublications?category=10.1555%2Fcategory.40527610']
        # 'Education': ['https://www.emeraldinsight.com/action/showPublications?category=10.1555%2Fcategory.40056804']
        # 'Engineering': ['https://www.emeraldinsight.com/action/showPublications?category=10.1555%2Fcategory.40057660']
        # 'Health & Social Care': [
        #     'https://www.emeraldinsight.com/action/showPublications?category=10.1555%2Fcategory.40057479']
        # 'HR, Learning & Organization Studies': [
        #     'https://www.emeraldinsight.com/action/showPublications?category=10.1555%2Fcategory.40057019']
        # 'Information & Knowledge Management': [
        #     'https://www.emeraldinsight.com/action/showPublications?category=10.1555%2Fcategory.40057110']
        # 'Library Studies': [
        #     'https://www.emeraldinsight.com/action/showPublications?category=10.1555%2Fcategory.40057696']
        # 'Marketing': ['https://www.emeraldinsight.com/action/showPublications?category=10.1555%2Fcategory.40057137']
        # 'Operations, Logistics & Quality': [
        #     'https://www.emeraldinsight.com/action/showPublications?category=10.1555%2Fcategory.40057257']
        # 'Property Management & Built Environment': [
        #     'https://www.emeraldinsight.com/action/showPublications?category=10.1555%2Fcategory.40057228']
        # 'Public Policy & Environmental Management': [
        #     'https://www.emeraldinsight.com/action/showPublications?category=10.1555%2Fcategory.40057620']
        # 'Sociology': ['https://www.emeraldinsight.com/action/showPublications?category=10.1555%2Fcategory.40057538']
        # 'Tourism & Hospitality': ['https://www.emeraldinsight.com/action/showPublications?category=10.1555%2Fcategory.40057413']
        # 'Transport': ['https://www.emeraldinsight.com/action/showPublications?category=10.1555/category.40057738']
    }
    for category in category_dic.items():
        start_url = category[1][0]
        type_ = category[0]
        print(type_)
        res1 = requests.get(start_url)
        soup1 = bs(res1.text,'html.parser')
        for w in range(29,33):
            page_url = start_url + '&startPage=' + str(w)
            res2 = requests.get(page_url)
            soup2 = bs(res2.text,'html.parser')

            print('正在处理第{0}页正在处理第{0}页正在处理第{0}页正在处理第{0}页'.format(w))
            for z in range(len(soup2.select('.browseItem a'))):
                url = 'https://www.emeraldinsight.com' + soup2.select('.browseItem a')[z].attrs['href']
                writeurl2txt('data/Emerald管理学全文期刊库.txt',url)

                result['分类'] = type_
                result['页面链接'] = url
                res = requests.get(url)
                soup = bs(res.text,'html.parser')
                # print(url)
                try:
                    try:
                        title = soup.select('.bookInfo h3')[0].text.strip()
                    except:
                        title = soup.select('.issueSerialNavigation h4')[0].text.strip()
                except:
                    title = ''
                result['标题'] = title
                try:
                    try:
                        pic_url = 'https://www.emeraldinsight.com' + soup.select('.publicationCoverImage img')[0].attrs['src']
                    except:
                        pic_url = 'https://www.emeraldinsight.com' + soup.select('.cover img')[0].attrs['src']
                except:
                    pic_url = ''
                result['图片链接'] = pic_url


                try:
                    for i in range(len(soup.select('.bookInfo')[0].text.split('\n'))):
                        details = soup.select('.bookInfo')[0].text.split('\n')[i].split(':')
                        # pprint(details)
                        try:
                            label = details[0].strip()
                            value = details[1].strip()
                        except:
                            label = ''
                            value = ''
                        result[label] = value
                    introduction = soup.select('.tabs-booksDetails')[0].text.strip()
                    result['介绍'] = introduction
                    tips = []
                    for i in range(len(soup.select('.title-group'))):
                        tip = soup.select('.title-group')[i].text.strip()
                        tips.append(tip)
                    tips = ';'.join(tips)
                    result['小标题'] = tips
                except:
                    print('页面结构不一样')
                try:
                    for i in range(len(soup.select('.info')[0].text.split('\n'))):
                        infos = soup.select('.info')[0].text.split('\n')[i].split(':')
                        # pprint(details)
                        try:
                            label = infos[0].strip()
                            value = infos[1].strip()
                        except:
                            label = ''
                            value = ''
                        result[label] = value
                except:
                    print('页面结构不一样')

                print(result)
                write2csv('data/Emerald管理学全文期刊库.csv',[
                result.get('分类', ''),
                result.get('页面链接',''),
                result.get('标题', ''),
                result.get('ISBN', ''),
                result.get('eISBN', ''),
                result.get('Edited by', ''),
                result.get('Published', ''),
                result.get('介绍', ''),
                result.get('小标题', ''),
                result.get('Book Series', ''),
                result.get('Series ISSN', ''),
                result.get('Series editor(s)', ''),
                result.get('Subject Area', ''),
                result.get('ISSN', ''),
                result.get('Subject Area', '')

            ])





if __name__ == '__main__':
    # write2csv('data/Emerald管理学全文期刊库.csv',['分类', '页面链接','标题','ISBN', 'eISBN', 'Edited by', 'Published', '介绍',
    #                                       '小标题', 'Book Series', 'Series ISSN', 'Series editor(s)',
    #                                       'Subject Area', 'ISSN', 'Subject Area'])
    parse()