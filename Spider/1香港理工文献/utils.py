# coding=utf8
import threading
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
        csvStr=csvStr.lstrip('\ufeff')
        # csvStr = csvStr.replace('\xa0','')
        csvStr = '"' + csvStr.replace('"', '""') + '"'
        csvStr = csvStr.replace('\r', '')
        csvStr = csvStr.replace('\n', '\\n')
        return csvStr
    return csvStr


def write2csv(filename: str, row: list):
    # 一行一行地写入csv
    fileLock = threading.Lock()
    fileLock.acquire()
    row = map(csvStrProcess, row)
    row = list(row)
    # print(list(row))
    csvfile = open(f'{filename}', 'a', newline='', encoding='utf8')
    print(','.join(row))
    csvfile.write(','.join(row))
    # csvfile.write(row)
    csvfile.write('\n')
    csvfile.close()
    fileLock.release()


def xgdxPaser(html):
    # 香港大学学术库详情页解析
    result = {}
    # res = requests.get('http://hub.hku.hk/handle/10722/258862')
    # soup = BeautifulSoup(res.text, 'html.parser')
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select('#full_view tr')
    for row in rows:
        tds = row.select('td')
        if not tds:
            continue
        result[tds[0].text] = tds[1].text
    print(result)
    col_list = ['dc.contributor.author',
                'dc.date.accessioned',
                'dc.date.available',
                'dc.date.issued',
                'dc.identifier.citation',
                'dc.identifier.uri',
                'dc.description.abstract',
                'dc.language',
                'dc.publisher',
                'dc.relation.ispartof',
                'dc.rights',
                'dc.subject.lcsh',
                'dc.title',
                'dc.type',
                'dc.description.thesisname',
                'dc.description.thesislevel',
                'dc.description.thesisdiscipline',
                'dc.description.nature',
                'dc.date.hkucongregation',
                'dc.identifier.mmsid']
    result_list = [result.get(col,'') for col in col_list]
    print(result_list)
    return result_list


def gjzrParser(html):
    # 国家自然基金
    result = {}
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        # 'Content-Type':'text/html;charset=UTF-8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
               'Content-Language':'zh-CN,zh;q=0.9'}
    res = requests.get('http://or.nsfc.gov.cn/handle/00001903-5/435612',headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser').select('#item-right')[0]
    result['main-title'] = soup.select('.main-title')[0].text.strip()
    result['alter-title'] = soup.select('.alter-title')[0].text.strip()
    for row in soup.find_all('div', class_=['row']):
        k = row.select('.col-1')[0].text.strip()
        v = row.select('.col-2')[0].text.strip()
        result[k]=v
    result['Author'] = result['Author'].replace('\xa0\xa0\r\n        \t\t\t\t\r\n        \t\t\t\t\t','')
    print(result)
def dbdsParser(url, html):
    result = {}
    # res = requests.get('https://book.douban.com/subject/26853356/')
    # soup = BeautifulSoup(res.text, 'html.parser')
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    try:
        title = soup.select('#wrapper h1 span')[0].text.strip()
    except:
        print('拿标题出错')
        print(url)
        return None
    result['标题'] = title
    try:
        indent = soup.select('.indent')[0]
    except:
        return None
    try:
        img = indent.select('.nbg')[0].attrs['href']
    except:
        img = ''
    result['封面图'] = img

    info = soup.select('#info')[0].text.replace('\xa0\n        \n            ', '').strip().replace('\n\n', '\n')
    info = info.replace('\n            ', '').replace('\n        \n        \n        ', '')
    info = info.split('\n')
    # print(repr(info))
    for item in info:
        kv = item.split(':')
        try:
            result[kv[0]] = kv[1].strip().lstrip('\xa0').lstrip('    ')
        except:
            print('出错啦: ', url)
            return None
    # print(repr(info))
    rating = soup.select('#interest_sectl .rating_num')[0].text.strip()
    result['评分'] = rating
    indent = soup.select('.related_info .indent')
    try:
        book_intro = indent[0].select('.all .intro')[0].text.strip()
    except:
        try:
            book_intro = indent[0].select('.intro')[0].text.strip()
        except:
            book_intro = ''
    try:
        author_intro = indent[1].select('.all .intro')[0].text.strip()
    except:
        try:
            author_intro = indent[1].select('.intro')[0].text.strip()
        except:
            author_intro = ''
        print('出错啦2: ', url)
        author_intro = ''
    result['内容简介'] = book_intro
    result['个人简介'] = author_intro
    # print(result)
    dj = result.get('定价', '')
    yuan = ''
    jg = 0
    if len(dj) != 6:
        return None
    if dj:
        if '元' in dj:
            yuan = '元'
            jg = dj.replace('元', '')
        else:
            return None
    ys = result.get('页数', '')

    # if ys:
    #     ys = int(ys)
    # print(result)
    isbn = result.get('ISBN', '')
    # if isbn:
    #     isbn = int(isbn)
    print([result.get('标题', ''),
           result.get('封面图', ''),
           result.get('作者', ''),
           result.get('出版社', ''),
           result.get('出版年', ''),
           ys,
           jg,
           yuan,
           result.get('装帧', ''),
           isbn,
           result.get('评分', ''),
           result.get('内容简介', ''),
           result.get('个人简介', '')
           ])
    return [csvStrProcess(result.get('标题', '')),
            csvStrProcess(result.get('封面图', '')),
            csvStrProcess(result.get('作者', '')),
            csvStrProcess(result.get('出版社', '')),
            csvStrProcess(result.get('出版年', '')),
            ys,
            jg,
            csvStrProcess(yuan),
            csvStrProcess(result.get('装帧', '')),
            isbn,
            result.get('评分', ''),
            csvStrProcess(result.get('内容简介', '')),
            csvStrProcess(result.get('个人简介', '')),
            ]


if __name__ == "__main__":
    pass
    # gjzrParser('')
    gjzrkxCol = ['main-title','alter-title','Author','Publisher',
                 'Date Issued','Program','Project ID','Sponsorship',
                 'Institution','Recommend','']
    xglg = ['Title','Authors','Keywords','Issue Date','Publisher','Source','Journal','Abstract','URI','ISSN',
            'EISSN','ISBN','DOI','Rights','Appears in Collections']
    # col_list = ['dc.contributor.author',
    #             'dc.date.accessioned',
    #             'dc.date.available',
    #             'dc.date.issued',
    #             'dc.identifier.citation',
    #             'dc.identifier.uri',
    #             'dc.description.abstract',
    #             'dc.language',
    #             'dc.publisher',
    #             'dc.relation.ispartof',
    #             'dc.rights',
    #             'dc.subject.lcsh',
    #             'dc.title',
    #             'dc.type',
    #             'dc.description.thesisname',
    #             'dc.description.thesislevel',
    #             'dc.description.thesisdiscipline',
    #             'dc.description.nature',
    #             'dc.date.hkucongregation',
    #             'dc.identifier.mmsid']
    write2csv('csvFiles/香港理工大学文献.csv', xglg)
