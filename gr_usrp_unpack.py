import struct
import matplotlib.pyplot as plt
import numpy as np


f=open('3C212off.raw','rb')
n=1024
N=10#积分次数
Z=np.zeros(n)

for i in range(N):
    I=[]
    Q=[]
    for j in range(n):
        I.append(struct.unpack('f',f.read(4))[0])
        Q.append(struct.unpack('f',f.read(4))[0])
    sample=I+Q*j    
    Y = np.fft.fftshift(np.fft.fft(sample))/n 
    Y = abs(Y)
    Z = Z + Y


for i in range(N):
sample=[]
for j in range(n):
    context=f.read(4)
    f.read(4);
    sample.append(struct.unpack('f',context)[0])
Y = np.fft.fftshift(np.fft.fft(sample))/n 
Y = abs(Y)
Z = Z + Y






