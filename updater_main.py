import optparse
import pymysql
import os
from lib import readFile
from features import feature_process



class updater_opt:

    def __init__(self):

        parser = optparse.OptionParser()
        parser.add_option("-i", "--input", dest="input", help="input file(absolute or relative)")
        parser.add_option("-o", "--output", dest="output", help="output file path(absolute or relative)")
        #parser.add_option("-d", "--database", dest="database", help="database name for annotation")
        parser.add_option("-n", "--filename", dest="filename", help="job name or id")
        parser.add_option("-c", "--feature_config", dest="feature_config", help="optional: Custom features calculation")
        parser.add_option("-s", "--split_type", dest="split_type", help="optional:how to split input file.\n t:tab(default)\n c:comma")
        parser.add_option("-t", "--title", dest="title", help="optional:Has title or not.\n 1:no(default)\n 2:yes")



        self.options, self.args = parser.parse_args()
        #print(self.options,self.args)

    def verification(self):
        if not self.options.input or not self.options.output or not self.options.filename:
            exit('ERROR: must support input,output and file id parameters!\nType "python updater.py -h" to seek for help')
def match_config(config_dict):     # Logic of calculation order!!
	normal_methods = ['transvar','annovar','biodbnet','transfic']

	del_list = []
	for k in config_dict:                      #first delete key not right in config
		if k not in normal_methods:
			del_list.append(k)
	for k in del_list:
		config_dict.pop(k)

	for k in config_dict:                       #2nd , if not False,we do it

		if config_dict[k] != 'False':
			config_dict[k] = True
		else:
			config_dict[k] = False

	for k in normal_methods:                 #3rd , the methods not in config, we do it
		if k not in config_dict:
			config_dict[k] = True

	if config_dict['biodbnet']:     # bionetbio rely on transvar 
		config_dict['transvar'] = True
	if config_dict['transfic']:   # tansfic rely on ensgid annovar sorce in dbnsfp
		config_dict['biodbnet'] = True
		config_dict['annovar'] = True
		config_dict['transvar'] = True




	return config_dict
	



def main():
	main_opt = updater_opt()
	main_opt.verification()

	input_file = main_opt.options.input
	output_path = main_opt.options.output
	jobid = main_opt.options.filename

	if not os.path.exists(output_path):
		os.makedirs(output_path)
	if not os.path.exists(output_path+ '/' + jobid):
		os.makedirs(output_path + '/' + jobid)
	if main_opt.options.split_type == 'c':
		split_symbol = ','
	else:
		split_symbol = '\t'
	if main_opt.options.title == '2':
		hasTitle = True
	else:
		hasTitle = False
	#print(main_opt.options.feature_config)
	if main_opt.options.feature_config:
		feature_config = main_opt.options.feature_config
		f_config = open(feature_config,'r')
		ls = f_config.readlines()
		config_dict = {}
		for l in ls:
			l = l.strip()
			temp = l.split(':')
			config_dict[temp[0]] = temp[1]

		config_dict = match_config(config_dict)

	else:
		config_dict = None
		#print(feature_config)

	error_code,error_massage,var_list,file_base_list= readFile.readFileFromInput(input_file,'variant',split_symbol,hasTitle) # now only read variant
	if error_code:
		exit(error_massage)	

	print(var_list)

	feature_process(var_list,output_path,jobid,config_dict)	
	#print()
	#result_dict = collect_result(output_path,jobid)


if __name__ == '__main__':
	main()
