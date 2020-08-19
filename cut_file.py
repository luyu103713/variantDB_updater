import time
import numpy as np
import pandas as pd

try:
    import MySQLdb
except:
    import pymysql


try:
    db = MySQLdb.Connect(host="10.20.212.172", user="varientdb", passwd="varient2017", db="varientDB_new")
except:
    db = pymysql.connect(host="10.20.212.172", user="varientdb", passwd="varient2017", db="varientDB_new")
cursor = db.cursor()




def fix_illegal_char(index_dict):

    new_index_dict = {}
    new_index_list = []
    for index in index_dict:
        index_backup = index
        index = index.replace(' ','_')
        index = index.replace('-','_')
        index = index.replace('+','plus')
        new_index_dict[index] = index_dict[index_backup]    
        #new_index_list.append(index)

    return new_index_dict

def get_index_cols_list(f_base,split_mark='\t',clean_col = True):
    f = open(f_base,'r')
    l = f.readline()
    new_index_list = []

    temp = l[:-1].split(split_mark)
    if clean_col:
        for index in temp:
            index = index.replace(' ','_')
            index = index.replace('-','_')
            index = index.replace('+','plus')

            new_index_list.append(index)
    else:
        for index in temp:

            new_index_list.append(index)        
    return new_index_list

def write_info_into_database(base_file,index_dict,index_list,dbname):
    
    sql_col = ''
    for key in index_list:
        l = ' `' + key + '`,'
        sql_col += l
    #print(sql_col)

    f = open(base_file,'r')
    l = f.readline()
    l = f.readline()
    count = 0 
    while l:
        temp = l[:-1].split('\t')
        #temp_dict = {}
        index_dict_temp = dict(zip(index_list , temp))
        #sql = "INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME) VALUES ('Mac', 'Mohan', 20, 'M', 2000)"
        #print(index_dict_temp)
   
        sql_head = "INSERT INTO varientDB_new." + dbname + "(" + sql_col[:-1] + ") VALUES ("
        new_value = ""
        for key in index_list:
            new_value += "'"
            new_value += str(index_dict_temp[key])
            new_value += "',"
        sql = sql_head + new_value[:-1] + ');' 

        #print('sql query: ',sql)
        #try:
        cursor.execute(sql)
        db.commit()


        l = f.readline()


        count +=1 
        if count % 1000 == 0:
            print(str(count)+ ' varientDB_new.' + dbname +' lines write done')
            print(str(int(time.time())))    
            #break  

def get_model_print(index_dict,index_list,max_len=255):
    #CDS_position = models.CharField(db_column='CDS_position', max_length=255, blank=True, null=True)
    print('####################')
    print('####################')
    print('####################')
    ls = []
    for i in index_list:
        l = i + " = models.CharField(db_column='" + i + "', max_length=" + str(max_len) +", blank=True, null=True)"
        ls.append(l)
        print(l)
    print('####################')
    print('####################')
    print('####################')
    return ls


def check_maxi_length(base_file,split_mark='\t'):
    train=pd.read_csv(base_file, sep=split_mark)
    index_dict = get_index_for_cols(base_file)
    more_than_200 = []
    for i in index_dict:
        #print(train[i].head())
        df = train[i]
        len_maxi = df.map(lambda x: len(str(x))).max()
        if len_maxi > 200:
            
            more_than_200.append(i+' : '+str(len_maxi))
        print(i+' : '+str(len_maxi))
    print('####################')
    print('####################')
    print('####################')

    print('more than 200:')
    for s in more_than_200:
        print(s)
    print('####################')
    print('####################')
    print('####################')

def cut_file(base_file,save_file,lines='all',cols='all',split_mark = '\t'):
    if cols == 'all':
        if lines != 'all':
            f_r = open(base_file,'r')
            f_s = open(save_file,'w')
            l = f_r.readline()
            f_s.write(l)


            for i in range(lines):
                l = f_r.readline()
                f_s.write(l)            
        else:
            f_r = open(base_file,'r')
            f_s = open(save_file,'w')
            l = f_r.readline()
            
            while l:
                f_s.write(l)
                l = f_r.readline()
    else:
        
        if lines != 'all':
            index_list = []
            index = 0
            f_r = open(base_file,'r')
            f_s = open(save_file,'w')
            l = f_r.readline()
            temp = l[:-1].split(split_mark)
            for col_name in temp:
                if col_name in cols:
                    index_list.append(index)
                index += 1
            n_l = ''
            for index in index_list:
                n_l += temp[index]
                n_l += split_mark
            n_l = n_l[:-1]+ '\n'
            f_s.write(n_l)
            print(n_l)
            for i in range(lines):
                l = f_r.readline()
                temp = l[:-1].split(split_mark)
                n_l = ''
                for index in index_list:
                    n_l += temp[index]
                    n_l += split_mark
                n_l = n_l[:-1]+ '\n'
                f_s.write(n_l)


        else:
            index_list = []
            index = 0
            f_r = open(base_file,'r')
            f_s = open(save_file,'w')
            l = f_r.readline()
            temp = l[:-1].split(split_mark)
            for col_name in temp:
                if col_name in cols:
                    index_list.append(index)
                index += 1
            n_l = ''
            for index in index_list:
                n_l += temp[index]
                n_l += split_mark
            n_l = n_l[:-1]+ '\n'
            f_s.write(n_l)
            print(n_l)
            l = f_r.readline()    
            while l:
                temp = l[:-1].split(split_mark)
                n_l = ''
                for index in index_list:
                    n_l += temp[index]
                    n_l += split_mark
                n_l = n_l[:-1]+ '\n'
                f_s.write(n_l)
                l = f_r.readline()        

def get_index_for_cols(base_file,cols='all',split_mark = '\t'):

    index_list = []
    index_dict = {}
    index = 0
    f_r = open(base_file,'r')
    l = f_r.readline()
    temp = l[:-1].split(split_mark)
    index_range = range(len(temp))
    index_dict_temp = dict(zip(temp , index_range))
    #print(index_dict_temp)
    if cols != 'all':

        for col_name in cols:
            index_dict[col_name] = index_dict_temp[col_name]
        return index_dict
    else:
        return index_dict_temp
def count_time(func):
    def int_time(*args, **kwargs):
        start_time = time.time()  
        func()
        over_time = time.time() 
        total_time = over_time - start_time
        print('Updater process running : %s s' % total_time)

    return int_time
def main():
    print('welcome')
if __name__ == '__main__':
    main()