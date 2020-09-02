import optparse
import os
import time
def do_2020_plus_process(output_2020_dict):
	






def check_2020_input(input_path):
	file_list = os.listdir(input_path)
	input_filename_dict = {'bed':None,'fasta':None,'mutations':None}
	print(file_list)
	for filename in file_list:
		temp = filename.split('.')
		if temp[-1] == 'bed':
			input_filename_dict['bed'] = input_path + '/' + filename
		elif temp[-1] == 'fa' or temp[-1] == 'fasta':
			input_filename_dict['fasta'] = input_path + '/' + filename
		elif temp[-1] == 'input':
			input_filename_dict['mutations'] = input_path + '/' + filename
	for k in input_filename_dict:
		if not input_filename_dict[k]:
			exit('input error\nprobabilistic2020 process needs:\n1.Mutation Annotation Format (MAF) file\n2.Gene BED file\n3.Gene FASTA\nplease check your input folder')
	return input_filename_dict

def probabilistic2020_process(maf_file,bed_file,fasta_file,output_dir='./',jobid='2020_process'):
	print('job begin')
	sh_root = output_dir + '/' + jobid + '_2020_process.sh'
	sh = 'source /data/Luhy/tools/2020/probabilistic2020_py2/bin/activate\n'
	#probabilistic2020 tsg -i gene_input/job1/snvboxGenes.fa -b gene_input/job1/snvboxGenes.bed -m gene_input/job1/pancreatic_adenocarcinoma.input -c 1.5 -p 10 -o gene_input/job1/tsg_output.txt
	#oncogene
	sh += "probabilistic2020 oncogene -i " +  fasta_file + " -b " + bed_file + " -m " + maf_file + " -c 1.5 -p 10 -o " + output_dir + "/" + jobid + "_oncogene_output.txt\n"
	sh += "probabilistic2020 tsg -i " +  fasta_file + " -b " + bed_file + " -m " + maf_file + " -c 1.5 -p 10 -o " + output_dir + "/" + jobid + "_tsg_output.txt\n"
	sh += "probabilistic2020 hotmaps1d -i " +  fasta_file + " -b " + bed_file + " -m " + maf_file + " -w 3 -c 1.5 -p 10 -o " + output_dir + "/" + jobid + "_hotmaps1d_output.txt\n"
	sh += "mut_annotate --summary -i " +  fasta_file + " -b " + bed_file + " -m " + maf_file + " -n 1 -c 1.5 -p 10 -o " + output_dir + "/" + jobid + "_summary_output.txt\n"
	f_sh = open(sh_root,'w')
	f_sh.write(sh)
	f_sh.close()
	#os.system('sh '+ sh_root)
	time.sleep(0.5)
	output_2020_dict = {'oncogene' : output_dir + "/" + jobid + "_oncogene_output.txt",
						'tsg' : output_dir + "/" + jobid + "_tsg_output.txt",
						'summary' : output_dir + "/" + jobid + "_summary_output.txt",
	} 
	return output_2020_dict
def main():
	print('probabilistic2020 process:\nInput formats:\n1.Mutation Annotation Format (MAF) file\n2.Gene BED file\n3.Gene FASTA')

if __name__ == '__main__':
    main()