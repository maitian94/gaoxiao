import requests
from bs4 import BeautifulSoup as bs
import re



def xglgparser(url):
    result = {}
    try:
        res = requests.get(url)
        soup = bs(res.text, 'html.parser')
        print(res.text)
        div = soup.find_all('div', {'class': 'panel panel-default'})
        soup1 = bs(str(div), 'html.parser')
        tds_ = soup1.select('td')
        number = len(tds_)
        tds = soup.select('td')
        for i in range(0, len(tds) - number, 2):
            result[tds[i].text.strip()] = tds[i + 1].text.strip()
        if 'Source:' in result.keys():
            try:
                result['Source:'] = re.findall('(.*?)How to cite?',result['Source:'])
                result['Source:'] = result['Source:'][0].strip()
                print(result['Source:'])
            except Exception as e:
                print(e)
                result['Source:'] = ''
        return [
            result.get('Title:', ''),
            result.get('Authors:', ''),
            result.get('Keywords:', ''),
            result.get('Issue Date:', ''),
            result.get('Publisher:', ''),
            result.get('Source:', ''),
            result.get('Journal:', ''),
            result.get('Abstract:', ''),
            result.get('URI:', ''),
            result.get('ISSN:', ''),
            result.get('EISSN:', ''),
            result.get('ISBN:', ''),
            result.get('DOI:', ''),
            result.get('Rights:', ''),
            result.get('Appears in Collections:', '')
        ]
    except TimeoutError:
        xglgparser(url)



def main():
    url = 'http://ira.lib.polyu.edu.hk/handle/10397/50211'
    xglgparser(url)

if __name__ == '__main__':
    main()
