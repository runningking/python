#coding=utf-8
'''
 把DataFrame中的数据导入到mysql中
'''
import pandas
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:123456@192.168.159.128:3306/up')
data = pandas.DataFrame({'id':[3,4,5],'name':['ali','happy','kk']})
data.to_sql('stu',index=False,con=engine,if_exists='append')