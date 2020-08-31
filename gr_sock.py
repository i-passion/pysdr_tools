#-*- coding: UTF-8 -*- 
import socket
import struct
import matplotlib.pyplot as plt
import numpy as np
import time
from multiprocessing import Process,Pipe

#fft config
n=1024
N=10#积分次数

parent_conn, child_conn = Pipe()

def info_get():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1",8000))
    while True:
        parent_conn.send(client.recv(8))
        print("done,recv:")
        print(child_conn.recv())
        time.sleep(1)

def dsp(n,N):
    #while True:#总任务
    Z=np.zeros(n)
    for u in range(N):#积分N次
        sample=[]
        for v in range(n):#n个fft点
            print("2")
            info = child_conn.recv()
            print("3")
            I=struct.unpack('f',info[0:4])[0]
            Q=struct.unpack('f',info[4:8])[0]
            sample.append(complex(I,Q))  
        Y = np.fft.fftshift(np.fft.fft(sample))/n 
        Y = abs(Y)
        Z = Z + Y
    plt.plot(Z)
    plt.ylim(0, 0.0003)
    plt.pause(0.01)
    plt.cla()


if __name__ == '__main__':
     a = Process(target=info_get, args=())
     #b = Process(target=dsp, args=(n,N))
     #c = Process(target=draw, args=())
     a.start()
     #b.start()
     a.join()
     #b.join()
