#coding=utf-8
import pymysql

conn  = pymysql.connect(host='192.168.159.128', user='root', password='123456', db='up')
cursor = conn.cursor()
cursor.execute('insert into stu values (%s,%s)',['3','lixiaoli'])
conn.commit()
cursor.close()
cursor = conn.cursor()
cursor.execute('select * from stu')
value = cursor.fetchall()
print(value)
cursor.close()
conn.close