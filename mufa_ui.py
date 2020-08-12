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
def get_gene_muta_dict(output_path,jobid):
	f_transvar = open(output_path+ '/' + jobid + '/' + jobid +'_transvar_out.tsv','r')
	gene_muta_dict = {}
	ls = f_transvar.readlines()
	for l in ls[1:]:
		l = l.strip()
		temp = l.split('\t')
		index = int(temp[0])
		#0	7	140453136	A	T	CCDS5863.1	BRAF	p.V600E
		gene = temp[6]
		if temp[7] != '.':
			muta = temp[7][2:]


		else:
			muta = '.'
		gene_muta_dict[index] =  gene + ':' + muta
	return gene_muta_dict


def check_or_write_gm_input(output_path,jobid):
	f_gm_input_file = output_path+ '/' + jobid + '/mufa/' + jobid + '_mufa_gene_muta.input'
	if os.path.exists(f_gm_input_file):
		gene_muta_dict =  get_gene_muta_dict(output_path,jobid)
		return f_gm_input_file,gene_muta_dict
	else:
		fw = open(f_gm_input_file,'w')
		#symbol,aa_mutation
		fw.write('symbol\taa_mutation\n')
		gene_muta_dict =  get_gene_muta_dict(output_path,jobid)
		for k in gene_muta_dict:
			temp = gene_muta_dict[k].split(':')
			fw.write(temp[0] + '\t' + temp[1] + '\n')
		fw.close()
		return f_gm_input_file,gene_muta_dict
def listToStr(list1):
	s = ''
	for info in list1:
		s += info
		s += '|'
	return s[:-1]


def oncokb_process(output_path,jobid,basic_dict):
	#basic step
	mufa_file_root = output_path+ '/' + jobid + '/mufa/'
	if not os.path.exists(mufa_file_root):
		os.makedirs(mufa_file_root)
	f_gm_input_file,gene_muta_dict = check_or_write_gm_input(output_path,jobid)
	print(gene_muta_dict)
	####
	#python mufa.py -i ./mufa_example/mufa_test.csv -o ./output/ -d oncokb -s c -n test080602
	sh = "python ./mufa/mufa.py -i " + f_gm_input_file + " -o " + output_path+ '/' + jobid + '/mufa/ -d ' + 'oncokb' + " -n " + jobid 

	print(sh)
	sh_root =  output_path+ '/' + jobid + '/mufa/' + jobid + "_oncokb_mufa.sh"
	f_sh = open(sh_root,'w')
	f_sh.write(sh)
	f_sh.close()

	os.system('sh '+ sh_root)
	time.sleep(0.5)

	f_result = output_path+ '/' + jobid + '/mufa/oncokb_' + jobid + "_annotation.tsv"    #oncokb_0209_annotation.tsv
	ls = open(f_result,'r').readlines()
	oncokb_anno_dict = {}
	for l in ls[1:]:
		l = l.strip()
		temp = l.split('\t')
		#gene	aa_muta	oncoKB_id	evidenceType	cancerType	subtype	curatedRefSeq	curatedIsoform	level

		if len(temp) > 5:
			#print(temp)
			gene = temp[0]
			aa_muta = temp[1]
			oncoKB_id = temp[2]
			evidenceType = temp[3]
			cancerType =temp[4]
			subtype = temp[5]
			curatedRefSeq =temp[6]
			curatedIsoform =temp[7]
			level =temp[8]

			gene_muta = gene + ':' + aa_muta

			if gene_muta in oncokb_anno_dict:
				if oncoKB_id not in oncokb_anno_dict[gene_muta]['oncoKB_id']:
					oncokb_anno_dict[gene_muta]['oncoKB_id'].append(oncoKB_id)
					oncokb_anno_dict[gene_muta]['evidenceType'].append(evidenceType)
					oncokb_anno_dict[gene_muta]['cancerType'].append(cancerType)
					oncokb_anno_dict[gene_muta]['subtype'].append(subtype)
					oncokb_anno_dict[gene_muta]['curatedRefSeq'].append(curatedRefSeq)
					oncokb_anno_dict[gene_muta]['curatedIsoform'].append(curatedIsoform)
					oncokb_anno_dict[gene_muta]['level'].append(level)
			else:
				oncokb_anno_dict[gene_muta] = {}
				oncokb_anno_dict[gene_muta]['oncoKB_id'] = [oncoKB_id]
				oncokb_anno_dict[gene_muta]['evidenceType'] = [evidenceType]
				oncokb_anno_dict[gene_muta]['cancerType'] = [cancerType]
				oncokb_anno_dict[gene_muta]['subtype'] = [subtype]
				oncokb_anno_dict[gene_muta]['curatedRefSeq'] = [curatedRefSeq]
				oncokb_anno_dict[gene_muta]['curatedIsoform'] = [curatedIsoform]
				oncokb_anno_dict[gene_muta]['level'] = [level]
	#print(oncokb_anno_dict)

	fw = open(output_path+ '/' + jobid + '/mufa/' + jobid + "_oncokb_out.tsv",'w')

	fw.write("index\tgene\taa_muta\toncoKB_id\tevidenceType\tcancerType\tsubtype\tcuratedRefSeq\tcuratedIsoform\tlevel\n")
	for index in range(len(basic_dict)):
		gene_muta = gene_muta_dict[index]
		temp = gene_muta.split(':')
		gene = temp[0]
		muta = temp[1]
		if gene_muta in oncokb_anno_dict:
			oncoKB_id = oncokb_anno_dict[gene_muta]['oncoKB_id']
			evidenceType = oncokb_anno_dict[gene_muta]['evidenceType']
			cancerType = oncokb_anno_dict[gene_muta]['cancerType']
			subtype = oncokb_anno_dict[gene_muta]['subtype']
			curatedRefSeq = oncokb_anno_dict[gene_muta]['curatedRefSeq']
			curatedIsoform = oncokb_anno_dict[gene_muta]['curatedIsoform']
			level = oncokb_anno_dict[gene_muta]['level']
			nl = str(index) + '\t' + gene + '\t' + muta + '\t' + listToStr(oncoKB_id) + "\t" + listToStr(evidenceType) + "\t" + \
			listToStr(cancerType) + "\t" + listToStr(subtype) + "\t" + listToStr(curatedRefSeq) + "\t" + listToStr(curatedIsoform) + "\t" + listToStr(level) + "\n" 

		else:
			nl = str(index) + '\t' + gene + '\t' + muta + '\t' + '.' + '\t' + '.' + '\t' + '.' + '\t' + '.' + '\t' + '.' + '\t' + '.' + '\t' + '.' + '\n'
		fw.write(nl)
	fw.close()








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