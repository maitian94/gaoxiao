#coding=utf8
import requests
from lxml import etree
from utils import *

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Referer': 'https://elliott.gwu.edu/emeritus-faculty',
}


def parse(url):
    authors = {}
    resp = requests.get(url, headers=headers)
    html = etree.HTML(resp.text)
    lis = html.xpath("//ul[@class='content']/li")
    for li in lis:
        detail_lis = li.xpath(".//li")
        for detail_li in detail_lis:
            try:
                author = ''.join(detail_li.xpath("./a/text()")).replace("\r\n", "")
                href = 'https://elliott.gwu.edu' + detail_li.xpath("./a/@href")[0]
                # print(author, href)
                authors[author] = href
            except:
                continue
    return authors # 我把作者和对应作者链接存到一个字典 


def detail_author_parse(authors):

    for name in authors:
        results = {}
        print(name, authors[name])
        results['Author'] = name
        resp = requests.get(authors[name], headers=headers)
        html = etree.HTML(resp.text)
        pic_url = html.xpath("//div[@class='person-image-wrapper']/img/@src")
        results['图片链接'] = pic_url
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
        results['教师分类'] = 'Full-Time'
        print(results)
        write2csv('data/数据.csv',[
            results.get('教师分类',''),
            results.get('页面链接',''),
            results.get('Author',''),
            results.get('图片链接',''),
            results.get('Title:',''),
            results.get('Faculty:',''),
            results.get('Office:',''),
            results.get('Phone:',''),
            results.get('Fax:',''),
            results.get('Areas of Expertise',''),
            results.get('Current Research',''),
            results.get('Education',''),
            results.get('Publications',''),
            results.get('Classes Taught',''),
            results.get('Curriculum Vitae','')

        ])


def main():
    choice = ['full-time-faculty', 'part-time-faculty']
    for it in choice:
        url = 'https://elliott.gwu.edu/' + it
        authors = parse(url)
        # print(author)
        detail_author_parse(authors)


if __name__ == '__main__':
    main()

