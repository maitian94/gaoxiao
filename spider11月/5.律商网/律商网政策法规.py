#coding=utf8
import requests
from lxml import etree
from bs4 import BeautifulSoup as bs
from utils import *
from pprint import pprint
import re



def parse():
    for i in range(5682,8000):
        url = 'https://hk.lexiscn.com/search/index?keyword=%E6%B3%95%E8%A7%84&page='+str(i)+'&ctStat%5Ball%5D=0&ctStat%5Blaw%5D=422078&ctStat%5Bcase%5D=345121&ctStat%5Bep_news%5D=6823&ctStat%5Bcontract%5D=0&ctStat%5Bexpert%5D=4620&ctStat%5Bforeignlaw%5D=55&ctStat%5Bnewsletter%5D=377&ctStat%5Bbook%5D=1006&content_type=law&displayMode=&sort=relevance'
        print('正在处理第{0}页正在处理第{0}页正在处理第{0}页正在处理第{0}页'.format(i))
        res = requests.get(url)
        html = etree.HTML(res.text)
        lis = html.xpath("//ul[@class='list']/li")
        for li in lis:
            url = li.xpath(".//a/@href")[0].strip()
            print(url)
            writeurl2txt('data/律商网法律法规_Url.txt', url)
            try:
                title = li.xpath(".//a/text()")[0].strip() + '法规' + li.xpath(".//a/text()")[1].strip()
            except:
                title = li.xpath(".//a/text()")[0].strip()
            try:
                date = li.xpath(".//span/text()")[0].replace('[', '').replace(']', '').replace('政策法规','').strip()
            except:
                writeurl2txt('data/failed_url.txt', url)
                continue
            res1 = requests.get(url)
            html1 = res1.content.decode('utf-8')
            soup1 = bs(html1, 'html.parser')
            text = soup1.select('.content-container br')[:3]
            text = ''.join([i.text for i in soup1.select('.content-container br')[:3]])
            #处理时间
            riqi = re.findall('(\d+)-(\d+)-(\d+)',date)
            yuefen = int(riqi[0][1])
            jiri = int(riqi[0][2])
            if yuefen < 10 and jiri < 10:
                riqi = riqi[0][0] + '年' + riqi[0][1].replace('0','') + '月'+ riqi[0][2].replace('0','') + '日'
            elif yuefen < 10 and jiri > 10:
                riqi = riqi[0][0] + '年' + riqi[0][1].replace('0','') + '月'+ riqi[0][2] + '日'
            elif yuefen > 10 and jiri > 10:
                riqi = riqi[0][0] + '年' + riqi[0][1] + '月' + riqi[0][2] + '日'
            else:
                riqi = riqi[0][0] + '年' + riqi[0][1] + '月' + riqi[0][2].replace('0','') + '日'
            try:
                fagui = text.split(riqi)[0].replace('\r\n','').split(title)[1].replace('\n','').replace('（','').replace('\u3000','').strip()
            except:
                fagui = text.split(riqi)[0].replace('\r\n','').split(title)[0].replace('\n','').replace('（','').replace('\u3000','').strip()
            fagui_num = len(fagui)
            if fagui_num >50:
                fagui = fagui.split('）',1)[0].replace('（','').replace('（','').replace('\u3000','')
            fagui_len = len(fagui)
            if fagui_len > 25:
                continue
            result = [url, title, date, fagui]
            print(result)
            write2csv('data/律商网法律法规.csv',result)





if __name__ == '__main__':
    # write2csv('data/律商网法律法规.csv',['页面链接', '标题', '日期', '法令号'])
    parse()

