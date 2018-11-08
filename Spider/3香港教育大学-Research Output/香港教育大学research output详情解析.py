# coding=utf8
import requests
from bs4 import BeautifulSoup as bs


def xgjyParser(url):
    result = {}
    res = requests.get(url)
    soup = bs(res.text,'html.parser')
    Title = soup.select('#page-content .row h1')[0].text.strip()
    result['Title'] = Title
    Author = soup.select('#page-content .row p')[0].text.strip()
    result['Author'] = Author
    try:
        Department = soup.select('#page-content .row li')[0].text.strip()
    except:
        Department = ''
    result['Department'] = Department
    try:
        Abstract = soup.select('#page-content .container .textblock')[0].text.strip()
    except:
        Abstract = ''
    result['Abstract'] = Abstract
    # TextInfo = soup.select('#page-content .article tbody tr')
    TextInfo = soup.select('#page-content .clearfix tr')
    for tr in TextInfo:
        lable = tr.select('th')[0].text.strip()
        value = tr.select('td')[0].text.strip()
        result[lable] = value
    # Citation = re.findall('Citation</h3>(.*?)</div>',res.text)[0].strip()
    try:
        Citation = soup.select('#page-content .container .rendering_researchoutput_publicationbibliographicalnoteportalrenderer')[0].text.strip().replace('Citation','')
    except:
        Citation = ''
    result['Citation'] = Citation
    Keywords = soup.select('#page-content .keyword-group .userdefined-keyword')
    key = ''
    for keyword in Keywords:
        key = key + keyword.get_text().strip() + '   '
    result['Keywords'] = key.strip()
    # return result
    return [
        result.get('Title', ''),
        result.get('Author', ''),
        result.get('Department', ''),
        result.get('Abstract', ''),
        result.get('Language', ''),
        result.get('Title of host publication', ''),
        result.get('Publisher', ''),
        result.get('Pages', ''),
        result.get('Journal', ''),
        result.get('Volume', ''),
        result.get('Issue number', ''),
        result.get('ISBN (Electronic)', ''),
        result.get('State', ''),
        result.get('Citation', ''),
        result.get('Keywords', ''),
    ]



    # print(TextInfo)



def main():
    url = 'https://repository.eduhk.hk/en/publications/differences-in-the-toxicities-of-an-oil-dispersant-and-a-surface-'
    result = xgjyParser(url)
    print(result)

if __name__ == '__main__':
    main()