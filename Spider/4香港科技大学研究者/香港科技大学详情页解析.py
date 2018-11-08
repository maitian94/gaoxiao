# coding=utf8
import requests
from bs4 import BeautifulSoup as bs
import re

def xgkjParser(url):
    result = {}
    res = requests.get(url)
    soup = bs(res.text,'html.parser')
    result['PictureUrl'] = 'http://repository.ust.hk' + soup.select('#profilePhoto')[0].attrs['src'].strip()
    result['AuthorName'] = soup.select('.authorName')[0].text.strip()
    result['PositionInfo'] = soup.select('#bd .audbResultList')[0].text.strip()
    PersonalInfo = soup.select('#bd p')[0].text.strip()
    PersonalInfo = re.sub('\s{2,200}','    ',PersonalInfo)
    PersonalInfo = re.sub(':\s{5}',': ',PersonalInfo)
    try:
        PersonalInfo = PersonalInfo.replace('Co-authorship graph','').strip().replace(':    ',': ').split('    ')
    except:
        PersonalInfo = PersonalInfo.replace(':    ',': ').split('    ')
    for i in PersonalInfo:
        lable = i.split(': ')[0]
        value = i.split(': ')[1]
        try:
            value = value.replace('https://orcid.org/','')
        except:
            value = value
        result[lable] = value
    PublicationUrl = soup.select('#profileTabnav .tabselected a')[0].get('href').strip()
    result['PublicationUrl'] = PublicationUrl
    PublicationNumber = soup.select('#bd .audbPubListBox tbody tr')[0].select('td')[0].get_text().strip()
    result['PublicationNumber'] = PublicationNumber
    AffiliatedNumber = soup.select('#bd .audbPubListBox tbody tr')[1].select('td')[0].get_text().strip()
    result['AffiliatedNumber'] = AffiliatedNumber
    res1 = requests.get(PublicationUrl + '/ResearchInterests')
    soup1 = bs(res1.text,'html.parser')
    try:
        Interesets = soup1.select('#rsarea_ul')[0].get_text().strip()
    except:
        Interesets = soup1.select('#bd .rsarea_text')[0].get_text().strip()
    result['Interesets'] = Interesets
    return [
        result.get('PictureUrl', ''),
        result.get('AuthorName', ''),
        result.get('PositionInfo', ''),
        result.get('Telephone', ''),
        result.get('Email', ''),
        result.get('Homepage', ''),
        result.get('Scopus', ''),
        result.get('Google Scholar', ''),
        result.get('ResearcherID', ''),
        result.get('ORCID iD', ''),
        result.get('PublicationUrl', ''),
        result.get('PublicationNumber', ''),
        result.get('AffiliatedNumber', ''),
        result.get('Interesets', '')
    ]



def main():
    url = 'http://repository.ust.hk/ir/AuthorProfile/cai-yong-shun'
    result = xgkjParser(url)
    # print(result)

if __name__ == '__main__':
    main()

