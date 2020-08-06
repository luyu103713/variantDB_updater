from lib import readFile
from lib import annotateLib
from lib import databaseTab

import optparse
import os
import time

class mufa_opt:

    def __init__(self):

        parser = optparse.OptionParser()
        parser.add_option("-i", "--input", dest="input", help="input file(absolute or relative)")
        parser.add_option("-o", "--output", dest="output", help="output file path(absolute or relative)")
        parser.add_option("-d", "--database", dest="database", help="database name for annotation")
        parser.add_option("-n", "--filename", dest="filename", help="optional:job name or id")
        parser.add_option("-t", "--mutation_type", dest="mutation_type", help="optional:annotation type ")
        parser.add_option("-s", "--split_type", dest="split_type", help="optional:how to split input file.\n t:tab(default)\n c:comma")
        parser.add_option("-f", "--from_where", dest="from_where", help="optional: 1: from varinatBD(default) , 2: from Lab MySQL ")



        self.options, self.args = parser.parse_args()
        #print(self.options,self.args)

    def verification(self):
        if not self.options.input or not self.options.output or not self.options.database:
            exit('ERROR: must support input,output and database parameters!\nType "python mufa.py -h" to seek for help')

def match_key_type(database,mutation_type):
	#write this function later,use default only now
	key_type = databaseTab.database_key_default_dict[database]
	return key_type
	#############################################

def main():
	main_opt = mufa_opt()
	main_opt.verification()


	input_file = main_opt.options.input
	output_path = main_opt.options.output
	if output_path[-1] != '/':
		output_path += '/'
	database = main_opt.options.database.lower()

	begin_time = float(time.time())
	if not os.path.exists(output_path):
		os.makedirs(output_path)

	if database.lower() not in databaseTab.databaseList:
		exit('ERROR: database name error or not in the mufa now')

	key_type = match_key_type(database,main_opt.options.mutation_type) # some database can annotate to gene or variant...,mufa allows user to choose one 

	if main_opt.options.split_type == 'c':
		split_symbol = ','
	else:
		split_symbol = '\t'


	if main_opt.options.from_where == '2':
		fromWhere = 'mysql'
	elif main_opt.options.from_where == '3':
		fromWhere = 'data_dict'
	else:
		fromWhere = 'data_tab'

	if main_opt.options.filename:
		job_name = main_opt.options.filename + '_annotation'
	else:
		job_name = 'annotation'

	error_code,error_massage,key_list,new_line_head = readFile.readFileFromInput(input_file,key_type,split_symbol)
	if error_code:
		exit(error_massage)

	annotateLib.annotate_list(key_list,database,key_type,fromWhere,output_path,job_name)
	if main_opt.options.filename:
		print('Job '+main_opt.options.filename+' done!')
	else:
		print('Job done!')
	end_time = float(time.time())

	print('Total annotation time:' + str(end_time - begin_time))




if __name__ == '__main__':
	main()