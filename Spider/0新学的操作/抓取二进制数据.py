#coding=utf8
import requests

#把图片链接转换成了图片，并保存在文件picture.ico里
#open方法第一个参数是文件名，图片格式文件以ico为文件后缀，，第二个参数代表以二进制写的形式打开，可以向文件中写入二进制数据
#音频和视频文件也可以用这种方法获取
res = requests.get('https://online-learning.harvard.edu/sites/default/files/styles/course_image/public/course/stefan-stefancik-257625-unsplash.jpg?itok=DZoT0KzD')
with open('picture.ico','wb') as f:
    f.write(res.content)