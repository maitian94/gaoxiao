# coding=utf8
import requests
from bs4 import BeautifulSoup as bs
import re
from utils import write2csv


def xglgparser(url):
    result = {}
    try:
        res = requests.get(url)
        soup = bs(res.text, 'html.parser')
        div = soup.find_all('div', {'class': 'panel panel-default'})
        soup2 = bs(str(div), 'html.parser')
        tds_ = soup2.select('td')
        number = len(tds_)
        tds = soup.select('td')
        for i in range(0, len(tds) - number, 2):
            result[tds[i].text.strip()] = tds[i + 1].text.strip()
        if 'Source:' in result.keys():
            try:
                result['Source:'] = re.findall('(.*?)How to cite?', result['Source:'])
                result['Source:'] = result['Source:'][0].strip()
                print(result['Source:'])
            except Exception as e:
                print(e)
                result['Source:'] = ''
        return [result.get('Title:', ''),
                result.get('Authors:', ''),
                result.get('Keywords:', ''),
                result.get('Issue Date:', ''),
                result.get('Publisher:', ''),
                result.get('Source:', ''),
                result.get('Journal:',''),
                result.get('Abstract:', ''),
                result.get('URI:', ''),
                result.get('ISSN:', ''),
                result.get('EISSN:', ''),
                result.get('ISBN:', ''),
                result.get('DOI:', ''),
                result.get('Rights:', ''),
                result.get('Appears in Collections:', '')]
    except:
        return ['','','','','','','','','','','','','','','']


def get_href():
    urls = []
    for i in range(5500,6978):
        next_url = 'http://ira.lib.polyu.edu.hk/simple-search?query=&location=dspaceitem&sort_by=score&order=desc&rpp=10&etal=0&start=' + str(
            i * 10)
        print('正在解析第%s页' % str(i+1))
        print(next_url)
        try:
            response = requests.get(next_url)
            html = response.text
            soup = bs(html, 'html.parser')
            table = soup.find_all('table', {'align': 'center'})
            soup1 = bs(str(table), 'html.parser')
            for j in range(1, 11):
                href = soup1.select('tr')[j]('a')[0]['href']
                href = 'http://ira.lib.polyu.edu.hk' + href
                urls.append(href)
        except:
            continue
    return urls



def main():
    urls = get_href()
    for url in urls:
        result = xglgparser(url)
        write2csv('csvFiles/香港理工大学文献.csv', result)


if __name__ == '__main__':
    main()
