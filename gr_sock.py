#-*- coding: UTF-8 -*- 


import socket
import struct
import matplotlib.pyplot as plt
import numpy as np

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1",8000))

'''
while True:
    info = client.recv(4096)
    print('',info)
'''

#fft config
n=1024
N=1000#积分次数

while True:#总任务
    Z=np.zeros(n)
    for u in range(N):#积分N次
        sample=[]
        for v in range(n):#n个fft点
            I=struct.unpack('f',client.recv(4))[0]
            Q=struct.unpack('f',client.recv(4))[0]
            sample.append(complex(I,Q))  
        Y = np.fft.fftshift(np.fft.fft(sample))/n 
        Y = abs(Y)
        Z = Z + Y

    plt.plot(Z)
    plt.pause(0.05)
    plt.cla()