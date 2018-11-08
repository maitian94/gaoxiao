# coding=utf8
import requests
from bs4 import  BeautifulSoup as bs
# from utils import write2csv
# import time
def get_url(url):
    # t1 = time.time()
    res = requests.get(url)
    # t2 = time.time()
    # print(t2-t1)
    soup = bs(res.text,'html.parser')
    # for i in range(50):
    #     onepage_urls = soup.select('.list-result-item .title a')[i].attrs['href']
    next_url = 'https://repository.eduhk.hk' + soup.select('.portal-search-results .pages a')[-1].attrs['href']
    print(next_url)


def main():
    url = 'https://repository.eduhk.hk/en/publications/'
    get_url(url)

if __name__ == '__main__':
    main()