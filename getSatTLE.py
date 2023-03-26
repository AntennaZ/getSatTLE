# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 11:35:13 2021

@author: AntennaZ
"""

import requests
from bs4 import BeautifulSoup
import xlrd
from xlutils.copy import copy

url = 'https://celestrak.com/NORAD/elements/starlink.txt'
resp = requests.get(url) #请求网页
text = BeautifulSoup(resp.content,'html5lib').get_text()#得到源代码
A = text.split('\n')
A.pop(len(A)-1)#去除末尾多余空行
i = 0
while i<len(A):
    if i%3==0 and A[i][0:8]!='STARLINK':
        A.pop(i)
        A.pop(i)
        A.pop(i)
        i-=3
    i+=3
#筛掉非星链数据
satNum = [] #卫星数量列表
time = '19029'
cnt = 0
file = open('20'+time+'.txt','w')
for i in range(len(A)):
    if i%3==0 and A[i+1][9:14]!=time:
        #file.write('共'+str(cnt/3)+'颗卫星')
        satNum.append(cnt/3)
        time = A[i+1][9:14]
        file = open('20'+time+'.txt','w')
        cnt = 1
        file.write(A[i])
        file.write('\n')
    else:
        cnt = cnt+1
        file.write(A[i])
        file.write('\n')
#file.write('共'+str(cnt/3)+'颗卫星')
satNum.append(cnt/3)
file.close()

rb = xlrd.open_workbook('卫星数目.xls')
wb = copy(rb)                          #利用xlutils.copy下的copy函数复制
ws = wb.get_sheet(0)                   #获取表单0
for i in range(len(satNum)):
    ws.write(i,0,satNum[i])
wb.save('卫星数目.xls')
print('Done! ;)')
