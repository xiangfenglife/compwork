#coding=utf-8

import threading
from time import ctime, sleep


def player(name, timer):

    for i in range(2):

        print "file name:%s, run time:%s" %(name,ctime())
        sleep(timer)


lst = {'aa.mp3': 3, 'bb.map4': 5, 'cc.mp5': 4}

threads = []

file_num = len(lst)

for name, timer in lst.items():
    t = threading.Thread(target=player, args=(name, timer))
    threads.append(t)


if __name__ == "__main__":

    for i in range(file_num):
        threads[i].start()

    for i in range(file_num):
        threads[i].join()
    print "end:%s" % ctime()

