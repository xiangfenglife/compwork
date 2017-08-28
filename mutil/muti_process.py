#coding=utf-8

from time import sleep, ctime
import multiprocessing


def super_player(file, time):
    for i in range(2):
        print 'Start playing: %s! %s' % (file, ctime())
        sleep(time)
        #播放的文件与播放时长
list1 = {'AAA.mp3': 3, 'BBB.mp4': 4, 'CCC.mp3': 5}
threads = []
files = range(len(list1))

#创建线程
for file, time in list1.items():
    t = multiprocessing.Process(target=super_player, args=(file, time))
    threads.append(t)

if __name__ == '__main__':
    #启动线程
    for i in files:
        threads[i].start()
    for i in files:
        threads[i].join()
    #主线程
    print 'end:%s' % ctime()
