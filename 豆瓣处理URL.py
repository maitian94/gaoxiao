# coding=utf8
import threading
import time

import requests
from bs4 import BeautifulSoup
import redis
from utils import write2csv, getIP, csvStrProcess, writeurl2txt, txt2Redis,quchong

pool = redis.ConnectionPool(host='localhost', port=6379,
                            decode_responses=True)  # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
r1 = redis.Redis(connection_pool=pool)


def SaddListPageUrl(rds):
    # 把搜索结果页面的url塞到redis里面
    for i in open('fl.txt', encoding='utf8'):
        tag = i.strip()
        for i in range(0, 1000, 20):
            print(f'当前进度：{tag} -- {i}')
            url = f'https://book.douban.com/tag/{tag}?start={i}&type=S'
            rds.sadd('dbfl', url)


def getAllUrlUseTag(rds):
    ip = getIP()
    flag = 1
    while flag:
        url = rds.spop('dbfl')
        try:
            res = requests.get(url=url,
                           verify=False,
                           proxies={'https': ip},
                           cookies={
                               'cookies': 'bid=TX46Fh960Io; gr_user_id=9472f59e-3423-469c-a898-4d7be0efe16f; _vwo_uuid_v2=D945973C56E9DE5A89F4A407FF5B9F65B|8193048ef938ca0f9e21e82b5744da7a; __yadk_uid=IPSJiIkXJpASML3BRiVvfPmTQxziqRaY; viewed="2230208_25849649_1019210_6849293_6849290_20365152_2060130_6885810_25780889_3315384"; ct=y; ps=y; push_noty_num=0; push_doumail_num=0; dbcl2="179755333:lBCXZdA+b1Y"; __utmv=30149280.17975; ck=Ybkc; __utmc=30149280; __utmz=30149280.1539673041.4.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=81379588; __utmz=81379588.1539673041.4.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; gr_cs1_ffc94504-020a-4b55-a144-fc8e796f6f1c=user_id%3A1; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1539679774%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DsuTcGShpmJjLainnnS6EuguD_DelMI8XRcQh3k6YmQ-S9Wsyxf3kOfuoYJfimrjL%26wd%3D%26eqid%3De2bd69540001c29e000000065bc58bc9%22%5D; _pk_ses.100001.3ac3=*; __utma=30149280.322353021.1539312805.1539677732.1539679774.6; __utma=81379588.2102712258.1539312976.1539677732.1539679774.6; ap_v=0,6.0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=cf00eb62-9699-4cb3-a2cf-477014a9081e; gr_cs1_cf00eb62-9699-4cb3-a2cf-477014a9081e=user_id%3A1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_cf00eb62-9699-4cb3-a2cf-477014a9081e=true; __utmb=81379588.10.10.1539679774; _pk_id.100001.3ac3=d01456c0712c87d8.1539312977.6.1539681674.1539677742.; douban-fav-remind=1; __utmb=30149280.94.4.1539681799685'})
        except:
            ip = getIP()
            print(ip)
            rds.sadd('dbfl', url)
            continue
        if '检测到有异常请求' in res.text:
            print('检测到有异常请求')
            ip = getIP()
            print(ip)
            rds.sadd('dbfl',url)
            continue

        time.sleep(0.8)

        soup = BeautifulSoup(res.text, 'html.parser')
        a_tags = soup.select('#subject_list .nbg')
        for tag in a_tags:
            href = tag.attrs.get('href', '')
            writeurl2txt('豆瓣读书书籍URL.txt', href)
            rds.sadd('dbds', href)
        leftNums = rds.scard('dbfl')
        print('rds剩余：',leftNums)
        flag = leftNums


if __name__ == "__main__":
    pool = redis.ConnectionPool(host='localhost', port=6379,
                                decode_responses=True)
    r1 = redis.Redis(connection_pool=pool)
    # tlist = []
    # for i in range(10):
    #     t = threading.Thread(target=getAllUrlUseTag, args=(r1,), name=f'线程{i}号')
    #     tlist.append(t)
    #     t.start()
    # for t in tlist:
    #     t.join()
    # already = {line for line in open('data/豆瓣读书书籍已完成爬取的URL.txt',encoding='utf8')}
    # allurl = {line for line in open('data/豆瓣读书书籍URL.txt',encoding='utf8')}
    # waitto = {line for line in open('data/豆瓣读书待爬取的URL.txt',encoding='utf8')}
    # print(len(already))
    # print(len(allurl))
    # print(len(already.union(waitto).union(allurl)))
    # print(len(allurl|waitto))

    # quchong('data/豆瓣读书所有URL_18-10-22.txt','data/豆瓣读书所有URL_18-10-222.txt')
    for i in range(1000000,9999999):
        url = 'https://book.douban.com/subject/%d/' % i
        # print(url)
        r1.sadd('dbds',url)
    # txt2Redis('data/豆瓣读书所有URL_18-10-22.txt','dbds')
    # left = already.union(waitto).union(allurl)
    # for i in left:
    #     writeurl2txt('data/豆瓣读书所有URL_18-10-18.txt',i.strip())
