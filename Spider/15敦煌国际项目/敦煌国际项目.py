#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
import re
from pprint import pprint
from utils import write2csv,writeurl2txt

def parser():
    result = {}
    for z in range(28,30):
        next_url = 'http://idp.nlc.cn/database/search_results.a4d?uid=-9761261559;bst=' + str(1+z*50)
        res = requests.get(next_url)
        soup = bs(res.text,'html.parser')
        trs = soup.select('#results tr')
        print('正在处理第*******' + str(z) + '*********页')
        for tr in trs:
            picture_detail_url = 'http://idp.nlc.cn/database/' + tr.select('.thumb a')[0].attrs['href'].strip()
            result['图片详情页链接'] = picture_detail_url
            picture_url = 'http://idp.nlc.cn' + tr.select('img')[0].attrs['src'].strip()
            result['图片链接'] = picture_url
            detail_url = 'http://idp.nlc.cn/database/' + tr.select('.resultdetails a')[0].attrs['href'].strip()
            result['详情页链接'] = detail_url
            # institution = tr.select('.resultdetails a')[0].text.strip()
            year = tr.select('.resultdetails a')[1].text.strip()
            result['未知信息'] = year
            details = tr.select('.resultdetails')[0].text.strip().replace('\n',' ').replace('\t','')
            # yizhi = re.findall('.*?遺址:(.*?)語言/.*?',details)[0].strip()
            language = re.findall('.*?語言/文字: (.*?) 材料:.*?',details)[0].strip()
            result['语言'] = language
            # material = re.sub('.*?材料:','',details).strip()
            try:
                res1 = requests.get(picture_detail_url,timeout=75)
            except:
                failed_urls = []
                failed_urls.append(picture_detail_url)
                writeurl2txt('failedurl.txt',picture_detail_url)
                continue
            soup1 = bs(res1.text,'html.parser')
            duis = soup1.select('#iteminfotable tr')
            print(1111111111)
            for dui in duis:
                label = dui.select('td')[0].text.strip()
                value = dui.select('td')[1].text.strip()
                result[label] = value
                print(222222222)
            print(result)
            write2csv('敦煌国际项目.csv',[
                result.get('图片详情页链接', ''),
                result.get('图片链接', ''),
                result.get('详情页链接', ''),
                result.get('未知信息', ''),
                result.get('语言', ''),
                result.get('收藏機構及版權:', ''),
                result.get('遺址:', ''),
                result.get('藏品形態:', ''),
                result.get('材料:', ''),
                result.get('尺寸 (h x w) 釐米:', '')
                ])

if __name__ == '__main__':
    parser()
    # print(result)