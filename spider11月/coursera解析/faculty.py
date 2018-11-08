import requests
from lxml import etree

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
        # print(name, authors[name]) # name是作者名字, authors[name]是url
        results['Author'] = name
        # try:
        resp = requests.get(authors[name], headers=headers)
        html = etree.HTML(resp.text)
        dts = html.xpath("//dl[@class='person-description']//dt")
        for i in range(1, len(dts)+1):
            label = html.xpath("//dl[@class='person-description']/dt[%d]//text()" % i)[0].split(":")[0]
            value = html.xpath("//dl[@class='person-description']/dd[%d]//text()" % i)[0]
            results[label] = value  # 这里是存储class=person-description的处理

        subs = html.xpath("//div[@class='sub-section clearfix']")
        for i in range(1, len(subs)+1):
            try:
                label = html.xpath("//div[@class='sub-section clearfix'][%d]//h2/text()" % i)[0]
                value = html.xpath("//div[@class='sub-section clearfix'][%d]//p/text()" % i)[0].replace("\xa0", " ") + ''.join(html.xpath("//div[@class='sub-section clearfix'][%d]//ul/li/text()" % i)).replace("\xa0", " ")
                results[label] = value
            except:
                continue

        print(results)
        # except:
        #     continue


def main():
    choice = ['full-time-faculty', 'part-time-faculty']
    for it in choice:
        url = 'https://elliott.gwu.edu/' + it
        authors = parse(url)
        # print(author)
        detail_author_parse(authors)


if __name__ == '__main__':
    main()

