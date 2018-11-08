# -*- coding: utf-8 -*- 
import os

def main(filepath: str):
    lineNum = 0
    files = os.listdir(filepath)
    os.chdir(filepath)
    for file in files:
        print(file)
        if file.endswith('csv'):
            f=open(file,encoding='utf8')
            lineNum+=f.readlines().__len__()
            f.close()
    print(lineNum-len(files))

if __name__ == '__main__':
    main(r'C:\Users\admin\PycharmProjects\spider11月\4.网上报告厅\data')