# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from utils import *
from selenium import webdriver
from pprint import pprint


def rankingsBySubject():
    url = 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/physical_sciences_rankings_2011_limit0_6734ee4616ee0618d3c596fdd1920e61.json'
    headers = {
        'cookie':'siteCountry=CN; cookie-agreed=2; Drupal.visitor.the_user=%7B%22show_menu%22%3A0%2C%22user_closed%22%3A0%7D; __tesu=a0556562-859f-4d9f-b218-3bcf8c065805; __tese=aca42a30-3df5-4768-bb5e-e9bad248768d; geoCountry=HK; has_js=1; __tesv=0b95a21d-d72a-4938-8d37-d80489d16306; __tess=home%7C%7C6',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    for i in range(len(res.json()['data'])):
        details = res.json()['data']
        subject = 'Physical Sciences'
        url = 'https://www.timeshighereducation.com' + details[i].get('url').strip()
        year = '2011'
        rank = details[i].get('rank').strip()
        name = details[i].get('name').strip()
        location = details[i].get('location').strip()
        try:
            FTEstu_num = details[i].get('stats_number_students').strip()
        except:
            FTEstu_num = ''
        try:
            staffstu_num = details[i].get('stats_student_staff_ratio').strip()
        except:
            staffstu_num = ''
        try:
            interstu = details[i].get('stats_pc_intl_students').strip()
        except:
            interstu = ''
        try:
            fm_ratio = details[i].get('stats_female_male_ratio').replace(' ','').replace(':00','')
        except:
            fm_ratio = ''
        overall = details[i].get('scores_overall').replace('-','').strip()
        teaching = details[i].get('scores_teaching').replace('-','').strip()
        research = details[i].get('scores_research').replace('-','').strip()
        citations = details[i].get('scores_citations').replace('-','').strip()
        industry_income = details[i].get('scores_industry_income').replace('-','').strip()
        inter_outlook = details[i].get('scores_international_outlook').replace('-','').strip()
        result = [subject, url,year, rank, name, location, FTEstu_num, staffstu_num, interstu, fm_ratio, overall, teaching, research, citations, industry_income, inter_outlook]
        print(result)
        write2csv('data/Rankings By Subject.csv', result)

if __name__ == '__main__':
    # write2csv('data/Rankings By Subject.csv', ['subject', 'url', 'year', 'rank', 'school name', 'location', 'No.of FTE Students', 'No.of Students per staff',  'international students', 'female:male ratio', 'overall', 'teaching', 'research', 'citation', 'industry income', 'international outlook'])
    rankingsBySubject()