#coding=utf8
import requests
from bs4 import BeautifulSoup as bs

def parse():
    url = 'https://databases.hollis.harvard.edu/primo-explore/fulldisplay?docid=01HVD_ALMA612220051990003941&context=L&vid=HVD_DB&lang=en_US&search_scope=default_scope&adaptor=Local%20Search%20Engine&tab=databases&query=lsr39,exact,General&sortby=title&offset=0'
    soup = bs(requests.get(url).text,'html.parser')
    print(soup)

if __name__ == '__main__':
    parse()