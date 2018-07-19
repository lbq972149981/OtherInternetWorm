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
teamid = [] #球队编号
teamname=[] #球队名称
season = [] #赛季
shoot = []  #投篮
shootrating = [] #投篮命中
shootsell = []   #投篮出手
trisection = []  #三分
trisectionrating = [] #三分命中
trisectionsell = []   #三分出手
penaltyshot = []      #罚球
penaltyshotrating = []#罚球命中
penaltyshotsell = []  #罚球出手
rebound = []   #篮板球
frontcour = [] #前场
backcourt = [] #后场
AssistsAsts = [] #助攻
StealsStls = []  #抢断
BlockShotsBlks = [] #盖帽
TurnOverTOs = [] #失误
Fouls = []       #犯规
PointsPTs = []   #得分
pointsagainst = [] #失分
victory = []       #胜
defeat = []        #负
score = []         #综合得分
urls=[]
NBA = [teamid,teamname,season,shoot,shootrating,shootsell,trisection,trisectionrating,trisectionsell,penaltyshot,
       penaltyshotrating,penaltyshotsell,rebound,frontcour,backcourt,AssistsAsts,StealsStls,BlockShotsBlks,
       TurnOverTOs,Fouls,PointsPTs,pointsagainst,victory,defeat,score]
global myqueue
myqueue = queue.Queue(maxsize=10)
for i in range(5):
    url = "http://stat-nba.com/query_team.php?page="+str(i)+"&QueryType=ss&order=1&crtcol=formular&SsType=season&Formular=result_out_wdivideleftbracketresult_out_waddresult_out_lrightbracketmultiply100&PageNum=30#label_show_result"
    myqueue.put(url)
# for i in range(myqueue.qsize()):
#     if not myqueue.empty():
#         print(myqueue.get())
def dataTofloat(nbalist):
    newnbalist = []
    for v in nbalist:
        v = float(v)
        newnbalist.append(v)
    return newnbalist
def dataToint(nbalist):
    newnbalist = []
    for v in nbalist:
        v = int(v)
        newnbalist.append(v)
    return newnbalist
def dateformat(nbalist):
    newnbalist = []
    for v in nbalist:
        v = float(v[0:len(v)-1])
        newnbalist.append(v)
    return newnbalist
def Pretreatment():
    NBA[0] = dataToint(NBA[0])
    NBA[3] = dateformat(NBA[3])
    NBA[6] = dateformat(NBA[6])
    NBA[9] = dateformat(NBA[9])
    for i in range(3, 25):
        if i == 22 or i == 23:
            NBA[i] = dataToint(NBA[i])
        else:
            NBA[i] = dataTofloat(NBA[i])
def insertToMysql():
    for i in range(len(NBA[0])):
        teamid = NBA[0]
        teamname = NBA[1]  # 球队名称
        season = NBA[2]  # 赛季
        shoot = NBA[3]  # 投篮
        shootrating = NBA[4]  # 投篮命中
        shootsell = NBA[5]  # 投篮出手
        trisection = NBA[6] # 三分
        trisectionrating = NBA[7]  # 三分命中
        trisectionsell = NBA[8]  # 三分出手
        penaltyshot = NBA[9]  # 罚球
        penaltyshotrating = NBA[10]  # 罚球命中
        penaltyshotsell = NBA[11]  # 罚球出手
        rebound = NBA[12]  # 篮板球
        frontcour = NBA[13]  # 前场
        backcourt = NBA[14]  # 后场
        AssistsAsts = NBA[15]  # 助攻
        StealsStls = NBA[16]  # 抢断
        BlockShotsBlks = NBA[17]  # 盖帽
        TurnOverTOs = NBA[18]  # 失误
        Fouls = NBA[19]  # 犯规
        PointsPTs = NBA[20]  # 得分
        pointsagainst = NBA[21]  # 失分
        victory = NBA[22]  # 胜
        defeat = NBA[23]  # 负
        score = NBA[24]  # 综合得分
        conn = DbConn("localhost", "root", "root", "school_db")
        cursor = conn.DBconnect()
        sql = "insert into nba_t VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (teamid[i],teamname[i],season[i],shoot[i],shootrating[i],shootsell[i],trisection[i],trisectionrating[i],trisectionsell[i],penaltyshot[i],penaltyshotrating[i],penaltyshotsell[i],rebound[i],frontcour[i],backcourt[i],AssistsAsts[i],StealsStls[i],BlockShotsBlks[i],TurnOverTOs[i],Fouls[i],PointsPTs[i],pointsagainst[i],victory[i],defeat[i],score[i])
        conn.Sql(sql)
        conn.commit()
        conn.close()
def Print():
    for v in NBA:
        print(len(v),v)
def func():
    if not myqueue.empty():
        web = urlopen(myqueue.get())
        html = web.read()
        html = html.decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.find("tbody").find_all("tr")
        for v in trs:
            tds = v.find_all("td")
            for i in range(len(tds)):
                NBA[i].append(tds[i].get_text())
def run():
    for k in range(5):
        threading.Thread(target=func(), args=(k,)).start()
if __name__ == '__main__':
    run()
    Pretreatment()
    Print()
    # insertToMysql()