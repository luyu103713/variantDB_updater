class at:
	"""docstring for ClassName"""
	def __init__(self, arg):
		self.arg = arg
		

from peewee import *
#from lib import dbconfig

#db = MySQLDatabase("mufa", host=dbconfig.ip, port=dbconfig.port, user=dbconfig.user, passwd=dbconfig.passwd)
#db.connect()


class test01():
    test_col = CharField(unique=True) 


def getORM(dbname):
	#try:
	dbClass = locals()[dbname]
	return dbClass

print(locals().keys())