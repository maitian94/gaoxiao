# coding=utf8
import sys

import requests
from bs4 import BeautifulSoup
import threading
import redis
import time
import re
from utils import write2csv, getIP, csvStrProcess, writeurl2txt, txt2Redis
import logging
from datetime import datetime

today = datetime.today().date()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log/豆瓣读书_%s.log' % today,
                    filemode='a')
pool = redis.ConnectionPool(host='192.168.100.121', port=6379,
                            decode_responses=True)  # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
r1 = redis.Redis(connection_pool=pool)


def dbdsParser(detailUrl, html):
    soup = BeautifulSoup(html, 'html.parser')
    # 标题
    title = soup.select('#wrapper h1 span')[0].text.strip()

    # 书籍缩略图
    try:
        imgUrl = soup.select_one('.nbg').attrs['href']
    except:
        imgUrl = ''

    # 缩略图右边的书籍信息
    infoDic = {'作者': '',
               '出版社': '',
               '出品方': '',
               '译者': '',
               '出版年': '',
               '页数': '',
               '定价': '',
               '装帧': '',
               '丛书': '',
               'ISBN': '',
               '副标题': '',
               '原作名': '',
               }
    infos = soup.select_one('#info').text.replace('\xa0\n        \n            ', '').strip()
    infos = infos.replace('\n\n', '\n').replace('\xa0', '')
    infos = infos.replace('\n            ', '').replace('\n        \n        \n        ', '')

    infos = infos.replace('        ', '').replace(':\n', ':').replace('\n\n   /\n\n', '/').replace('\n  /\n', '/')
    infos = infos.replace('\n\n   /', '/')
    # print(repr(infos))

    infos = infos.split('\n')

    for info in infos:
        if len(info.strip()) == 0: continue
        # print(info)
        kv = info.split(':', 1)
        infoDic[kv[0]] = kv[1].strip()

    maincontent = soup.select_one('.related_info')
    h2s = maincontent.select('h2')[:3]
    indents = maincontent.select('.indent')
    # 3个重要字段：内容简介，作者简介，目录
    big3Dic = {'内容简介': '', '作者简介': '', '目录': ''}
    for h2, indent in zip(h2s, indents):
        try:
            k = h2.span.text.strip()
        except:
            continue
        # print(k)
        # k搞好搞v
        if k not in ['内容简介', '作者简介', '目录']: continue
        if k == '目录':
            v = indent.find_next_sibling("div").text.strip()
            v = v.strip('\n        目录\n        ').strip('     · · · · · ·     (收起)\n')
            v = v.replace('\u3000', ' ').replace('\n        ', '\n')
            # print(v)
            big3Dic[k] = v
            continue

        try:
            short = indent.select_one('.short .intro').text.strip()
        except:
            short = ''
        try:
            long = indent.select_one('.all .intro').text.strip()
        except:
            long = ''
        if not any([short, long]):
            v = indent.select_one('.intro').text.strip()
        else:
            if long:
                v = long
            else:
                v = short
        big3Dic[k] = v

    rating = soup.select('#interest_sectl .rating_num')[0].text.strip()

    print(
        [title, detailUrl, imgUrl, rating, infoDic['作者'], infoDic['出版社'], infoDic['出品方'], infoDic['译者'], infoDic['出版年'],
         infoDic['页数'], infoDic['定价'], infoDic['装帧'], infoDic['丛书'], infoDic['ISBN'],
         infoDic['副标题'], infoDic['原作名'], big3Dic['内容简介'], big3Dic['作者简介'], big3Dic['目录']])

    return [title, detailUrl, imgUrl, rating, infoDic['作者'], infoDic['出版社'], infoDic['出品方'], infoDic['译者'],
            infoDic['出版年'],
            infoDic['页数'], infoDic['定价'], infoDic['装帧'], infoDic['丛书'], infoDic['ISBN'],
            infoDic['副标题'], infoDic['原作名'], big3Dic['内容简介'], big3Dic['作者简介'], big3Dic['目录']]



def main(rds):
    # 从rds里取详情页url，请求 并 解析
    ip = getIP()
    flag = 1
    while flag:
        detailUrl = rds.spop('dbds')
        if not detailUrl:
            flag = 0
        try:
            res = requests.get(url=detailUrl, proxies={'https': ip}, verify=False)
            # time.sleep(1)
        except Exception as e:
            rds.sadd('dbds', detailUrl)
            ip = getIP()
            if not ip:
                sys.exit('IP用完了')
            print(f'请求出错，错误原因：\n{e}已更换IP：{ip}')
            logging.info(f'请求出错，错误原因：[{e}]，链接：{detailUrl}')
            continue

        if '检测到有异常' in res.text:
            ip = getIP()
            if not ip:
                sys.exit('IP用完了')
            print('检测到IP有异常，已更换IP：', ip)
            rds.sadd('dbds', detailUrl)

        if '页面不存在' in res.text:
            continue

        try:
            result = dbdsParser(detailUrl, res.text)
        except:
            writeurl2txt('data/解析错误的URL.txt',detailUrl)
        else:
            write2csv('data/豆瓣读书1030_2.csv', result)
            writeurl2txt('data/豆瓣读书存在的7位数URL.txt',detailUrl)

if __name__ == "__main__":
    # print(r1.scard('dbds'))
    tlist = []
    for i in range(150):
        t = threading.Thread(target=main, args=(r1,), name=f'线程{i}号')
        tlist.append(t)
        t.start()
    for t in tlist:
        t.join()
