import random
f = open('mufa_test.csv','r')
fw = open('testdb_tab.tsv','w')
ls = f.readlines()
cols = ls[0].strip()
temp = cols.split(',')
for i in temp:
	fw.write(i)
	fw.write('\t')
fw.write('test1\ttest2\n')
for l in ls[1:]:
	check = random.randint(1,10)
	if check < 5:
		temp = l[:-1].split(',')
		for i in temp:
			fw.write(i)
			fw.write('\t')
		if check != 2:
			A = 'A'
		else:
			A = ''
		if check != 3:
			B = 'B'
		else:
			B = ''
		fw.write(A+'\t'+B+'\n')





