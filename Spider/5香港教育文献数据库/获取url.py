# conding=utf8
import requests
from bs4 import BeautifulSoup as bs
from utils import write2csv

def get_url():
    for i in range(1,147):
        next_url = 'http://bibliography.ied.edu.hk:8080/washkEN/outline?page='+str(i)+'&channelid=128933&searchword=%28Subject%3D%28%27M%25%27%29%29&option=ignorehfw&sortfield=-YearofPublication&prepage=20&keyword=Education%20Category=M&templet=searchResult.jsp&firstkeyword=Education%20Category=M'
        res = requests.get(next_url)
        soup = bs(res.text,'html.parser')
        trs = soup.select('#jg tr .contentbody')
        for tr in trs:
            urls = 'http://bibliography.ied.edu.hk:8080/washkEN/' + tr.select('.content_right a')[0].attrs['href'].strip()
            print(urls)
    return urls


def main():
    urls = get_url()
    write2csv('香港教育文献url/香港教育url.txt',urls)

if __name__ == '__main__':
    main()