#coding:utf-8
from text9.dbcon import *
import pymysql

conn = DbConn("localhost", "root", "root", "school_db")
cursor = conn.DBconnect()
sql = "select * from film_sy"
conn.Sql(sql)
results = conn.cursor.fetchall()
conn.commit()
conn.close()
file1 = open("D://score.txt","w")
file2 = open("D://num.txt", "w")
for v in results:
    file1.write(str(v[1])+'\n')
    file2.write(str(v[3])+'\n')

