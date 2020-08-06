import os
import time


def write_v_input(output_path,jobid,basic_v_dict):
	v_input_map_dict = {}
	mufa_v_input_file = output_path+ '/' + jobid + '/mufa/' + jobid + '_mufa_variant.input'
	fw = open(mufa_v_input_file,'w')
	fw.write('index\n')
	for i in range(len(basic_v_dict)):
		info = basic_v_dict[i]
		#10:100008701:G:A
		#{'chr': '7', 'pos': '140453136', 'ref': 'A', 'mut': 'T'}
		row = info['chr'] + ':' + info['pos'] + ':' + info['ref'] + ':' + info['mut'] 
		fw.write(row + '\n')
		v_input_map_dict[row] = i


	fw.close()
	return v_input_map_dict,mufa_v_input_file








def test_mufa(output_path,jobid,basic_v_dict,dbname):
	print('test:')
	mufa_file_root = output_path+ '/' + jobid + '/mufa/'
	if not os.path.exists(mufa_file_root):
		os.makedirs(mufa_file_root)
	v_input_map_dict,mufa_v_input_file = write_v_input(output_path,jobid,basic_v_dict)
	print(v_input_map_dict)

	#sh = python mufa.py -i ./mufa_example/speed_test.tsv -o ./output/ -d transfic_score -n 0806 -f 2
	sh = "python ./mufa/mufa.py -i " + mufa_v_input_file + " -o " + output_path+ '/' + jobid + '/mufa/ -d ' + dbname + " -n " + jobid +" -f 2"
	print(sh)
	sh_root =  output_path+ '/' + jobid + '/mufa/' + jobid + "_mufa.sh"
	f_sh = open(sh_root,'w')
	f_sh.write(sh)
	f_sh.close()

	os.system('sh '+ sh_root)
	time.sleep(0.5)



def main():
	print('This is a shell for mufa')

	
if __name__ == '__main__':
	main()