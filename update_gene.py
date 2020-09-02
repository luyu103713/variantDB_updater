import optparse
import pymysql
import os
from cut_file import count_time
from Probabilistic_2020_and_2020_plus import *

class updater_opt:

    def __init__(self):

        parser = optparse.OptionParser()
        parser.add_option("-i", "--input", dest="input", help="input dir(absolute or relative)")
        parser.add_option("-o", "--output", dest="output", help="output file path(absolute or relative)")
        parser.add_option("-m", "--method", dest="method", help="gene scores method")
        parser.add_option("-n", "--filename", dest="filename", help="job name or id")

        self.options, self.args = parser.parse_args()
        #print(self.options,self.args)

    def verification(self):
        if not self.options.input or not self.options.output or not self.options.filename or not self.options.method:
            exit('ERROR: must support input,output and file id parameters!\nType "python updater_gene.py -h" to seek for help')

@count_time
def main():
    main_opt = updater_opt()
    main_opt.verification()

    input_path = main_opt.options.input
    output_path = main_opt.options.output
    jobid = main_opt.options.filename
    method = main_opt.options.method




    if not os.path.exists(output_path):
        os.makedirs(output_path)
    if not os.path.exists(output_path+ '/' + jobid):
        os.makedirs(output_path + '/' + jobid)

    if method == '2020':
    	input_filename_dict = check_2020_input(input_path)
    	#print(input_filename_dict)
    	output_2020_dict = probabilistic2020_process(input_filename_dict['mutations'],input_filename_dict['bed'],input_filename_dict['fasta'],output_path+'/'+jobid,jobid)
    	print(output_2020_dict)
    	do_2020_plus_process(output_2020_dict)



if __name__ == '__main__':
    main()
