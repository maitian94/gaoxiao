#coding=utf-8
import requests
from lxml import etree
from utils import *
from bs4 import BeautifulSoup as bs

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Referer': 'https://elliott.gwu.edu/emeritus-faculty',
}


def parse(url):
    authors = {}
    resp = requests.get(url, headers=headers)
    soup = bs(requests.get(url).text, 'html.parser')
    panels = soup.select('.panel-body')
    for panel in panels:
        # print(panel.select('p'))
        for i in range(1, len(panel.select('p')) - 1):
            author = panel.select('p')[i].select('a')[0].text.strip()
            href = 'https://elliott.gwu.edu' + panel.select('p')[i].select('a')[0].attrs['href']
            authors[author] = href
    # html = etree.HTML(resp.text)
    # lis = html.xpath("//ul[@class='content']/li")
    # for li in lis:
    #     detail_lis = li.xpath(".//li")
    #     for detail_li in detail_lis:
    #         try:
    #             author = ''.join(detail_li.xpath("./a/text()")).replace("\r\n", "")
    #             href = 'https://elliott.gwu.edu' + detail_li.xpath("./a/@href")[0]
    #             # print(author, href)
    #             authors[author] = href
    #         except:
    #             continue
    return authors # 我把作者和对应作者链接存到一个字典


def detail_author_parse(authors):

    for name in authors:
        results = {}
        print(name, authors[name])
        writeurl2txt('data/url.txt',authors[name])
        results['页面链接'] = authors[name]
        results['Author'] = name
        resp = requests.get(authors[name], headers=headers)
        html = etree.HTML(resp.text)
        try:
            pic_url = html.xpath("//div[@class='person-image-wrapper']/img/@src")
        except:
            pic_url = ''
        try:
            results['图片链接'] = pic_url[0]
        except:
            results['图片链接'] = ''
        dts = html.xpath("//dl[@class='person-description']//dt")
        for i in range(1, len(dts)+1):
            label = html.xpath("//dl[@class='person-description']/dt[%d]//text()" % i)[0].split(":")[0]
            value = html.xpath("//dl[@class='person-description']/dd[%d]//text()" % i)[0]
            results[label] = value

        subs = html.xpath("//div[@class='sub-section clearfix']")
        for i in range(1, len(subs)+1):
            try:
                label = ''.join(html.xpath("//div[@class='sub-section clearfix'][%d]//h2/text()" % i))
                if label == "":
                    label = 'Curriculum Vitae'
                    value = ','.join(html.xpath("//div[@class='sub-section clearfix'][%d]//p//text()" % i)).replace(
                        "\xa0", " ").replace("\n", '')
                    results[label] = value
                    continue
                value = ','.join(html.xpath("//div[@class='sub-section clearfix'][%d]//p//text()" % i)).replace("\xa0", " ").replace("\n", '') + ','.join(html.xpath("//div[@class='sub-section clearfix'][%d]//ul//li//text()" % i)).replace("\xa0", " ").replace("\n", '')
                results[label] = value
            except:
                continue
        results['教师分类'] = 'Emeritus Faculty'
        print(results)
        write2csv('data/数据.csv', [
            results.get('教师分类',''),
            results.get('页面链接',''),
            results.get('Author',''),
            results.get('图片链接',''),
            results.get('Title',''),
            results.get('Faculty',''),
            results.get('Office',''),
            results.get('Phone',''),
            results.get('Fax',''),
            results.get('Website', ''),
            results.get('Areas of Expertise',''),
            results.get('Current Research',''),
            results.get('Education',''),
            results.get('Publications',''),
            results.get('Classes Taught',''),
            results.get('Curriculum Vitae','')

        ])


def main():
    choice = ['emeritus-faculty']
    for it in choice:
        url = 'https://elliott.gwu.edu/' + it
        authors = parse(url)
        # print(author)
        detail_author_parse(authors)


if __name__ == '__main__':
    # write2csv('data/数据.csv', ['教师分类', '页面链接', 'Author', '图片链接', 'Title', 'Faculty', 'Office', 'Phone', 'Fax',
    #                           'Website', 'Areas of Expertise', 'Current Research', 'Education', 'Publications', 'Classes Taught',
    #                           'Curriculum Vitae'])
    main()

