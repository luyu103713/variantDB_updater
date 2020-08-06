import os
import time

f_root = '/data/Luhy/variantDB/file_result/transfic_result/'
#all_info_unique_transfic_2.tsv
dirs = os.listdir(f_root)
all_count = len(dirs)
count = 0
for filename in dirs:
	sh = 'python uploadFeature.py -c 2 -n transfic_score -i /data/Luhy/variantDB/file_result/transfic_result/' + filename
	#print(sh)
	count += 1
	os.system(sh)
	print(str(count) + ' / ' + str(all_count))
	print(str(time.time()))

