from peewee import *
from lib import peeweeORM
from lib import dbconfig
import pymysql
import time


def create_table_in_mysql(input_file,dbname):

	tab = peeweeORM.getORM(dbname)
	
	tab.create_table()



def update_data(input_file,dbname,forceUpdata,split_type,hasTitle):

	#tab = peeweeORM.getORM(dbname)
	f = open(input_file,'r')
	db = pymysql.connect(dbconfig.ip,dbconfig.user,dbconfig.passwd,"mufa" )
	cursor = db.cursor()
	l = f.readline()
	if hasTitle:
		l = f.readline()
	print('Begin update database : ' + dbname)
	if forceUpdata:
		print('Update strategy : force override')
	else:
		print('Update strategy : ignore duplicate rows')
	count = 0
	while l:

		temp = l[:-1].split(split_type)
		#print(temp)
		if l[:-1] != "":
			if forceUpdata:
				myQuery = "REPLACE INTO mufa.`" + dbname + "` VALUES(" 
				for i in temp:
					myQuery += "'"
					myQuery += str(i)
					myQuery += "',"
				myQuery = myQuery[:-1] + ");"
				#print(myQuery) 
				cursor.execute(myQuery)
				db.commit()
			else:
				myQuery = "INSERT IGNORE INTO mufa.`" + dbname + "` VALUES(" 
				for i in temp:
					myQuery += "'"
					myQuery += str(i)
					myQuery += "',"
				myQuery = myQuery[:-1] + ");"
				#print(myQuery) 
				cursor.execute(myQuery)
				db.commit()		
		count += 1
		if count % 10000 == 0:
			print(str(count))
			print(str(time.time()))

		l = f.readline()
		
	db.close()







