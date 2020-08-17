import os
import time
import requests
import json
from cut_file import get_index_for_cols
from lib import readFile
from mufa_ui import *



def test_venv():

	sh = 'source test_venv/bin/activate\npython -V\ndeactivate\npython -V'
	f = open('test.sh','w')
	f.write(sh)


	os.popen('sh test.sh')

	#sh = 'pip list'
	#os.system(sh)
def test_transvar():
	sh = "source /data/Luhy/tools/2020/transvar/bin/activate\ntransvar panno -i 'PIK3CA:p.E545K' --ucsc --ccds"
	sh2 = 'source test_venv/bin/activate\npython -V'
	f = open('test.sh','w')
	f.write(sh)
	f.close()
	os.system('sh test.sh > test.txt')
	#time.sleep(1)
	f2 = open('test2.sh','w')
	f2.write('source test_venv/bin/activate\npip list')
	f2.close()
	os.system('sh test2.sh > test2.txt')
	#os.popen(sh2)

def inti_variant_input(var_list,output_path,jobid):
	basic_dict = {}
	f_input = open(output_path+ '/' + jobid + '/' + jobid +'.input','w')
	job_count = 0
	for i in var_list:
		#print(i)
		temp = i.split(':')
		nl = ''
		for col in temp:
			nl += col
			nl += '\t'
		f_input.write(nl[:-1] + '\n')
		chrom =temp[0]
		pos = temp[1]
		ref = temp[2]
		mut = temp[3]

		basic_dict[job_count] = {'chr' : chrom, 'pos':pos,'ref':ref,'mut':mut}
		job_count += 1
	return basic_dict

def test_ANNOVAR():
	sh = 'perl /data/Luhy/ANNOVAR/annovar/table_annovar.pl example/ex1.avinput humandb/ -buildver hg19 -out output/test -remove -protocol refGene,cytoBand,exac03,avsnp147,dbnsfp30a -operation gx,r,f,f,f -nastring . -csvout -polish -xref example/gene_xref.txt'
	f = open('test.sh','w')
	f.write(sh)
	f.close()
	os.system('sh test.sh > test.txt')
def biodbnet_process(output_path,jobid,basic_dict):
	f_transvar = open(output_path+ '/' + jobid + '/' + jobid +'_transvar_out.tsv','r')
	symbol_dict = {}

	l = f_transvar.readline()
	l = f_transvar.readline()
	while l:
		temp =l.split('\t')
		index = int(temp[0])
		symbol = temp[6]
		#symbol_dict[symbol] = index
		symbol_dict[index] = symbol
		l = f_transvar.readline()
	total_count = len(basic_dict)

	url = "https://biodbnet-abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi.json?method=db2db&input=genesymbol&inputValues="
	for i in range(len(symbol_dict)):
		#https://biodbnet-abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi.json?method=db2db&input=genesymbol&inputValues=TP53,BRAF&outputs=affyid&taxonId=9606
		url += symbol_dict[i]
		url += ','
	url = url[:-1] + "&outputs=ensemblgeneid&taxonId=9606"
	print(url)
	r = requests.get(url)
	text_dict = json.loads(r.text)
	#print(text)
	fw = open(output_path+ '/' + jobid + '/' + jobid +'_ensemblgeneid_out.tsv','w')
	fw.write('index\tsymbol\tensemblgeneid\n')
	write_dict = {}
	for i in range(total_count):
		print(text_dict[str(i)])
		symbol = text_dict[str(i)]['InputValue']
		#index = symbol_dict[symbol]
		index = i
		if text_dict[str(i)]['outputs'] != []:
			ensg = text_dict[str(i)]['outputs']['Ensembl Gene ID'][0]   #use first one
		else:
			ensg = '.'
		write_dict[index] = [symbol,ensg]

	for i in range(total_count):

		nl = str(i) + '\t' + write_dict[i][0] + '\t' + write_dict[i][1] + '\n'
		fw.write(nl)
	fw.close()
	f_transvar.close()
	
def write_candra_input(output_path,jobid,basic_dict):
	index_dict = {}
	f_candra= output_path+ '/' + jobid + '/' + jobid +'_candra.input'
	fw = open(f_candra,'w')
	total_count = len(basic_dict)
	for i in range(total_count):
		#info = basic_dict[i]
		#1	948921	948921	T	C
		nl =  str(basic_dict[i]['chr']) + '\t' + str(basic_dict[i]['pos'])+ '\t' + basic_dict[i]['ref'] + '\t' + basic_dict[i]['mut']+'\t+' + '\n'
		#index_dict[str(basic_dict[i]['chr']) + ':' + str(basic_dict[i]['pos']) + ':' + basic_dict[i]['ref']+ ':' + basic_dict[i]['mut']] = i
		index_dict[i] = str(basic_dict[i]['chr']) + ':' + str(basic_dict[i]['pos']) + ':' + basic_dict[i]['ref']+ ':' + basic_dict[i]['mut']
		fw.write(nl)
	fw.close()
	return f_candra,index_dict 



def write_avinput(output_path,jobid,basic_dict):
	f_avinput = output_path+ '/' + jobid + '/' + jobid +'_annovar.avinput'
	fw = open(f_avinput,'w')
	#fw.write()
	total_count = len(basic_dict)
	for i in range(total_count):
		#info = basic_dict[i]
		#1	948921	948921	T	C
		nl =  str(basic_dict[i]['chr']) + '\t' + str(basic_dict[i]['pos']) + '\t' + str(basic_dict[i]['pos']) + '\t' + basic_dict[i]['ref'] + '\t' + basic_dict[i]['mut'] + '\n'
		fw.write(nl)
	fw.close()
	return f_avinput
def fathmm_cancer(output_path,jobid,basic_dict):
	



def candra_process(output_path,jobid,basic_dict):
	input_file,index_dict = write_candra_input(output_path,jobid,basic_dict)
	output_file = output_path+ '/' + jobid + '/' + jobid +'_candra_result.tsv'
	sh = "perl /data/Luhy/tools/2020/CanDrA/open_candra.pl GENERAL " + input_file + " > " + output_file
	sh_root = output_path+ '/' + jobid + '/' + jobid +'_candra.sh'

	f_sh = open(sh_root,'w')
	f_sh.write(sh)
	f_sh.close()

	os.system('sh '+ sh_root)
	time.sleep(0.5)

	fr = open(output_file,'r')
	fw = open(output_path+ '/' + jobid + '/' + jobid +'_candra_out.tsv','w')
	match_result = {}

	ls = fr.readlines()
	col_name = ls[0]
	fw.write('index\t' + col_name)
	for l in ls[1:]:
		l = l.strip()
		temp = l.split('\t')
		match_index = temp[0] + ':' + temp[1] + ':' + temp[2] + ':' + temp[3]
		match_result[match_index] = l
	for index in index_dict:
		nl = str(index) + '\t'
		if index_dict[index] in match_result:
			nl += match_result[index_dict[index]]
			nl += '\n'
		else:
			temp = index_dict[index].split(':')
			for k in temp:
				nl += k
				nl += '\t'
			nl += '+'
			for i in range(8):
				nl += '\t'
				nl += '.'
			nl += '\n'
		fw.write(nl)
	fw.close()
	fr.close()


def ANNOVAR_process(output_path,jobid,basic_dict):
	has_error = False
	error_type = ''
	
	avinput_file = write_avinput(output_path,jobid,basic_dict)
	sh = "perl /data/Luhy/ANNOVAR/annovar/table_annovar.pl " + avinput_file + " humandb/ -buildver hg19 -out " + output_path+ '/' + jobid + '/' + jobid \
	+ " -remove -protocol exac03,avsnp147,dbnsfp30a -operation f,f,f -nastring . -csvout -polish"
	sh_root = output_path+ '/' + jobid + '/' + jobid +'_annovar.sh'

	f_sh = open(sh_root,'w')
	f_sh.write(sh)
	f_sh.close()

	os.system('sh '+ sh_root)
	time.sleep(0.5)
	#rename annovar output 
	fw = open(output_path+ '/' + jobid + '/' + jobid +'_annovar_out.tsv','w')               
	fbase = open(output_path+ '/' + jobid + '/' + jobid +'.hg19_multianno.csv','r')
	l = fbase.readline()
	nl = 'index'
	temp = l.split(',')
	for col in temp:
		nl += '\t'
		nl += col
	fw.write(nl)
	index = 0
	l = fbase.readline()
	while l:
		nl = str(index)
		temp = l.split(',')
		for col in temp:
			nl += '\t'
			nl += col
		fw.write(nl)		
		index += 1
		l = fbase.readline()
	
	return has_error,error_type
def transvar_g_to_updater_input(gene_hg19_v):
	# chr3:g.178952085A>G -> 3\t178952085\tA\tG\n
	if gene_hg19_v == '.':
		nl = '.\t.\t.\t.\n'
	else:

		temp = gene_hg19_v.split(':g.')
		chrom = temp[0][3:]
		pos = temp[1][:-3]
		ref = temp[1][-3]
		alt = temp[1][-1]
		nl = chrom + '\t' + pos + '\t' + ref + '\t' + alt + '\n'
	return nl




def map_back_to_hg19(input_file,split_symbol,variant_type,hasTitle,output_path,jobid):
	if variant_type in ['aa','cds']:
		print("begin transfer back to hg19,")
		error_code,error_massage,var_list,file_base_list= readFile.readFileFromInput(input_file,variant_type,split_symbol,hasTitle)
		if error_code:
			exit(error_massage)	
		print(var_list)
		sh = "source /data/Luhy/tools/2020/transvar/bin/activate\n"
		total_count = len(var_list)
		f_transvar_pwd = output_path+ '/' + jobid + '/' + jobid+'_'+ variant_type +'_to_hg19.result'

		#transvar canno --ccds -i 'BRAF:c.1799T>A' --ensembl
		#transvar panno -i BRAF:p.V600E --ensembl
		for info in var_list:
			if variant_type == "cds":
				sh_transvar = "transvar canno --ccds -i '" + info + "'\n"
			elif variant_type == "aa":
				sh_transvar = "transvar panno -i '" + info + "' --ensembl\n"
			sh += sh_transvar
		sh_root = output_path+ '/' + jobid + '/' + jobid +'_'+ variant_type +'_to_hg19_transvar.sh'

		
		f_sh = open(sh_root,'w')
		f_sh.write(sh[:-1])
		f_sh.close()
		os.system('sh '+ sh_root + ' > ' + f_transvar_pwd)
		time.sleep(0.5)
		f_out = output_path+ '/' + jobid + '/' + jobid+'_'+ variant_type +'_to_hg19_result.tsv'
		fw = open(f_out,'w')
		f_result = open(f_transvar_pwd,'r')

		transvar_result_dict = {}
		l = f_result.readline()
		#l = f_result.readline()
		result_index = 0
		begin_read = False
		while l:
			#print(l)
			if l[0:5] == 'input':
				begin_read = True
			if l[0:5] != 'input' and begin_read: #cols name, multiple rusult,only read first one!!!  need check!
				
				#print(l[0:4])
				temp = l.split('\t')
				gene_hg19_v = temp[4].split('/')[0]  #chr3:g.178952085A>G

				nl = transvar_g_to_updater_input(gene_hg19_v)  # chr3:g.178952085A>G -> 3\t178952085\tA\tG\n
				fw.write(nl)
				result_index += 1
				begin_read = False

			l = f_result.readline()
		fw.close()


		return f_out
	else:
		return input_file



def transvar_process(output_path,jobid,basic_dict):
	#print(basic_dict)
	#sh = "source /data/Luhy/tools/2020/transvar/bin/activate\ntransvar ganno --ccds -i 'chr3:g.178936091G>A'"
	has_error = False
	error_type = ''
	sh = "source /data/Luhy/tools/2020/transvar/bin/activate\n"
	#{0: {'chr': '7', 'pos': '140453136', 'ref': 'A', 'mut': 'T'}}  # basic dict
	total_count = len(basic_dict)
	fw = open(output_path+ '/' + jobid + '/' + jobid +'_transvar_out.tsv','w')
	fw.write('index\tchr\tposition\tref\talt\ttranscript\tsymbol\taa_change\n')
	for i in range(total_count):
		info = basic_dict[i]
		sh_head = "transvar ganno --ccds -i 'chr"
		temp_sh = sh_head + str(info['chr']) + ':g.' + str(info['pos']) + info['ref'] + '>' + info['mut'] + "'\n"
		sh += temp_sh
	sh_root = output_path+ '/' + jobid + '/' + jobid +'_transvar.sh'
	f_sh = open(sh_root,'w')
	f_sh.write(sh[:-1])
	f_sh.close()
	transvar_result_file = output_path+ '/' + jobid + '/' + jobid +'_transvar.result'
	os.system('sh '+ sh_root + ' > ' + transvar_result_file)
	time.sleep(0.5)
	f_result = open(transvar_result_file,'r')
	transvar_result_dict = {}
	l = f_result.readline()
	#l = f_result.readline()
	result_index = 0
	begin_read = False
	while l:
		#print(l)
		if l[0:5] == 'input':
			begin_read = True
		if l[0:5] != 'input' and begin_read: #cols name, multiple rusult,only read first one!!!  need check!
			
			#print(l[0:4])
			temp = l.split('\t')
			#print(temp)
			transcript = temp[1].split(' (p')[0]
			symbol = temp[2]
			aa_change = temp[4].split('/')[-1]
			print(transcript,symbol,aa_change)
			nl = str(result_index) + '\t' + str(basic_dict[result_index]['chr']) + '\t' + str(basic_dict[result_index]['pos']) + '\t' + basic_dict[result_index]['ref'] + '\t' + basic_dict[result_index]['mut'] + '\t' + \
			transcript + '\t' +  symbol + '\t' +  aa_change + '\n'
			fw.write(nl)
			result_index += 1
			begin_read = False

		l = f_result.readline()
	fw.close()
	return has_error,error_type
def write_transfic_base(output_path,jobid,basic_dict):
	transfic_big_dict = {} #all info in it!
	ensembl_file = output_path+ '/' + jobid + '/' + jobid +'_ensemblgeneid_out.tsv'
	av_file = output_path+ '/' + jobid + '/' + jobid +'_annovar_out.tsv'

	fw = open(output_path+ '/' + jobid + '/' + jobid +'_transfic_base.tsv','w')

	av_index_dict = get_index_for_cols(av_file,cols='all',split_mark = '\t')
	#print(av_index_dict)
	f_av = open(av_file,'r')
	ls = f_av.readlines()

	for l in ls[1:]:
		l = l.strip()
		temp = l.split('\t')
		index = int(temp[0])
		sift = temp[av_index_dict['SIFT_score']]
		p2 = temp[av_index_dict['Polyphen2_HDIV_score']]
		ma = temp[av_index_dict['MutationAssessor_score']]		
		if sift == '.':
			sift = '0.001'
			sift_dummy = True
		else:
			sift_dummy = False
		if p2 == '.':
			p2 = '0.971'
			p2_dummy = True
		else:
			p2_dummy = False		
		if ma == '.':
			ma = '1.32'
			ma_dummy = True
		else:
			ma_dummy = False
		transfic_big_dict[index] = {'sift':sift,'sift_dummy':sift_dummy,'p2':p2,'p2_dummy':p2_dummy,'ma':ma,'ma_dummy':ma_dummy}

	f_av.close()

	f_ensmbl = open(ensembl_file,'r')
	ls = f_ensmbl.readlines()
	for l in ls[1:]:
		l = l.strip()
		temp = l.split('\t')
		index = int(temp[0])
		ensg = temp[2]
		if ensg == '.':
			ensg = 'ENSG99999999999'
			ensg_dummy = True
		else:
			ensg_dummy = False		
		transfic_big_dict[index]['ensg'] = ensg
		transfic_big_dict[index]['ensg_dummy'] = ensg_dummy
	f_ensmbl.close()

	for index in range(len(basic_dict)):
		fw.write( str(index)+'\t' +transfic_big_dict[index]['ensg'] + '\t' +transfic_big_dict[index]['sift'] + '\t' + transfic_big_dict[index]['p2'] + '\t' + transfic_big_dict[index]['ma'] + '\n')



	fw.close()

	return output_path+ '/' + jobid + '/' + jobid +'_transfic_base.tsv',transfic_big_dict

def transfic_process(output_path,jobid,basic_dict):
	f_transfic_base,transfic_big_dict = write_transfic_base(output_path,jobid,basic_dict)
	#print(transfic_big_dict)
	sh = "perl  ./transf_scores.pl gosmf " + f_transfic_base + ' ' + output_path+ '/' + jobid + '/' + jobid +'_transfic_result.txt'
	sh_root = output_path+ '/' + jobid + '/' + jobid +'_transfic_main.sh'
	f_sh = open(sh_root,'w')
	f_sh.write(sh)
	f_sh.close()

	os.system('sh '+ sh_root)
	time.sleep(0.5)
	fw = open(output_path+ '/' + jobid + '/' + jobid +'_transfic_out.tsv','w')
	fw.write('index\tensg\tSIFT_transfic_score\tSIFT_transfic_pred\tPolyphen2_transfic_score\tPolyphen2_transfic_pred\tMutationAssessor_transfic_score\tMutationAssessor_transfic_pred\n')

	f_result = open(output_path+ '/' + jobid + '/' + jobid +'_transfic_result.txt','r')
	ls = f_result.readlines()
	result_dict = {}
	for l in ls:
		l = l.strip()
		temp = l.split('\t')
		index = int(temp[0])	
		result_dict[index] = temp[1:]
	for index in range(len(basic_dict)):
		#{'sift': '0.001', 'sift_dummy': False, 'p2': '0.971', 'p2_dummy': False, 'ma': '1.32', 'ma_dummy': False, 'ensg': 'ENSG00000157764', 'ensg_dummy': False}
		nl = str(index)
		info = transfic_big_dict[index]

		if index in result_dict:
			if info['ensg_dummy']:
				ensg = '.'
			else:
				ensg = transfic_big_dict[index]['ensg']
			if info['sift_dummy']:
				sift_tr = '.'
				sift_p_tr = '.'
			else:
				sift_tr = result_dict[index][1]
				sift_p_tr = result_dict[index][2]
			if info['p2_dummy']:
				p2_tr = '.'
				p2_p_tr = '.'
			else:
				p2_tr = result_dict[index][3]
				p2_p_tr = result_dict[index][4]				
			if info['ma_dummy']:
				ma_tr = '.'
				ma_p_tr = '.'
			else:
				ma_tr = result_dict[index][5]
				ma_p_tr = result_dict[index][6]		
		else:
			if info['ensg_dummy']:
				ensg = '.'
			else:
				ensg = transfic_big_dict[index]['ensg']
			sift_tr = '.'
			sift_p_tr = '.'			
			p2_tr = '.'
			p2_p_tr = '.'
			ma_tr = '.'
			ma_p_tr = '.'

		nl = nl + '\t' + ensg + '\t' + sift_tr + '\t' + sift_p_tr + '\t' + p2_tr + '\t' + p2_p_tr + '\t' + ma_tr + '\t' + ma_p_tr + '\n'
		fw.write(nl)
	fw.close()
	f_result.close()



def feature_process(var_list,output_path,jobid,config_dict=None):
	#test_venv()
	basic_dict = inti_variant_input(var_list,output_path,jobid)
	print(config_dict)

	#print(basic_dict)
	if not config_dict:
		has_error,error_type = transvar_process(output_path,jobid,basic_dict)
		if has_error:
			exit(error_type)
		has_error,error_type = ANNOVAR_process(output_path,jobid,basic_dict)
		if has_error:
			exit(error_type)
		candra_process(output_path,jobid,basic_dict)
		fathmm_cancer(output_path,jobid,basic_dict)
		biodbnet_process(output_path,jobid,basic_dict)
		transfic_process(output_path,jobid,basic_dict)
		oncokb_process(output_path,jobid,basic_dict)
	else:  # use config_dict
		if config_dict['transvar']:
			has_error,error_type = transvar_process(output_path,jobid,basic_dict)
			if has_error:
				exit(error_type)
		if config_dict['annovar']:			
			has_error,error_type = ANNOVAR_process(output_path,jobid,basic_dict)
			if has_error:
				exit(error_type)
		if config_dict['candra']:
			candra_process(output_path,jobid,basic_dict)
		if config_dict['fathmm_cancer']:
			fathmm_cancer(output_path,jobid,basic_dict)
		if config_dict['biodbnet']:
			biodbnet_process(output_path,jobid,basic_dict)
		if config_dict['transfic']:
			transfic_process(output_path,jobid,basic_dict)
		if config_dict['oncokb']:
			oncokb_process(output_path,jobid,basic_dict)





def main():

	#test_transvar()
	#test_ANNOVAR()
	#transfic_process('./output/','0103',{0: {'chr': '7', 'pos': '140453136', 'ref': 'A', 'mut': 'T'}, 1: {'chr': '3', 'pos': '178936091', 'ref': 'G', 'mut': 'A'}, 2: {'chr': '5', 'pos': '2131234', 'ref': 'G', 'mut': 'A'}})
	test_mufa('./output/','0202',{0: {'chr': '7', 'pos': '140453136', 'ref': 'A', 'mut': 'T'}, 1: {'chr': '3', 'pos': '178936091', 'ref': 'G', 'mut': 'A'}, \
		2: {'chr': '5', 'pos': '2131234', 'ref': 'G', 'mut': 'A'}, 3: {'chr': '17', 'pos': '7577121', 'ref': 'G', 'mut': 'A'}},'transfic_score')


if __name__ == '__main__':
	main()