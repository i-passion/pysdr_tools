import matplotlib.pyplot as plt

power=[]
flag = 0

f = open('data','r')

while(flag==0):
	line = f.readline()
	if(line!=""):
		power.append(float(line.split()[1]))
	else:
		flag=1

f.close()


plt.plot(power,'B') # plotting the spectrum
plt.xlabel('Time()')
plt.ylabel('Power')
plt.ylim((0, 0.01))


plt.show()