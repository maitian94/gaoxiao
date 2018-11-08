# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from utils import *
import re
def mainlasddx():
    #两岸四地大学排名
    rankUrl_0 = 'http://www.zuihaodaxue.com/Greater_China_Ranking2017_0.html'
    res=requests.get(rankUrl_0)
    res.encoding='utf8'
    rankSoup_0 = BeautifulSoup(res.text,'html.parser')
    rows = rankSoup_0.select('.news-text tr')[3:]
    for row in rows:
        tds = row.select('td')
        paiming = tds[0].text.strip()
        xiaoming = tds[1].text.strip()
        diqu = tds[2].text.strip()
        zongfen = tds[3].text.strip()
        yjsbl = tds[4].text.strip()
        lxsbl = tds[5].text.strip()
        ssb = tds[6].text.strip()
        bsxwsys_zl = tds[7].text.strip()
        bsxwsys_sj = tds[8].text.strip()
        xyhj_zl = tds[9].text.strip()
        xyhj_sj = tds[10].text.strip()
        result = [paiming, xiaoming, diqu, zongfen, yjsbl, lxsbl, ssb, bsxwsys_zl, bsxwsys_sj, xyhj_zl,
                  xyhj_sj]
        write2csv('data/中国两岸四地大学排名2017_0.csv',result)

    rankUrl_1 = 'http://www.zuihaodaxue.com/Greater_China_Ranking2017_1.html'
    res = requests.get(rankUrl_1)
    res.encoding = 'utf8'
    rankSoup_1 = BeautifulSoup(res.text, 'html.parser')
    rows = rankSoup_1.select('.news-text tr')[3:]
    for row in rows:
        tds = row.select('td')
        kyjf_zl = tds[4].text.strip()
        kyjf_sj = tds[5].text.strip()
        djlw_zl = tds[6].text.strip()
        djlw_sj = tds[7].text.strip()
        gjlw_zl = tds[8].text.strip()
        gjlw_sj = tds[9].text.strip()
        gjzl_zl = tds[10].text.strip()
        gjzl_sj = tds[11].text.strip()
        result = [kyjf_zl, kyjf_sj, djlw_zl, djlw_sj, bsxwsys_sj, gjlw_zl, gjlw_sj, gjzl_zl,
                  gjzl_sj]
        write2csv('data/中国两岸四地大学排名2017_1.csv',result)

    #
    rankUrl_2 = 'http://www.zuihaodaxue.com/Greater_China_Ranking2017_2.html'
    res = requests.get(rankUrl_2)
    res.encoding = 'utf8'
    rankSoup_2 = BeautifulSoup(res.text, 'html.parser')
    rows = rankSoup_2.select('.news-text tr')[3:]
    for row in rows:
        tds = row.select('td')
        bsxwjsbl = tds[4].text.strip()
        jshj_zl = tds[5].text.strip()
        jshj_sj = tds[6].text.strip()
        gbykxj_zl = tds[7].text.strip()
        gbykxj_sj = tds[8].text.strip()
        result = [bsxwjsbl, jshj_zl, jshj_sj, gbykxj_zl, gbykxj_sj]
        write2csv('data/中国两岸四地大学排名2017_2.csv',result)

    rankUrl_3 = 'http://www.zuihaodaxue.com/Greater_China_Ranking2017_3.html'
    res = requests.get(rankUrl_3)
    res.encoding = 'utf8'
    rankSoup_3 = BeautifulSoup(res.text, 'html.parser')
    rows = rankSoup_3.select('.news-text tr')[3:]
    for row in rows:
        tds = row.select('td')
        bxjf_zl = tds[4].text.strip()
        bxjf_sj = tds[5].text.strip()

        result = [bxjf_zl, bxjf_sj]
        write2csv('data/中国两岸四地大学排名2017_3.csv',result)








if __name__ == "__main__":
    # write2csv('data/中国最好大学排名2015.csv',['排名','学校名称','省市','总分','生源质量（新生高考成绩得分）',
    #                                    '培养结果（毕业生就业率）',
    #                                    '科研规模（论文数量·篇）','科研质量（论文质量·FWCI）',
    #                                    '顶尖成果（高被引论文·篇）','顶尖人才（高被引学者·人）','科技服务（企业科研经费·千元）',
    #                                    '成果转化（技术转让收入·千元）','学生国际化（留学生比例）'])
    write2csv('data/中国两岸四地大学排名2017_0.csv',['排名','学校名称','地区','总分','研究生比例(5%)','留学生比例(5%)','师生比(5%)','博士学位授予数(10%)-总量','博士学位授予数(10%)-师均','校友获奖(10%)-总量','校友获奖(10%)-生均','科研经费(5%)-总量','科研经费(5%)-师均','顶尖论文(10%)-总量','顶尖论文(10%)-师均','国际论文(10%)-总量','国际论文(10%)-师均','国际专利(10%)-总量','国际专利(10%)-师均','博士学位教师比例(5%)','教师获奖(10%)-总量','教师获奖(10%)-师均','高被引科学家(10%)-总量','高被引科学家(10%)-师均','办学经费(5%)-总量','办学经费(5%)-生均'])
    mainlasddx()