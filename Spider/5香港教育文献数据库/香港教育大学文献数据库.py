# coding=utf8
import requests
from bs4 import BeautifulSoup as bs

def parse(url):
    result = {}
    res = requests.get(url)
    soup = bs(res.text,'html.parser')
    tds = soup.select('td')
    for i in range(19,len(tds)-1,2):
        lable = soup.select('td')[i].text.strip()
        value = soup.select('td')[i+1].text.strip()
        result[lable] = value

    url = 'http://bibliography.ied.edu.hk:8080/washkEN/detail?channelid=128933&searchword=id=' + soup.select('td .detail_id_value')[0].text.strip()
    result['Persistent Link to this record'] = url

    firsttp = soup.select('#eduCate .firstType')
    secondtp = soup.select('#eduCate .secondType')
    result['Education Category'] = ''
    for dui in zip(firsttp, secondtp):
       result['Education Category'] += dui[0].select('a')[0].text + ' ' + dui[0].select('a')[1].text + '   ' + dui[1].select('a')[0].text + ' '\
                                      + dui[1].select('a')[1].text + '   '
    result['Education Category'] = result['Education Category'].strip()

    auts = soup.select('.cups a')
    result['Author'] = ''
    for aut in auts:
        result['Author'] += aut.text.strip() + '   '
    result['Author'] = result['Author'].strip()

    affs = soup.select('.detail_EAuthorAffliation_value span')
    result['Affiliation'] = ''
    for aff in affs:
        result['Affiliation'] += aff.text.strip() + '   '
    result['Affiliation'] = result['Affiliation'].strip()

    keyws = soup.select('.keywords_no li')
    result['Keywords'] = ''
    for keyw in keyws:
        result['Keywords'] += keyw.text.strip() + '   '
    result['Keywords'] = result['Keywords'].strip()

    # return result
    return [
        result.get('Title', ''),
        result.get('Author', ''),
        result.get('Affiliation', ''),
        result.get('Publication Year', ''),
        result.get('Education Category', ''),
        result.get('Keywords', ''),
        result.get('Region',''),
        result.get('Period', ''),
        result.get('Level', ''),
        result.get('Abstract', ''),
        result.get('Conference', ''),
        result.get('Language', ''),
        result.get('ISSN', ''),
        result.get('DOI', ''),
        result.get('Document Type', ''),
        result.get('Publisher', ''),
        result.get('Accession Number', ''),
        result.get('Persistent Link to this record', ''),
        result.get('Entry Date', '')
            ]

def main():
    url = 'http://bibliography.ied.edu.hk:8080/washkEN/detail?record=9&channelid=128933&searchword=%28Subject%3D%28%27R%25%27%29%29&option=ignorehfw&extension=cst&sortfield=RELEVANCE'
    result = parse(url)
    print(result)

if __name__ == '__main__':
    main()