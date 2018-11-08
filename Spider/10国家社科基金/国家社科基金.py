#coding=utf8
import requests
from bs4 import BeautifulSoup as bs
from utils import write2csv
import time

def parser():
    result = {}
    ziduans = ['项目批准号','项目类别','学科分类','项目名称','立项时间',
               '项目负责人','专业职务','工作单位','单位类别','所在省区市',
               '所属系统','成果名称','成果形式','成果等级','结项时间',
               '结项证书号','出版社','出版时间','作者','获奖情况']
    for z in range(1,3303):
        try:
            nexturl = 'http://fz.people.com.cn/skygb/sk/index.php/Index/seach?&p='+ str(z)
        except:
            time.sleep(5)
            nexturl = 'http://fz.people.com.cn/skygb/sk/index.php/Index/seach?&p=' + str(z)
        print('**********正在打印第'+str(z)+'页***********')
        res = requests.post(nexturl)
        soup = bs(res.text, 'html.parser')
        tds = soup.select('.jc_a td')
        for i in range(0,len(tds),20):
            for j in range(20):
                result[ziduans[j]] = tds[i+j].text.strip()
            print(result)
            write2csv('csvFiles/国家社科基金.csv', [
            result.get('项目批准号', ''),
            result.get('项目类别', ''),
            result.get('学科分类', ''),
            result.get('项目名称', ''),
            result.get('立项时间', ''),
            result.get('项目负责人', ''),
            result.get('专业职务', ''),
            result.get('工作单位', ''),
            result.get('单位类别', ''),
            result.get('所在省区市', ''),
            result.get('所属系统', ''),
            result.get('成果名称', ''),
            result.get('成果形式', ''),
            result.get('成果等级', ''),
            result.get('结项时间', ''),
            result.get('结项证书号', ''),
            result.get('出版社', ''),
            result.get('出版时间', ''),
            result.get('作者', ''),
            result.get('获奖情况', '')
                ])


def main():
    result = parser()
    # print(result)

if __name__ == '__main__':
    main()