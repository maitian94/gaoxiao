#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
import re

def parser():
    result = {}
    res = requests.get('http://readopac2.ncl.edu.tw/nclJournal/search/detail.jsp?sysId=0006965049&dtdId=000040&search_type=detail&la=ch&checked=&unchecked=0010006966762,0020006966790,0030006966421,0040006964553,0050006964571,0060006964573,0070006964577,0080006964578,0090006964581,0100006964582,0110006964583,0120006964587,0130006964589,0140006964529,0150006964972,0160006964981,0170006964982,0180006965048,0190006965049,0200006965050,')
    soup = bs(res.text,'html.parser')
    title = soup.select('.caption')[0].text.strip()
    result['标题'] = title
    author = soup.select('.publishInfo li a')[0].text.strip()
    source = soup.select('.publishInfo li a')[2].text.strip()
    result['作者'] = author
    result['来源'] = source
    quanqi = soup.select('.publishInfo li')[-2].text.strip()
    result['卷期'] = quanqi
    page = soup.select('.publishInfo li')[-1].text.strip()
    result['页码'] = page
    duis = soup.select('tr')[:-2]


    for dui in duis:
        label = dui.select('th')[0].text.strip()
        value = dui.select('td')[0].text.strip().replace('\r\n','').replace('\n','').replace('         ','')
        result[label] = value
    language = re.sub('(.*?)語文','',result['語文'])
    result['语言'] = language
    # return result
    return [
        result.get('标题', ''),
        result.get('作者', ''),
        result.get('来源', ''),
        result.get('卷期', ''),
        result.get('页码', ''),
        result.get('语言', ''),
        result.get('關鍵詞', ''),
        result.get('分類號', ''),
        result.get('本刊其他篇目查詢',''),
        result.get('專輯', ''),
        result.get('系統識別號','')
        ]





def main():
    result = parser()
    print(result)

if __name__ == '__main__':
    main()
