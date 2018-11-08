# coding=utf8
import requests
from bs4 import BeautifulSoup as bs
from utils import write2csv,writeurl2txt


def next_url():
    hrefs =[]
    nexturls = ['http://libdr1.ied.edu.hk/dspace/browse-title']
    try:
        while nexturls is not []:
            res = requests.get(nexturls.pop())
            soup = bs(res.text, 'html.parser')
            trs = soup.select('.miscTable tr a')
            for i in range(len(trs) - 1):
                href = 'http://libdr1.ied.edu.hk' + trs[i].attrs['href'].strip()
                hrefs.append(href)
                print(href)
            try:
                nexturl = 'http://libdr1.ied.edu.hk/dspace/' + soup.select('#next_page a')[0].attrs['href'].strip()
                nexturls.append(nexturl)
            except:
                break
        return hrefs
    except:
        next_url()


def parser(href):
    result = {}
    try:
        res = requests.get(href)
        result['Url'] = href
        soup = bs(res.text,'html.parser')
        labels = soup.select('.metadataFieldLabel')
        values = soup.select('.metadataFieldValue')
        for i in range(len(labels)):
            label = labels[i].text.strip()
            value = values[i].text.strip()
            result[label] = value
        return [
            result.get('Title[書名]:', ''),
            result.get('Other Titles[其他書名]:', ''),
            result.get('Authors[作者] :', ''),
            result.get('Publication/Copyright Date[出版/版權日期]:', ''),
            result.get('Call Number[索書號]:', ''),
            result.get('Format[媒體資料]:', ''),
            result.get('Category[分類]', ''),
            result.get('Url','')
        ]
    except:
        parser(href)


def main():
    hrefs = next_url()
    for href in hrefs:
        result = parser(href)
        print(result)
        write2csv('csvFiles/香港教育特藏.csv', result)
        writeurl2txt('csvFiles/香港教育特藏.txt',href)

if __name__ == '__main__':
    main()