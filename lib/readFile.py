'''
variant key: chr:position:mutated_from_allele:mutated_to_allele
gene key:gene symbol name
uniprot key: uniprot id
structrue key: PDB:Chain:aa_mutation
'''
import os
def check_file(col_line,key_type,split_symbol):
	check_ok = True
	if key_type == 'variant':
		temp = col_line.split(split_symbol)
		if (temp[0].lower() != 'chr') and (temp[0].lower() != 'chromosome'):
			check_ok = False
		if (temp[1].lower() != 'position'):
			check_ok = False

def get_file_map_list(input_file,key_type,split_symbol,hasTitle):
	f = open(input_file,'r')
	l = f.readline()
	if hasTitle:
		l = f.readline()
	map_key_list = []
	file_base_list =[]
	if not l:
		exit('empty input file!')
	while l:
		
		l = l .strip()
		file_base_list.append(l)

		if key_type == 'variant':
			temp = l.split(split_symbol)
			#print(temp)
			key_name = temp[0] + ':' + temp[1] + ':' + temp[2] + ':' + temp[3]
		elif key_type == 'gene':
			key_name = l
		elif key_type == 'gene-mutaAA':
			temp = l.split(split_symbol)
			key_name =  temp[0] + ':' + temp[1]
		elif key_type == 'uniprot':
			key_name = l
		elif key_type == 'structrue':
			
			temp = l.split(split_symbol)
			key_name = temp[0] + ':' + temp[1] + ':' + temp[2]
		elif key_type == 'index':
			key_name = l
		elif key_type == 'cds':
			#BRAF:c.1799T>A
			temp = l.split(':')
			gene = temp[0]
			if temp[1][0:2] == 'c.':
				info = temp[1][2:]
			else:
				info =temp[1]
			pos = info[:-3]
			ref = info[-3]
			alt = info[-1]
			key_name = gene + ":c." + pos + ref+ ">" + alt
		elif key_type == 'aa':
			#PIK3CA:p.H1047R
			temp = l.split(':')
			gene = temp[0]
			if temp[1][0:2] == 'p.':
				info = temp[1][2:]
			else:
				info =temp[1]
			pos = info[1:-1]
			ref = info[0]
			alt = info[-1]
			key_name = gene + ":p." + ref + pos + alt 
		#elif key_type == 'protein':
			#temp = l.split(':')
			#pdb = temp[0]
		elif key_type == 'hg38':
			temp = l.split(split_symbol)
			#print(temp)
			key_name = temp[0] + ':' + temp[1] + ':' + temp[2] + ':' + temp[3]

		map_key_list.append(key_name)



		l = f.readline()

	f.close()
	return map_key_list,file_base_list





def readFileFromInput(input_file,key_type,split_symbol,hasTitle):
	print('Begin read input file...')
	error_work = False
	error_massage = ''
	map_key_list = []
	file_base_list = []

	key_type_list = ['variant','gene','uniprot','structure','gene-mutaAA','index','cds','aa','hg38']

	if key_type not in key_type_list:
		error_massage = "Annotation key error , please check it!"
		error_work = True
		return error_work,error_massage,map_key_list,file_base_list
	
	if not os.path.exists(input_file):
		error_massage = "Input file not exists , please check it!"
		error_work = True
		return error_work,error_massage,map_key_list,file_base_list
	
	file_size = os.path.getsize(input_file)/float(1024*1024)
	
	if file_size > 2:    # 2M for test version
		error_massage = "Input file too large , the limit is 2M!"
		error_work = True
		return error_work,error_massage,map_key_list,file_base_list


	



	f = open(input_file,'r')
	col_line = f.readline().strip()
	f.close()
	

	# I do not want to check now , do it later
	#check_file_ok,error_massage = check_file(col_line,key_type,split_symbol)
	check_file_ok = True
	##########################################

	if not check_file_ok:
		error_massage = error_massage
		error_work = True
		return error_work,error_massage,map_key_list,file_base_list

	try:
		map_key_list,file_base_list = get_file_map_list(input_file,key_type,split_symbol,hasTitle)
	except:
		error_work =True
		error_massage="input file format error"

	return error_work,error_massage,map_key_list,file_base_list


def main():
	print('test:')

	#return error_code,error_massage,key_list,new_line_head

if __name__ == '__main__':
	main()