import os
import time
import datetime


def rename_file(path):
    new_name_lst = []
    for old_name in os.listdir(path):
        if len(old_name) < 29:
            fpath = path + old_name
            st = os.stat(fpath)
            mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime = st
            tmp_t = datetime.datetime.fromtimestamp(mtime)
            format_t = tmp_t.strftime('%Y-%m-%d-%H-%M-%S')
            new_name = path+old_name.split('.')[0]+'_'+format_t+'.'+old_name.split('.')[1]
            new_name_lst.append(new_name)
            os.rename(fpath, new_name)
    return new_name_lst

if __name__ =="__main__":

    path = '/home/xbu/Downloads/log_table/'
    rename_file(path)