#coding=utf-8

#pip install pandas
#pip install sqlalchemy

import pandas
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:123456@192.168.159.128:3306/up')
data  = pandas.read_sql('select * from stu;',con=engine,)