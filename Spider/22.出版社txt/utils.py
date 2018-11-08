# coding=utf8
import threading

import redis
import requests
from bs4 import BeautifulSoup
import re
import time
import sys


def getIP():
    global ip
    ip = requests.get(
        'http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=7&fa=2&fetch_key=&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson='
    ).text
    time.sleep(1.5)
    if '有效IP数量不够' in ip:
        sys.exit('有效IP数量不够')
    return ip


def csvStrProcess(csvStr):
    if isinstance(csvStr, str):
        csvStr = csvStr.lstrip('\ufeff')
        csvStr = csvStr.replace('\xa0','')
        csvStr = '"' + csvStr.replace('"', '""') + '"'
        csvStr = csvStr.replace('\r', '')
        csvStr = csvStr.replace('\n', '\\n')
        return csvStr
    return csvStr


FileLock = threading.Lock()


def write2csv(filename: str, row: list):
    # 一行一行地写入csv
    row = map(csvStrProcess, row)
    row = list(row)
    row = map(str, row)
    row = list(row)
    # print(list(row))
    FileLock.acquire()
    csvfile = open(f'{filename}', 'a', newline='', encoding='utf8')
    # print(','.join(row))
    csvfile.write(','.join(row))
    # csvfile.write(row)
    csvfile.write('\n')
    csvfile.close()
    FileLock.release()



TxtLock = threading.Lock()
def writeurl2txt(filename: str, url: str):
    TxtLock.acquire()
    csvfile = open(f'{filename}', 'a', encoding='utf8')
    csvfile.write(f'{url}\n')
    csvfile.close()
    TxtLock.release()


FailedLock = threading.Lock()
def writeFailed(filename: str, url: str):
    FailedLock.acquire()
    csvfile = open(f'data/failed/{filename}', 'a', encoding='utf8')
    csvfile.write(f'{url}\n')
    csvfile.close()
    FailedLock.release()


pool = redis.ConnectionPool(host='localhost', port=6379,
                            decode_responses=True)  # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
r1 = redis.Redis(connection_pool=pool)
def txt2Redis(filename: str, rdskey: str):
    with open(filename) as f:
        cnt=0
        for i in f:
            r1.sadd(rdskey,i.rstrip('\n'))
            cnt+=1
            print(cnt)





if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
        'Accept-Language': 'zh-CN'}
    # res = requests.get('http://or.nsfc.gov.cn//handle/00001903-5/351108', headers=headers)
    #
    # print(gjzrParser('http://or.nsfc.gov.cn/handle/00001903-5/382267',res.text))

    txt2Redis('data/urls/zrkxurl.txt','zrkx')

    gjzrkxCol = ['主标题', '副标题', '作者', '期刊名称',
                 '发表日期', '资助类型', '项目编号', '项目名称',
                 '研究机构', '所属学科', '全文下载', '下载次数', 'URL']
    col_list = ['dc.contributor.author',
                'dc.contributor.author',
                'dc.date.issued',
                'dc.identifier.citation',
                'dc.identifier.uri',
                'dc.language',
                'dc.publisher',
                'dc.relation.ispartof',
                'dc.rights',
                'dc.source.uri',
                'dc.subject.lcsh', 'dc.subject.lcsh',
                'dc.title',
                'dc.type',
                'dc.identifier.hkul',
                'dc.description.thesisname',
                'dc.description.thesislevel',
                'dc.description.thesisdiscipline',
                'dc.description.nature',
                'dc.identifier.doi',
                'dc.date.hkucongregation',
                ]
    # print(len(col_list))
    # write2csv('csvFiles/自然科学.csv', gjzrkxCol)
    pass