import matplotlib.pyplot as plt

power=[]
time=[]
flag = 0

f = open('data','r')
f.readline()
line=f.readline()
time0=float(line.split()[1])
while(flag==0):
	line = f.readline()
	if(line!=""):
		time.append(float(line.split()[1])-time0)
		power.append(float(line.split()[2]))
	else:
		flag=1

f.close()


plt.plot(time,power,'B') # plotting the spectrum
plt.xlabel('Time()')
plt.ylabel('Power')
plt.ylim((0, 10))


plt.show()