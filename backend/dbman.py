import os
import re
import sys
import time
from lib import dbconfig
import pymysql
from subprocess import call

def print_time():
    print('begin dbman.py')
    localtime = time.asctime( time.localtime(time.time()) )
    print(localtime)

def change_status(jobid, newstatus):
    con = None
    try:
        db = pymysql.connect(dbconfig.ip,dbconfig.user,dbconfig.passwd)
        cur = db.cursor()
        cur.execute("UPDATE varientDB_new.database_job set status= %s where job LIKE %s ", (newstatus, jobid))
        db.commit()
        print("change jobid : " + str(jobid) + " status to " + str(newstatus))
    except:

        print("jobid : "+ jobid + "db error!")
        sys.exit(1)

    finally:

        if db:
            db.close()

def get_new_jobs():
    con = None
    try:
        db = pymysql.connect(dbconfig.ip,dbconfig.user,dbconfig.passwd)

        cur = db.cursor()
        cur.execute("SELECT job,creation_date,job_type,features,order_in_job,chrname,position,ref,alt FROM varientDB_new.database_job,varientDB_new.database_job_details where status = 1 AND database_job.job = database_job_details.job_id;")

        rows = cur.fetchall()

        result_dict = {}
        for row in rows:
            job = row[0]

            change_status(job, 2) # status 2: begin collecting and into quene

            creation_date = row[1]
            job_type = row[2]
            features = row[3]
            order_in_job = row[4]
            chrname = row[5]
            position = row[6]
            ref = row[7]
            alt = row[8]


            if job not in result_dict:
                result_dict[job] = {}
                result_dict[job]['creation_date'] = str(creation_date)
                result_dict[job]['job_type'] = job_type
                result_dict[job]['features'] = features
                result_dict[job]['details'] = {}
                result_dict[job]['details'][order_in_job] = {'chrname':chrname,'position':position,'ref':ref,'alt':alt}
            else:
                result_dict[job]['details'][order_in_job] = {'chrname':chrname,'position':position,'ref':ref,'alt':alt}
                   

            # FOR TESTING ONLY!! added 999 ddg value at the end
            # mylist.append(job+"\t"+pdb_filename+"\t"+partner1+"\t"+partner2+"\t"+chain+"\t"+mutation+"\t"+str(result_id)+"\t"+str(999))

        return result_dict

    except:
        print("db error!")
        sys.exit(1)

    finally:
        if con:
            con.close()    
def create_updater_input(job_dict,jobid):
    #/data/Luhy/tools/variantDB_updater/input_file/
    file_root = "/data/Luhy/tools/variantDB_updater/input_file/" + str(jobid) + '/'
    if not os.path.exists(file_root):
        os.makedirs(file_root)
    out_path = "/data/Luhy/tools/variantDB_updater/output/" + str(jobid) + '/'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    #print(job_dict['features'])
    fw = open(file_root + jobid + '.input','w')
    for i in range(len(job_dict['details'])):
        info = job_dict['details'][i]
        fw.write(info['chrname'] + '\t' + info['position'] + '\t' +info['ref'] + '\t' +info['alt'] + '\n' )
    fw.close()
    f_config = open(file_root + jobid + '.config','w')
    config_list = job_dict['features'].split(';')
    for info in config_list:
        temp = info.split(':')
        if temp[1] == '0':
            f_config.write(temp[0] + ':' + 'False\n')
        else:
            f_config.write(temp[0] + ':' + 'True\n')

    f_config.close()

    #python updater_main.py -i ./example/test02.tsv -o ./output/ -n 20200810 -c config.txt
    f_sh_pwd = file_root + jobid + '_main.sh'
    f_sh = open(f_sh_pwd,'w')
    start_sh = 'echo start:`date +"%Y-%m-%d %H:%M:%S"` >> ./input_file/' + jobid + '/time.log\n'
    end_sh = 'echo end:`date +"%Y-%m-%d %H:%M:%S"` >> ./input_file/' + jobid + '/time.log\n'
    change_status_to_3_sh = "/home/Luhy/anaconda3/bin/python ./backend/change_status_to_3.py " + str(jobid) + '\n'
    updater_main_sh = "/home/Luhy/anaconda3/bin/python updater_main.py -i ./input_file/" + str(jobid) + "/" + str(jobid)+ ".input -o ./output/ -n " \
    + str(jobid) + " -c ./input_file/" +  str(jobid) + "/" + str(jobid) + ".config > ./output/" + str(jobid) + "/" + str(jobid) + "_updater_main_debug.txt\n"
    
    mail_sh = "/home/Luhy/anaconda3/bin/python ./backend/updater_result_and_mail.py " + str(jobid) + ' > ./output/' + str(jobid) + "/" + str(jobid) + "_updater_result_and_mail_debug.txt\n"
    
    f_sh.write(change_status_to_3_sh)
    f_sh.write(start_sh)
    f_sh.write(updater_main_sh)
    f_sh.write(end_sh)
    f_sh.write(mail_sh)


    f_sh.close()
    os.chmod(f_sh_pwd,0o775)
    call("ts sh "+f_sh_pwd, shell=True)
    #os.system("sh " + f_sh_pwd)

def main():
    result_dict = get_new_jobs()
    #print(result_dict)
    print_time()
    for jobid in result_dict:
        create_updater_input(result_dict[jobid],jobid)
        print('job : ' + str(jobid) + ' inputfiles....OK!')


if __name__ == '__main__':
    main()