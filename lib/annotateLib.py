import os
import pymysql
try:
	import databaseTab 
except:
	from lib import databaseTab
try:
	import configPy
except:

	from lib import configPy
from lib import peeweeORM
from lib import dbconfig

#from configPy import readConfig

def get_datebase_dict(database,fromWhere,key_type):
	database_dict = {}
	config_dict = configPy.readConfig()
	if config_dict['database_dir'] == 'default':
		database_root = './database/'
	elif config_dict['database_dir'] != '':
		if config_dict['database_dir'][-1] != '/':
			database_root = config_dict['database_dir'] + '/'
		else:
			database_root = config_dict['database_dir']
	else:
		database_root = './database/'

	if fromWhere == "data_tab":
		database_file = database_root + database + '_tab.tsv'
		if not os.path.exists(database_file):
			exit('Error:can not find annotation database : ' + database +'. Please type python download_db.py -d ' + database)
		f_tab = open(database_file,'r')
		l = f_tab.readline()
		l = f_tab.readline()
		while l:
			l = l[:-1]
			temp = l.split('\t')
			if key_type == 'variant':
				key_name = temp[0] + ':' + temp[1] + ':' + temp[2] + ':' + temp[3]
				annotation_list = temp[4:]
			elif key_type == 'structure':
				key_name = temp[0] + ':' + temp[1] + ':' + temp[2]
				annotation_list = temp[3:]	
			elif key_type == 'gene-mutaAA':
				key_name = temp[0] + ':' + temp[1] 
				annotation_list = temp[2:]
			else: #gene and uniprot and index mode

				key_name = temp[0]
				annotation_list = temp[1:]	

			if key_name in database_dict:
				database_dict[key_name].append(annotation_list)
			else:

				database_dict[key_name] = [annotation_list]
			
			try:
				l = f_tab.readline()
			except:
				#print(l)
				continue






		return database_dict






	elif fromWhere == "data_dict":
		# code later
		return database_dict

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
def annotate_list(key_list,database,key_type,fromWhere,output_path,job_name):
	error_work = False
	error_massage = ''	

	# code this part later , mysql/dict annotation mode.
	if fromWhere == "mysql":   #mysql mode
		'''
		error_work = True
		error_massage = "mysql/dict annotation mode has not be finished now"
		'''
		try:
			tab_list= testdb()
		except:
			exit('ERROR: cannot connect Mysql, Please check ./lib/dbconfig.py')
		if database not in tab_list:
			exit('ERROR: No table :' + database + ' in Mysql , Please check the database name!')
							
		tab = peeweeORM.getORM(database)


		#for a in tab.select().where(tab.uid == '1').tuples():
		f_result = open(output_path+database+'_' + job_name+'.tsv','w')
		f_result.write(databaseTab.database_head[database])
		row_col_count = len(databaseTab.database_head[database].split('\t'))

		for key_name in key_list:
			if key_name != '':
				keytps = tab.select().where(tab.index == key_name).tuples()
				n_l = ''
				if keytps:
					for tp in keytps:
						for col in tp:
							n_l+= str(col)
							n_l+= '\t'
					f_result.write(n_l[:-1] + '\n')

				else:
					#print(key_name)
					n_l += key_name
					for i in range(row_col_count):
						n_l += '\t'

					f_result.write(n_l[:-1] + '\n')











	elif fromWhere == "data_dict":
		error_work = True
		error_massage = "dict annotation mode has not be finished now"
	################################################


	elif fromWhere == "data_tab":
		print('Processing annotation map.....')
		database_dict = get_datebase_dict(database,fromWhere,key_type)
		#print(database_dict)

		f_result = open(output_path+database+'_' + job_name+'.tsv','w')
		#print('Write result.....')
		f_result.write(databaseTab.database_head[database])
		row_col_count = len(databaseTab.database_head[database].split('\t'))

		for key_name in key_list:
			#if key_type == 'variant':
			temp = key_name.split(':')
			row_col_count = row_col_count - len(temp)

			if key_name in database_dict:
				for result_row in  database_dict[key_name]:
					n_l = ''
					for col in temp:

						n_l += col + '\t'
					for database_result in result_row:
						n_l += database_result + '\t'
					n_l = n_l[:-1] + '\n'
					f_result.write(n_l)
			else:
				n_l = ''
				for col in temp:

					n_l += col + '\t'
				for i in range(row_col_count):
					n_l += '\t'

				n_l = n_l[:-1] + '\n'
				f_result.write(n_l)			

			








if __name__ == '__main__':
	main()