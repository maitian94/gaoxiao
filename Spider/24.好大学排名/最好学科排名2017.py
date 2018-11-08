# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from utils import *
import re
def mainzhxk():
    #最好学科排名
    category_dic = {
        '哲学':['zhexue'],
        '经济学':['lilunjingjixue','yingyongjingjixue'],
        '法学':['faxue','zhengzhixue','shehuixue','minzuxue','makesizhuyililun'],
        '教育学':['jiaoyuxue','xinlixue','tiyuxue'],
        '文学':['zhongguoyuyanwenxue','waiguoyuyanwenxue','xinwenchuanboxue'],
        '历史学':['kaoguxue','zhongguoshi','shijieshi'],
        '理学':['shuxue','wulixue','huaxue','tianwenxue','dilixue','daqikexue','haiyangkexue','diqiuwulixue','dizhixue','shengwuxue','shengtaixue','tongjixue'],
        '工学':['lixue','jixiegongcheng','guangxuegongcheng','yiqikexueyujishu','cailiaokexueyugongcheng','yejingongcheng','dongligongchengjigongchengrewuli','dianqigongcheng','dianzikexueyujishu','xinxiyutongxingongcheng','kongzhikexueyugongcheng','jisuanjikexueyujishu','jianzhuxue','tumugongcheng','shuiligongcheng','cehuikexueyujishu','huaxuegongchengyujishu','dizhiziyuanyudizhigongcheng','kuangyegongcheng','shiyouyutianranqigongcheng','fangzhikexueyugongcheng','qinggongjishuyugongcheng','jiaotongyunshugongcheng','chuanboyuhaiyanggongcheng','hangkongyuhangkexueyujishu','hekexueyujishu','nongyegongcheng','huanjingkexueyugongcheng','shengwuyixuegongcheng','shipinkexueyugongcheng','chengxiangguihuaxue','ruanjiangongcheng','anquankexueyugongcheng'],
        '农学':['zuowuxue','yuanyixue','nongyeziyuanyuhuanjing','zhiwubaohu','chumuxue','shouyixue','linxue','shuichan','caoxue'],
        '医学':['jichuyixue','linchuangyixue','kouqiangyixue','gonggongweishengyuyufangyixue','zhongyixue','zhongxiyijiehe','yaoxue','zhongyaoxue','tezhongyixue','hulixue'],
        '管理学':['guanlikexueyugongcheng','gongshangguanli','nonglinjingjiguanli','gonggongguanli','tushuqingbaoyudanganguanli'],
        '艺术学':['yishuxuelilun','yinyueyuwudaoxue','xijuyuyingshixue','meishuxue','shejixue']
    }

    for category in category_dic.items():
        # print(category)
        for i in range(len(category[1])):
            a= category[1][i]
            url = 'http://www.zuihaodaxue.com/BCSR/'+ category[1][i] +'2017.html'
            print(url)
            res = requests.get(url)
            res.encoding = 'utf8'
            soup = bs(res.text, 'html.parser')
            menlei = category[0]
            yjxk = soup.select('.post-title')[0].text.strip()
            yjxk = re.findall('.*?2017-([\u4e00-\u9fa5]+)', yjxk)
            rows = soup.select('.news-text .bgfd')
            for row in rows:
                tds = row.select('td')
                paiming = tds[0].text.strip()
                bfwd = tds[1].text.strip()
                yxmc = tds[2].text.strip()
                try:
                    bsd = tds[3].select('img')[0].attrs['title'].strip()
                except:
                    bsd = ''
                try:
                    zdxk = tds[4].select('img')[0].attrs['title'].strip()
                except:
                    zdxk = ''
                zongfen = tds[5].text.strip()
                result=[menlei,yjxk,paiming,bfwd,yxmc,bsd,zdxk,zongfen]
                write2csv('data/中国最好大学学科排名2017.csv',result)



if __name__ == "__main__":
    write2csv('data/中国最好大学学科排名2017.csv',['门类','一级学科','排名','百分段位','院校名称','博士点','重点学科','总分'])
    mainzhxk()

