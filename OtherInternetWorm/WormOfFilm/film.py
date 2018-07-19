#coding:utf-8
from bs4 import BeautifulSoup
import re
import urllib
from urllib.request import urlopen
from urllib.error import HTTPError
from distutils.filelist import findall
from text9.dbcon import *
import pymysql
import threading
import queue
filmname = []
filmscore=[]
filmpro = []
filmnum = []
urls=[]
film = []
global myqueue
myqueue = queue.Queue(maxsize=10)
for i in range(5):
    j = i * 30
    url = 'http://v.qq.com/x/list/tv?iarea=-1&iyear=2017&offset=' + str(j)
    myqueue.put(url)
def func():
    if not myqueue.empty():
        urlt = myqueue.get()
        web = urlopen(urlt)
        html = web.read()
        html = html.decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        lis = soup.find_all("li", "list_item")
        for i in range(len(lis)):
            name = lis[i].find("div",class_="figure_title_score").find("strong",class_="figure_title").get_text()
            score = float(lis[i].find("div",class_="figure_title_score").find("div",class_="figure_score").find("em",class_="score_l").get_text()+lis[i].find("div",class_="figure_title_score").find("div",class_="figure_score").find("em",class_="score_s").get_text())
            pro = lis[i].find("div", class_="figure_desc").find("a").get("title")
            num = lis[i].find("div",class_="figure_count").find("span",class_="num").get_text()
            if(num[len(num)-1] == '万'):
                num = float(num[:len(num)-1])/10000
            else:
                num = float(num[:len(num) - 1])
            filmname.append(name)
            filmscore.append(score)
            filmpro.append(pro)
            filmnum.append(num)
        if myqueue.empty():
            film.append(filmname)
            film.append(filmscore)
            film.append(filmpro)
            film.append(filmnum)
            # for i in range(len(filmname)):
            #     name = film[0]
            #     score = film[1]
            #     pro = film[2]
            #     num = film[3]
            #     conn = DbConn("localhost", "root", "root", "school_db")
            #      cursor = conn.DBconnect()
            #     sql = "insert into film_sy VALUES('%s','%s','%s','%s')" % (name[i],score[i],pro[i],num[i])
            #     conn.Sql(sql)
            #     conn.commit()
            #     conn.close()
            print(len(film),film)
def run():
    for k in range(5):
        threading.Thread(target=func(), args=(k,)).start()
if __name__ == '__main__':
    run()

