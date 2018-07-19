#coding:utf-8
from bs4 import BeautifulSoup
import re
import urllib
from urllib.request import urlopen
from urllib.error import HTTPError
from distutils.filelist import findall
import xlwt
header = []
scs=[]
sc=[]
web = urlopen("https://baike.baidu.com/item/%E5%A4%A7%E5%AD%A6%E6%8E%92%E8%A1%8C%E6%A6%9C/3130064")
html = web.read()
soup = BeautifulSoup(html, 'html.parser')
tables = soup.find_all("table")
table = tables[1]
trs = table.find_all("tr")
header_tds = trs[0].find_all("td")
for i in range(8):
    header.append(header_tds[i].get_text())
scs.append(header)
for i in range(2,27):
    sc_tds = trs[i].find_all("td")
    for j in range(8):
        sc.append(sc_tds[j].get_text())
    scs.append(sc)
    sc=[]
print(scs)
# workbook=xlwt.Workbook(encoding='utf-8')
# booksheet=workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
# for i,row in enumerate(scs):
#     for j,col in enumerate(row):
#         booksheet.write(i,j,col)
# workbook.save('grade.xlsx')
file = open("1.txt","a")
for v in scs:
    file.write(v[0]+'\t'+v[1]+'\t'+v[2]+'\t'+v[3]+'\t'+v[4]+'\t'+v[5]+'\t'+v[6]+'\t'+v[7]+'\n')