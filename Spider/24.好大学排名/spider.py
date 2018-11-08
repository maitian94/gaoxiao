# -*- coding: utf-8 -*- 
import requests
from bs4 import BeautifulSoup
from utils import *
import re


def main2018():
    rankUrl = 'http://www.zuihaodaxue.com/zuihaodaxuepaiming2018.html'
    res = requests.get(rankUrl)
    res.encoding = 'utf8'
    rankSoup = BeautifulSoup(res.text, 'html.parser')
    rows = rankSoup.select('.hidden_zhpm .alt')
    for row in rows:
        tds = row.select('td')
        paiming = tds[0].text.strip()
        xiaoming = tds[1].text.strip()
        shengshi = tds[2].text.strip()
        zongfen = tds[3].text.strip()
        syzl = tds[4].text.strip()
        pyjg = tds[5].text.strip()
        shsy = tds[6].text.strip()
        kygm = tds[7].text.strip()
        kyzl = tds[8].text.strip()
        djcg = tds[9].text.strip()
        djrc = tds[10].text.strip()
        kjfw = tds[11].text.strip()
        cgzh = tds[12].text.strip()
        xsgjh = tds[13].text.strip()
        result = [paiming, xiaoming, shengshi, zongfen, syzl, pyjg, shsy, kygm, kyzl, djcg, djrc, kjfw, cgzh, xsgjh]
        write2csv('data/中国最好大学排名2018.csv', result)


def main2017():
    rankUrl = 'http://www.zuihaodaxue.com/zuihaodaxuepaiming2017.html'
    res = requests.get(rankUrl)
    res.encoding = 'utf8'
    rankSoup = BeautifulSoup(res.text, 'html.parser')
    rows = rankSoup.select('.hidden_zhpm tr')
    for row in rows:
        tds = row.select('td')
        paiming = re.match(r'(.*)\d', tds[0].text.strip()[:4]).group(0)
        xiaoming = tds[1].text.strip()
        shengshi = tds[2].text.strip()
        zongfen = tds[3].text.strip()
        syzl = tds[4].text.strip()
        pyjg = tds[5].text.strip()
        kygm = tds[6].text.strip()
        kyzl = tds[7].text.strip()
        djcg = tds[8].text.strip()
        djrc = tds[9].text.strip()
        kjfw = tds[10].text.strip()
        cgzh = tds[11].text.strip()
        xsgjh = tds[12].text.strip()
        result = [paiming, xiaoming, shengshi, zongfen, syzl, pyjg, kygm, kyzl, djcg, djrc, kjfw, cgzh, xsgjh]
        write2csv('data/中国最好大学排名2017.csv', result)


def main2016():
    rankUrl = 'http://www.zuihaodaxue.com/zuihaodaxuepaiming2016.html'
    res = requests.get(rankUrl)
    res.encoding = 'utf8'
    rankSoup = BeautifulSoup(res.text, 'html.parser')
    rows = rankSoup.select('.hidden_zhpm tr')
    for row in rows:
        tds = row.select('td')
        paiming = re.match(r'(.*)\d', tds[0].text.strip()[:4]).group(0)
        xiaoming = tds[1].text.strip()
        shengshi = tds[2].text.strip()
        zongfen = tds[3].text.strip()
        syzl = tds[4].text.strip()
        pyjg = tds[5].text.strip()
        kygm = tds[6].text.strip()
        kyzl = tds[7].text.strip()
        djcg = tds[8].text.strip()
        djrc = tds[9].text.strip()
        kjfw = tds[10].text.strip()
        cgzh = tds[11].text.strip()
        xsgjh = tds[12].text.strip()
        result = [paiming, xiaoming, shengshi, zongfen, syzl, pyjg, kygm, kyzl, djcg, djrc, kjfw, cgzh, xsgjh]
        write2csv('data/中国最好大学排名2016.csv', result)


def main2015():
    rankUrl = 'http://www.zuihaodaxue.com/zuihaodaxuepaiming2015_0.html'
    res = requests.get(rankUrl)
    res.encoding = 'utf8'
    rankSoup = BeautifulSoup(res.text, 'html.parser')
    rows = rankSoup.select('.hidden_zhpm tr')
    for row in rows:
        tds = row.select('td')
        paiming = re.match(r'(.*)\d', tds[0].text.strip()[:4]).group(0)
        xiaoming = tds[1].text.strip()
        shengshi = tds[2].text.strip()
        zongfen = tds[3].text.strip()
        rcpy = tds[4].text.strip()
        kxyj = tds[5].text.strip()
        shfw = tds[6].text.strip()
        result = [paiming, xiaoming, shengshi, zongfen, rcpy, kxyj, shfw]
        write2csv('data/中国最好大学排名2015.csv', result)


def maintylyxpm():
    # 体育类院系排名2018-2016
    for nianfen in ['2016', '2017', '2018']:
        rankUrl = 'http://www.zuihaodaxue.com/Sport-Science-Schools-and-Departments-%s.html' % nianfen
        print(rankUrl)
        res = requests.get(rankUrl)
        res.encoding = 'utf8'
        rankSoup = BeautifulSoup(res.text, 'html.parser')
        rows = rankSoup.select('tbody tr')
        for row in rows:
            tds = row.select('td')
            # paiming = re.match(r'(.*)\d', tds[0].text.strip()[:4]).group(0)
            paiming = tds[0].text.strip()
            xuexiao = tds[1].strong.text.strip()
            yuanxi = tds[1].div.div.text.strip()
            try:
                guojiadiqu = tds[2].img.attrs['title']
            except:
                guojiadiqu = re.split('/|\.', tds[2].img.attrs['src'])[1]
            zongfen = tds[3].text.strip()
            pub = tds[4].text.strip()
            cit = tds[5].text.strip()
            cpp = tds[6].text.strip()
            top = tds[7].text.strip()
            ic = tds[8].text.strip()
            result = [nianfen, paiming, xuexiao, yuanxi, guojiadiqu, zongfen, pub, cit, cpp, top, ic]
            # print(result)
            write2csv('data/全球体育类院系学术排名2016-2018.csv', result)


def mainxklypm():
    # 学科领域排名2007-2016
    for nianfen in range(2007, 2017):
        for xueke in ['SCI', 'ENG', 'LIFE', 'MED', 'SOC']:
            rankUrl = f'http://www.zuihaodaxue.com/Field{xueke}{nianfen}.html'
            print(rankUrl)
            res = requests.get(rankUrl)
            res.encoding = 'utf8'
            rankSoup = BeautifulSoup(res.text, 'html.parser')
            rows = rankSoup.select('tbody tr')
            if xueke == 'ENG':
                for row in rows:
                    tds = row.select('td')
                    paiming = tds[0].text.strip()
                    xuexiao = tds[1].text.strip()
                    try:
                        guojiadiqu = tds[2].img.attrs['title']
                    except:
                        guojiadiqu = re.split('/|\.', tds[2].img.attrs['src'])[1]
                    zongfen = tds[3].text.strip()
                    alumini = ''
                    award = ''
                    hici = tds[4].text.strip()
                    pub = tds[5].text.strip()
                    top = tds[6].text.strip()
                    fund = tds[7].text.strip()
                    result = [nianfen, xueke, paiming, xuexiao, guojiadiqu, zongfen, alumini, award, hici, pub, top,
                              fund]
                    # print(result)
                    write2csv('data/世界大学学科领域排名2007-2016.csv', result)
            else:
                for row in rows:
                    tds = row.select('td')
                    paiming = tds[0].text.strip()
                    xuexiao = tds[1].text.strip()
                    try:
                        guojiadiqu = tds[2].img.attrs['title']
                    except:
                        guojiadiqu = re.split('/|\.', tds[2].img.attrs['src'])[1]
                    zongfen = tds[3].text.strip()
                    alumini = tds[4].text.strip()
                    award = tds[5].text.strip()
                    hici = tds[6].text.strip()
                    pub = tds[7].text.strip()
                    top = tds[8].text.strip()
                    fund = ''
                    result = [nianfen, xueke, paiming, xuexiao, guojiadiqu, zongfen, alumini, award, hici, pub, top,
                              fund]
                    # print(result)
                    write2csv('data/世界大学学科领域排名2007-2016.csv', result)


def mainxkpm():
    # 学科排名2017-2018
    lyxkDic = {'理学': ["mathematics", "physics", "chemistry", "earth-sciences", "geography", "ecology"],
               '工学': ["mechanical-engineering", "electrical-electronic-engineering", "automation-control",
                      "telecommunication-engineering", "instruments-science-technology", "biomedical-engineering",
                      "computer-science-engineering", "civil-engineering", "chemical-engineering",
                      "materials-science-engineering", "nanoscience-nanotechnology", "energy-science-engineering",
                      "environmental-science-engineering", "water-resources", "food-science-technology",
                      "biotechnology",
                      "aerospace-engineering", "marine-ocean-engineering", "transportation-science-technology",
                      "remote-sensing", "mining-mineral-engineering", "metallurgical-engineering"],
               '生命科学': ['biological-sciences', 'human-biological-sciences', 'agricultural-sciences',
                        'veterinary-sciences'],
               '医学': ['clinical-medicine', 'public-health', 'dentistry-oral-sciences', 'nursing', 'medical-technology',
                      'pharmacy-pharmaceutical-sciences'],
               '社会科学': ["economics", "statistics", "law", "political-sciences", "sociology", "education",
                        "communication", "psychology", "business-administration", "finance", "management",
                        "public-administration", "hospitality-tourism-management", "library-information-science"]
               }
    for ly in lyxkDic.keys():
        for xk in lyxkDic[ly]:
            for nf in ['2017', '2018']:
                if nf == '2017':
                    url = f'http://www.zuihaodaxue.com/subject-ranking-2017/{xk}.html'
                else:
                    url = f'http://www.zuihaodaxue.com/subject-ranking/{xk}.html'
                res = requests.get(url)
                res.encoding = 'utf8'
                rankSoup = BeautifulSoup(res.text, 'html.parser')
                rows = rankSoup.select('tbody tr')
                for row in rows:
                    tds = row.select('td')
                    paiming = tds[0].text.strip()
                    xuexiao = tds[1].text.strip()
                    try:
                        guojiadiqu = tds[2].img.attrs['title']
                    except:
                        guojiadiqu = re.split('/|\.', tds[2].img.attrs['src'])[1]
                    zongfen = tds[3].text.strip()
                    lwzs = tds[4].text.strip()
                    yxl = tds[5].text.strip()
                    bl = tds[6].text.strip()
                    ws = tds[7].text.strip()
                    xs = tds[8].text.strip()
                    result = [nf, ly,xk, paiming, xuexiao, guojiadiqu, zongfen, lwzs, yxl, bl, ws, xs]

                    # print(result)
                    write2csv('data/世界一流学科排名2017-2018.csv', result)



def mainxspm():
    #学术排名
    for i in range(2018,2019):#2003 2019
        nf=str(i)
        url = f'http://www.zuihaodaxue.com/ARWU{nf}Candidates.html'
        res = requests.get(url)
        if i>2015:
            if 'Candidates' in url:
                res.encoding='utf8'
            else:
                res.encoding='gbk'
        else:
            res.encoding = 'utf8'
        rankSoup = BeautifulSoup(res.text, 'html.parser')
        rows = rankSoup.select('tbody tr')
        for row in rows:
            tds = row.select('td')
            paiming = tds[0].text.strip()
            xuexiao = tds[1].text.strip()
            try:
                guojiadiqu = tds[2].a.attrs['title'].strip('.')
            except:
                guojiadiqu =re.split('/|\.', tds[2].img.attrs['src'])[-2]
            if i ==2004:
                gjdqpm = ''
                nobel=''
                zf = tds[3].text.strip()
                alumni = tds[4].text.strip()
                award = tds[5].text.strip()
                hici = tds[6].text.strip()
                ns = tds[7].text.strip()
                pub = tds[8].text.strip()
                pcb = tds[9].text.strip()
                faculty =''
            elif  'Candidates' in url:
                gjdqpm = ''
                nobel=''
                zf = ''
                alumni = tds[3].text.strip()
                award = tds[4].text.strip()
                hici = tds[5].text.strip()
                ns = tds[6].text.strip()
                pub = tds[7].text.strip()
                pcb = tds[8].text.strip()
                faculty =''
            elif i == 2003:
                gjdqpm = ''
                zf = tds[3].text.strip()
                nobel = tds[4].text.strip()
                alumni = ''
                award = ''
                hici = tds[5].text.strip()
                ns = tds[6].text.strip()
                pub = tds[7].text.strip()
                pcb = ''
                faculty = tds[8].text.strip()
            else:
                gjdqpm = tds[3].text.strip()
                nobel=''
                zf = tds[4].text.strip()
                alumni = tds[5].text.strip()
                award = tds[6].text.strip()
                hici = tds[7].text.strip()
                ns = tds[8].text.strip()
                pub = tds[9].text.strip()
                pcb = tds[10].text.strip()
                faculty =''
            result = [nf,  paiming, xuexiao, guojiadiqu, gjdqpm, zf, nobel, alumni, award, hici,
                      ns,pub,pcb,faculty]
            print(result)
            write2csv('data/世界大学学术排名2003-2018.csv', result)

if __name__ == "__main__":
    # write2csv('data/中国最好大学排名2015.csv',['排名','学校名称','省市','总分','生源质量（新生高考成绩得分）',
    #                                    '培养结果（毕业生就业率）',
    #                                    '科研规模（论文数量·篇）','科研质量（论文质量·FWCI）',
    #                                    '顶尖成果（高被引论文·篇）','顶尖人才（高被引学者·人）','科技服务（企业科研经费·千元）',
    #                                    '成果转化（技术转让收入·千元）','学生国际化（留学生比例）'])
    # write2csv('data/中国最好大学排名2015.csv', ['排名', '学校名称', '省市', '总分', '人才培养得分', '科学研究得分', '社会服务得分'])
    # write2csv('data/全球体育类院系学术排名2016-2018.csv', ['年份','排名', '学校名称', '院系', '国家/地区', '总分', '指标得分（PUB）',
    #                                             '指标得分（CIT）', '指标得分（CPP）', '指标得分（TOP）', '指标得分（IC）'])
    # write2csv('data/学科', ['年份', '领域', '学科', '世界排名', '学校名称', '国家/地区', '总分',
    #                                            '指标得分（论文总数）','指标得分（论文标准化影响力）',
    #                                            '指标得分（国际合作论文比例）','指标得分（顶尖期刊论文数）',
    #                                            '指标得分（教师获权威奖项数）'])
    # write2csv('data/世界大学学术排名2003-2018.csv', ['年份','世界排名', '学校名称', '国家/地区', '国家/地区排名', '总分',
    #                                          '指标得分（nobel）', '指标得分（Alumni）',
    #                                          '指标得分（Award）', '指标得分（HiCi）',
    #                                          '指标得分（N&S）','指标得分（PUB）','指标得分（PCB）','指标得分（faculty）'])
    mainxspm()
