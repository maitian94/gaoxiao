# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from utils import *
from selenium import webdriver
from pprint import pprint

def worldRanking():
    url = 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/asia_university_rankings_2013_limit0_214d48f4fdb3a3d448e5886b5c2a9577.json'
    headers = {
        'cookie':'siteCountry=CN; cookie-agreed=2; Drupal.visitor.the_user=%7B%22show_menu%22%3A0%2C%22user_closed%22%3A0%7D; __tesu=a0556562-859f-4d9f-b218-3bcf8c065805; __tese=aca42a30-3df5-4768-bb5e-e9bad248768d; geoCountry=HK; has_js=1; __tesv=0b95a21d-d72a-4938-8d37-d80489d16306; __tess=home%7C%7C6',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    for i in range(len(res.json()['data'])):
        details = res.json()['data']
        ranking_type = 'Asia University Rankings'
        year = '2013'
        url = 'https://www.timeshighereducation.com' + details[i].get('url').strip()
        rank = details[i].get('rank').strip()
        name = details[i].get('name').strip()
        try:
            location = details[i].get('location').strip()
        except:
            location = ''
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
        try:
            finance = details[i].get('stats_fin_per_stu_yen').strip()
        except:
            finance = ''
        try:
            resources = details[i].get('scores_resources').replace('-', '').strip()
        except:
            resources = ''
        try:
            engagement = details[i].get('scores_engagement').replace('-', '').strip()
        except:
            engagement = ''
        try:
            outcomes = details[i].get('scores_outcomes').replace('-', '').strip()
        except:
            outcomes = ''
        try:
            environment = details[i].get('scores_environment').replace('-', '').strip()
        except:
            environment = ''
        try:
            overall = details[i].get('scores_overall').strip()
        except:
            overall = ''
        try:
            teaching = details[i].get('scores_teaching').strip()
        except:
            teaching = ''
        try:
            tuition_fees = details[i].get('stats_fees_oos').strip()
        except:
            tuition_fees = ''
        try:
            room_board = details[i].get('stats_board').strip()
        except:
            room_board = ''
        try:
            salary = details[i].get('stats_salary').strip()
        except:
            salary = ''
        try:
            research = details[i].get('scores_research').strip()
        except:
            research = ''
        try:
            citations = details[i].get('scores_citations').strip()
        except:
            citations = ''
        try:
            industry_income = details[i].get('scores_industry_income').strip()
        except:
            industry_income = ''
        try:
            inter_outlook = details[i].get('scores_international_outlook').strip()
        except:
            inter_outlook = ''
        result = [ranking_type, year, url, rank, name, location, FTEstu_num, staffstu_num, interstu, fm_ratio, overall, teaching, research, citations, industry_income, inter_outlook,  finance, resources, engagement, outcomes, environment, tuition_fees,room_board,salary]
        print(result)
        write2csv('data/World University Rankings.csv', result)




if __name__ == '__main__':
    # write2csv('data/World University Rankings.csv', ['ranking_type','year','url', 'rank', 'school name', 'location', 'No.of FTE Students', 'No.of Students per staff',  'international students', 'female:male ratio', 'overall', 'teaching', 'research', 'citation', 'industry income', 'international outlook','finance','resources','engagement','outcomes','environment'])
    worldRanking()