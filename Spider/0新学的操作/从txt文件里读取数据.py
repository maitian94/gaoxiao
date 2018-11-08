#coding=utf8

def type():
    with open('C:\\Users\\admin\\Desktop\\出版社类别.txt','r') as file:
        lines = file.readlines()
        types = []
        for type in lines:
            type = type.strip()
            types.append(type)
        return types

type()