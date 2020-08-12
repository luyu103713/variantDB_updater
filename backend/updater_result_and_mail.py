import os
import re
import sys
import time
from lib import dbconfig
import pymysql
import paramiko
import pandas as pd
def get_sftp():
    hostname=dbconfig.ip 
    username=dbconfig.ssh_user
    password=dbconfig.ssh_passwd 
    port=dbconfig.ssh_port
    t = paramiko.Transport((hostname, port)) 
    t.connect(username=username, password=password) 
    sftp = paramiko.SFTPClient.from_transport(t)

    return sftp
def get_shh():
    hostname=dbconfig.ip 
    username=dbconfig.ssh_user
    password=dbconfig.ssh_passwd 
    port=dbconfig.ssh_port 
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=port, username=username, password=password)    
def walkFile(file):
    file_list = []
    for root, dirs, files in os.walk(file):
        for f in files:
            file_list.append(os.path.join(root, f))
    return file_list
def merge_file(base_df,add_df, begin_base):
	if not begin_base:
		base_df = base_df.merge(add_df,on="index")
	else:		
		base_df = add_df
	return base_df





def transfer_results(jobid):
    result_dir = "./output/" + str(jobid) + "/"
    server_172_dir = "/home/web/public/htdocs/projects/varientDB/static/server_data/" + str(jobid) + "/"
    file_list = walkFile(result_dir)
    begin_base =True
    base_df = None
    print(file_list)
    sftp = get_sftp()
    for file in file_list:
    	file_short_name = file.split('/')[-1]
    	#_out.tsv
    	if file_short_name[-8:] == "_out.tsv":
    		sftp.put(file, server_172_dir + file_short_name)

    		add_df = pd.read_csv(file, sep='\t')
    		base_df = merge_file(base_df,add_df, begin_base)
    		begin_base =False

    all_features_file = "./output/" + str(jobid) + "/" + str(jobid) + "_all_features.tsv"
    base_df.to_csv(all_features_file,sep='\t')

    config_file = "./input_file/"+ str(jobid) + "/" + str(jobid) + ".config"

    sftp.put(config_file, server_172_dir + str(jobid) +".config")
    sftp.put(all_features_file, server_172_dir + str(jobid) +"_all_features.tsv")







if __name__ == '__main__':

    jobid = sys.argv[1]
    transfer_results(jobid)
