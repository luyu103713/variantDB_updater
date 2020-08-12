import os
import re
import sys
import time
from lib import dbconfig
import pymysql

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


if __name__ == '__main__':
    jobid = sys.argv[1]
    change_status(jobid,3)
