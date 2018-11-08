tasks = [i for i in open(r'C:\Users\admin\PycharmProjects\spider11月\7.易阅通\data\易阅通.csv',encoding='utf8')]
print(list(set(tasks)))

print(len(list(set(tasks))))
task = list(set(tasks))
print('正在写入...')
f = open(r'C:\Users\admin\PycharmProjects\spider11月\7.易阅通\data\易阅通去重.csv','a',encoding='utf8')
for t in task:
    # print(t)
    f.write(t)
f.close()
print('Done!')