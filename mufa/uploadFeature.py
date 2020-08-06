import optparse
import pymysql
import os
from lib import dbconfig
from lib import databaseLib

def testdb():
	tab_list = []
	db = pymysql.connect(dbconfig.ip,dbconfig.user,dbconfig.passwd,"mufa" )
	cur = db.cursor()
	cur.execute('SHOW TABLES')	
	tabs = cur.fetchall()
	if len(tabs) != 0:
		for tab in tabs:
			tab_list.append(tab[0])

	return tab_list
class mufa_opt:

    def __init__(self):

        parser = optparse.OptionParser()
        parser.add_option("-i", "--input", dest="input", help="upload database path(absolute or relative)")
        parser.add_option("-n", "--dbname", dest="dbname", help="database name in Mysql")
        parser.add_option("-f", "--force", dest="force", help="optional: 1: insert only (default) , 2: update data")
        parser.add_option("-c", "--create", dest="create", help="optional: 1: DO NOT create new table in Mysql(if database name not in Mysql,default) , 2: create new table in Mysql (if database name not in Mysql)")
        #parser.add_option("-z", "--setting_file", dest="setting_file", help="optional:(if create new table in mysql)")
        parser.add_option("-s", "--split_type", dest="split_type", help="optional:how to split input file.\n t:tab(default)\n c:comma")
        parser.add_option("-t", "--title", dest="title", help="optional:Has title or not.\n 1:no(default)\n 2:yes")


        self.options, self.args = parser.parse_args()
        #print(self.options,self.args)

    def verification(self):
        if not self.options.dbname:
            exit('ERROR: must support database name and pathw parameters!\nType "python uploadFeature.py -h" to seek for help')
def main():
	main_opt = mufa_opt()
	main_opt.verification()

	try:
		tab_list= testdb()
		#print(tab_list)
	except:
		exit('ERROR: cannot connect Mysql, Please check ./lib/dbconfig.py')

	# init args
	if main_opt.options.split_type == 'c':
		split_symbol = ','
	else:
		split_symbol = '\t'

	input_file = main_opt.options.input
	dbname = main_opt.options.dbname
	
	if main_opt.options.force == '2':
		forceUpdata = True
	else:
		forceUpdata = False

	if main_opt.options.create == '2':
		createTab = True
	else:
		createTab = False
	## init done
	if main_opt.options.title == '2':
		hasTitle = True
	else:
		hasTitle = False

	if (dbname not in tab_list) and createTab:
		tab_list.append(dbname)
		print('create ' + dbname+' in database.mufa @' + dbconfig.ip)
		#print('You must code a Peewee ORM setting in ./lib/peeweeORM.py.\nOr mufa will not create tab!\nType "python uploadFeature.py -h" to seek for more help')
		### mysql setting file mode code later ,use default mode
		
		databaseLib.create_table_in_mysql(input_file,dbname)
	if dbname not in tab_list:
		exit('ERROR: database not in Mysql!')
	else:
		if input_file:
			databaseLib.update_data(input_file,dbname,forceUpdata,split_symbol,hasTitle)









if __name__ == '__main__':
	main()