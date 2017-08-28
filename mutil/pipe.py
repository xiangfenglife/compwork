#coding:utf-8

import multiprocessing

def proc1(pipe):
    pipe.send('hello')
    print ('proc1 rec:', pipe.recv())

def proc2(pipe):
    pipe.send('hello, too')
    print ('proc2 rec:', pipe.recv())



pipe = multiprocessing.Pipe(duplex=True)

p1 = multiprocessing.Process(target=proc1,args=(pipe[0],))
p2 = multiprocessing.Process(target=proc2,args=(pipe[1],))



p1.start()
p2.start()

p1.join()
p2.join()
