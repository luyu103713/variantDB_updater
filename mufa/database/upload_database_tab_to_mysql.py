import pymysql
import dbconfig

def testdb():
	db = pymysql.connect(dbconfig.ip,dbconfig.user,dbconfig.passwd,"mufa" )






def main():
	testdb()

if __name__ == '__main__':
	main()