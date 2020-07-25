import os

def test_venv():
	sh = 'source test_venv/bin/activate\npython -V'
	f = open('test.sh','w')
	f.write(sh)

	os.popen('sh test.sh > test.txt')
	#sh = 'pip list'
	#os.system(sh)
def inti_variant_input(var_list,output_path,jobid):
	f_input = open(output_path+ '/' + jobid + '/' + jobid +'.input','w')
	for i in var_list:
		print(i)
		temp = i.split(':')
		nl = ''
		for col in temp:
			nl += col
			nl += '\t'
		f_input.write(nl[:-1] + '\n')
		




def feature_process(var_list,output_path,jobid,feature_config):
	#test_venv()
	inti_variant_input(var_list,output_path,jobid)



def main():
	print('test')

if __name__ == '__main__':
	main()