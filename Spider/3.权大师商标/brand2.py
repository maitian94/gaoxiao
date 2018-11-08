import requests
from requests.exceptions import RequestException
import pandas as pd
from random import randint
import time


def get_one_page(url, current_page):
    proxies_list = [{
        'https': 'https://' + '191.234.163.231:3128'
    }, {
        'https': 'https://' + '191.232.238.230:3128'
    }, {
        'https': 'https://' + '191.234.166.71:3128'
    }, {
        'https': 'https://' + '94.242.58.108:10010'
    }, {
        'https': 'https://' + '195.189.60.23:3128'
    }, {
        'https': 'https://' + '89.40.12.150:3128'
    }, {
        'https': 'https://' + '189.55.193.154:3128'
    }
]
    cookies_list = [
        'NTKF_T2D_CLIENTID=guestFB899DE9-1810-5B77-695C-8A47E5CE138F; nTalk_CACHE_DATA={uid:kf_9479_ISME9754_guestFB899DE9-1810-5B,tid:1535683171607023}; Hm_lvt_df2da21ec003ed3f44bbde6cbef22d1c=1535623289,1535683136,1535683175; _csrf=37508335ba6f12a5fc2660631605e75e39e9b993b10ce51934a0666886dc20e4s%3A32%3A%22KRjbGZYuXVBEpncUKXTaj2UOWTqWdO3J%22%3B; PHPSESSID=t3kgitff0hnoss6o921g7s9en3; QDS_COOKIE=7e9906d33cd8887ac83dfa19ede48a1e7dcee0ba; Hm_lpvt_df2da21ec003ed3f44bbde6cbef22d1c=1535683259',
        'NTKF_T2D_CLIENTID=guestFB899DE9-1810-5B77-695C-8A47E5CE138F; nTalk_CACHE_DATA={uid:kf_9479_ISME9754_guestFB899DE9-1810-5B,tid:1535683171607023}; Hm_lvt_df2da21ec003ed3f44bbde6cbef22d1c=1535623289,1535683136,1535683175; _csrf=37508335ba6f12a5fc2660631605e75e39e9b993b10ce51934a0666886dc20e4s%3A32%3A%22KRjbGZYuXVBEpncUKXTaj2UOWTqWdO3J%22%3B; PHPSESSID=t3kgitff0hnoss6o921g7s9en3; QDS_COOKIE=64595141070a20a9b2d6633c1094f3fa8b0210b5; Hm_lpvt_df2da21ec003ed3f44bbde6cbef22d1c=1535683332',
        'NTKF_T2D_CLIENTID=guestFB899DE9-1810-5B77-695C-8A47E5CE138F; nTalk_CACHE_DATA={uid:kf_9479_ISME9754_guestFB899DE9-1810-5B,tid:1535683171607023}; Hm_lvt_df2da21ec003ed3f44bbde6cbef22d1c=1535623289,1535683136,1535683175; _csrf=37508335ba6f12a5fc2660631605e75e39e9b993b10ce51934a0666886dc20e4s%3A32%3A%22KRjbGZYuXVBEpncUKXTaj2UOWTqWdO3J%22%3B; PHPSESSID=t3kgitff0hnoss6o921g7s9en3; QDS_COOKIE=0df991108092fa32b3a3be2a22d64953e33a3077; Hm_lpvt_df2da21ec003ed3f44bbde6cbef22d1c=1535683437',
        'NTKF_T2D_CLIENTID=guestFB899DE9-1810-5B77-695C-8A47E5CE138F; nTalk_CACHE_DATA={uid:kf_9479_ISME9754_guestFB899DE9-1810-5B,tid:1535683171607023}; Hm_lvt_df2da21ec003ed3f44bbde6cbef22d1c=1535623289,1535683136,1535683175; _csrf=37508335ba6f12a5fc2660631605e75e39e9b993b10ce51934a0666886dc20e4s%3A32%3A%22KRjbGZYuXVBEpncUKXTaj2UOWTqWdO3J%22%3B; PHPSESSID=t3kgitff0hnoss6o921g7s9en3; QDS_COOKIE=ccfffad2f11a0797a54c83203973b1534be824b3; Hm_lpvt_df2da21ec003ed3f44bbde6cbef22d1c=1535683513'
    ]

    proxies = proxies_list[randint(0, len(proxies_list) - 1)]
    cookies = cookies_list[randint(0, len(cookies_list) - 1)]
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
        + 'Chrome/68.0.3440.106 Safari/537.36',
        'Referer':
        'https://so.quandashi.com/index/search?key=%E8%BF%90%E8%BE%93%E5%B7%A5%E5%85%B7&param=4',
        'host':
        'so.quandashi.com',
        'Cookie':
        cookies
    }
    data = {
        'key': '办公用品',
        'param': '4',
        'page': current_page,
        'pageSize': '20',
        'host': 'so.quandashi.com',
    }
    try:
        import time
        time.sleep(0.005)
        response = requests.post(url, data=data, headers=headers, proxies=proxies, timeout=3)
        if response.status_code == 200:
            return response.json()
        return None
    except RequestException:
        print('请求网址出现问题')
        return None

def tocsv(result, cols, path):
    df = pd.DataFrame(result)
    df = df.loc[:, cols]
    df.to_csv(path)

def main():
    #from bs4 import BeautifulSoup as bs
    result = {'name':[], 'typeCode':[], 'dataId':[], 'applicant':[], 'createDate':[], 'adress':[], 'logoUrl':[],
    'graphName':[], 'serviceName':[], 'noticeIssue':[], 'noticeDate':[], 'registerIssue':[], 'registerDate':[],
    'privateStartDate':[], 'privateEndDate':[] ,'agency':[], 'processName':[]}
    url = 'https://so.quandashi.com/search/search/search-list'
    html_list = []
    for i in range(800,2000):
        print('正在爬取第%d页'%i)
        html = get_one_page(url, i)
        html_list.append(html)
        try:
            items = html['data']['data']['items']
            #print('###### {}'.format(items))
        except:
            print()
            continue
        for item in items:
            #标题
            result['name'].append(item['name'])
            #类别
            result['typeCode'].append(item['typeCode'])
            #申请号
            result['dataId'].append(item['dataId'])
            #申请人名称
            result['applicant'].append(item['applicant'])
            #申请日期
            result['createDate'].append(item['createDate'])
            #申请人地址
            result['adress'].append(item['adress'])
            #商标图片
            result['logoUrl'].append(item['logoUrl'])
            #图片要素
            result['graphName'].append(item['graphName'])
            #服务项目
            result['serviceName'].append(item['serviceName'])
            #初审公告期号
            result['noticeIssue'].append(item['noticeIssue'])
            #初审公告日期
            result['noticeDate'].append(item['noticeDate'])
            #注册公告期号
            result['registerIssue'].append(item['registerIssue'])
            #注册公告日期
            result['registerDate'].append(item['registerDate'])
            #专利权起始时间
            result['privateStartDate'].append(item['privateStartDate'])
            #专利权结束时间
            result['privateEndDate'].append(item['privateEndDate'])
            # 是否共有商标

            # 代理人名称
            result['agency'].append(item['agency'])
            # 优先权日期

            # 国际注册日期
            # 后期制定日期
            # 商标状态
            result['processName'].append(item['processName'])
    print('运行结束')
    # 商标公告

    # URL
    loc = ['name', 'typeCode', 'dataId', 'applicant', 'createDate', 'adress', 'logoUrl',
    'graphName', 'serviceName', 'noticeIssue', 'noticeDate', 'registerIssue', 'registerDate',
    'privateStartDate', 'privateEndDate','agency', 'processName']
    tocsv(result, loc, './brangtest16.csv')


if __name__ == '__main__':
    main()
