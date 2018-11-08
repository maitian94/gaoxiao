#coding=utf8
import requests
from lxml import etree
from utils import *

headers = {
    'Host': 'engpat.kipris.or.kr',
    'Origin': 'http://engpat.kipris.or.kr',
    'Referer': 'http://engpat.kipris.or.kr/engpat/searchLogina.do?next=MainSearch',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Cookie': 'JSESSIONID=0a856a4330db7d16c6c7bbca4cd8b30ee4d9ee79769d; WMONID=sZ5ZJaf_yhB; KP_CONFIG=G1111111111111111111111S111111111000000000; DG_CONFIG=G11111111111111111SX11100110011011110; TM_CONFIG=G11111111111111111SX11111110011111100; JM_CONFIG=G11111111111111SX01101111110010; AB_CONFIG=G11001111111111111111111111110S10000111000111100001000; AT_CONFIG=G0000000000000S111110110111; KA_CONFIG=G0000000000000S110111000; K2_CONFIG=G1111111111111111111111S111111111000000000; _ga=GA1.3.1042151666.1541645567; _gid=GA1.3.1095258877.1541645567; ENGPAT_RECENTLY_JOB=1020180103293; KPAT_SRCH_HISTORY=E5CCDFE9AD544A05BEF9E42070812313D3BAECC779D6CEC34368E2E10595322CF6AEE595789D4D04525C85BA234CED500D55456C6661DB81; _gat=1'
}


def handleApplicant(results, key, lis):
    if ''.join(lis.xpath(".//li[2]//text()")).find("more") == -1:
        results[key] = ''.join(lis.xpath(".//li[2]/a//text()")).replace("\xa0", '')
    else:
        results[key] = ''.join(lis.xpath(".//li[2]//button/@title")).replace("\xa0", '')


def handleAgent(results, key, lis):
    if ''.join(lis.xpath(".//li[9]//text()")).find("more") == -1:
        results[key] = ''.join(lis.xpath(".//li[9]/a//text()")).replace("\xa0", '')
    else:
        results[key] = ''.join(lis.xpath(".//li[9]//button/@title")).replace("\xa0", '')


def parse(url, page):
    data = {
        'queryText': 'PD=[19480101~20181108]',
        'searchInResultCk': 'undefined',
        'next': 'SimpleList',
        'config': 'G1111111111111111111111S110001000000000000',
        'sortField': 'RANK',
        'sortState': 'DESC',
        'configChange': 'Y',
        'expression': 'PD=[19480101~20181108]',
        'historyQuery': 'PD=[19480101~20181108]',
        'numPerPage': 30,
        'numPageLinks': 10,
        'currentPage': page,
        'beforeExpression': 'PD=[19480101~20181108]',
        'userInput': '19480101~20181108',
        'searchInTrans': 'N',
        'logFlag': 'Y',
        'searchSaveCnt': 0,
        'strstat': 'TOP|KW',
        'searchInTransCk': 'undefined',
        'history': 'true'
    }

    resp = requests.post(url, data=data, headers=headers)
    html = etree.HTML(resp.text)
    articles = html.xpath("//section[@class='search_section']//article")
    for article in articles:
        results = {} #这个是handle函数的第一个参数， 第二个参数是我们自己定义好了的
        results['status'] = article.xpath(".//div[1]/h1/a/span/text()")[0]
        results['Title'] = article.xpath(".//div[1]/h1/text()")[0].strip() +"".join(article.xpath(".//div[1]/h1/a/text()")).strip()
        results['Picture_url'] = 'http://engpat.kipris.or.kr'+article.xpath(".//div[2]/div/a/img/@src")[0].strip()
        lis = article.xpath(".//ul[@class='search_info_list']")[0]  #这个是第三个参数
        results['IPC'] = ''.join(lis.xpath(".//li[1]//span/@title")).replace("\xa0", '').strip()
        # results['Applicant'] = ''.join(lis.xpath(".//li[2]/a//text()")).replace("\xa0", '')
        handleApplicant(results, 'Applicant', lis)
        # 这个函数中的results就是上面字典， 然后applicant是上面函数的key，因为你一个字典要有一个key和value对吧，能懂吧？然后lis就是第61行的那句代码，我们要在这里面用xpath处理，我就把这个传到函数里面，他才能使用xpath语法，这个函数中的参数差不多就是
        results['Application No'] = ''.join(lis.xpath(".//li[3]//span[2]/a/text()")).strip()
        results['Application Date'] = ''.join(lis.xpath(".//li[4]/text()")).strip()
        results['Registration No'] = ''.join(lis.xpath(".//li[5]//span[2]/a/text()")).strip()
        results['Registration Date'] = ''.join(lis.xpath(".//li[6]/text()")).strip()
        url = lis.xpath("")
        results['Unex. Pub. No.'] = ''.join(lis.xpath(".//li[7]/text()")).replace("\xa0", '').strip()
        results['Unex. Pub. Date '] = ''.join(lis.xpath(".//li[8]/text()")).strip()
        # results['Agent'] = ''.join(lis.xpath(".//li[9]/a//text()"))
        handleAgent(results, 'Agent', lis)
        results['Inventor'] = ''.join(lis.xpath(".//li[10]/font/@title")).strip()
        print(results) # 这里你就把results存储到csv文件

def main():
    url = 'http://engpat.kipris.or.kr/engpat/resulta.do'
    for i in range(1, 31): # 这里是页数 我不知道有好多页你去看看网页上 目前是1到30页
        parse(url, i)


if __name__ == '__main__':
    main()
