#coding=utf8
import requests
from bs4 import BeautifulSoup as bs

headers = {
    'Cookie':'JSESSIONID=0a856a4630db606c038dfda444fea77af49a6bfcdebe; KP_CONFIG=G1111111111111111111111S111111111000000000; DG_CONFIG=G11111111111111111SX11100110011011110; TM_CONFIG=G11111111111111111SX11111110011111100; JM_CONFIG=G11111111111111SX01101111110010; AB_CONFIG=G11001111111111111111111111110S10000111000111100001000; AT_CONFIG=G0000000000000S111110110111; KA_CONFIG=G0000000000000S110111000; K2_CONFIG=G1111111111111111111111S111111111000000000; _ga=GA1.3.452802084.1541559268; _gid=GA1.3.1393773942.1541559268; KP_TOTAL_HISTRY=a; WMONID=jbYECGLRBkU; KPAT_SRCH_HISTORY=C73A4EAD576897CF794E14DD7EB707AE4B9C7C9DFDB31A5C2E2C6F0CDD4FAEE025F98A1A8AC82B858E8303C83721AFCAEB7C5ED320EDAC35; _gat=1',
    'Referer':'http://engpat.kipris.or.kr/engpat/searchLogina.do?next=MainSearch',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
data = {
    'queryText':'PD=[19480101~20181108]',
    'searchInResultCk':'undefined',
    'next':'SimpleList',
    'config':'G1111111111111111111111S110001000000000000',
    'sortField':'RANK',
    'sortState':'DESC',
    'expression':'PD=[19480101~20181108]'


}

def parse():
    url = 'http://engpat.kipris.or.kr/engpat/resulta.do'
    res = requests.post(url, headers=headers, data=data)
    soup = bs(res.text,'html.parser')
    articles = soup.select('article')
    for article in articles:
        status = article.select('#iconStatus')[0].text.strip()
        title = article.select('.stitle a')[1].text.strip()
        pic_url = 'http://engpat.kipris.or.kr' + article.select('.thumb img')[0].attrs['src']
        for i in range(len(article.select('.search_info_list li'))):
            # print(li)
            ipcs = []
            for i in range(len(article.select('.search_info_list li')[0].select('.point01'))):
                ipc = article.select('.search_info_list li')[0].select('.point01')[i].text.strip()
                ipcs.append(ipc)
            ipcs = ';'.join(ipcs)






if __name__ == '__main__':
    parse()