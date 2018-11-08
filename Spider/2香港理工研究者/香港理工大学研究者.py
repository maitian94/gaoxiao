import requests
from bs4 import BeautifulSoup as bs


def xglgwenxian(url):
    result = {}
    res = requests.get(url)
    soup = bs(res.text,'html.parser')
    authoridentifcation = soup.select('#collapseOneauthoridentification .dynaField')
    for dynafield in authoridentifcation:
        lable = dynafield.select('.dynaLabel')[0].get_text().strip()
        value = dynafield.select('a')[0].get_text().strip()
        result[lable] = value
    profile = soup.select('#collapseOnedescription .dynaField')
    for dynafield in profile:
        lable = dynafield.select('div')[0].get('id').strip()
        try:
            value = 'http://ira.lib.polyu.edu.hk' + dynafield.select('img')[0].get('src').strip()
        except:
            value = dynafield.select('.dynaFieldValue')[0].get_text().strip()
        result[lable] = value
    socialcontact = soup.select('#collapseOnecontact .dynaField')
    for dynafield in socialcontact:
        lable = dynafield.select('div')[0].get('id').strip()
        try:
            value = dynafield.select('a')[0].get('href').strip()
            value = value.replace('mailto:','')
            value = value.replace('(Prof)','')
        except:
            value = dynafield.select('.dynaFieldValue')[0].get_text().strip()
        result[lable] = value
    interests = soup.select('#interestsDiv')[0].get_text().strip()
    result['interests'] = interests
    try:
        translate_name = soup.select('#translatedNameDiv')[0].get_text().strip()
        result['preferredNameDiv'] = result['preferredNameDiv'] + ' ' + translate_name
    except:
        result['preferredNameDiv'] = result['preferredNameDiv']
    return [
        result.get('ORCiD', ''),
        result.get('Author ID (Scopus)', ''),
        result.get('Researcher ID (WoS)', ''),
        result.get('Google Scholar',''),
        result.get('personalpictureDiv', ''),
        result.get('preferredNameDiv', ''),
        result.get('positionDiv', ''),
        result.get('deptDiv', ''),
        result.get('facultyDiv', ''),
        result.get('personalsiteDiv', ''),
        result.get('phoneDiv', ''),
        result.get('emailDiv', ''),
        result.get('interests','')
        ]


def main():
    url = 'http://ira.lib.polyu.edu.hk/cris/rp/rp00615'
    result = xglgwenxian(url)
    print(result)

if __name__ == '__main__':
    main()