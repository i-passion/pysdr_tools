import time
import numpy as np
import matplotlib.pyplot as plt
from rtlsdr import RtlSdr

def steps_number(freq_goal, frq):
	steps_number = int(round((freq_goal - frq[0]*1e6) / freq_step))
	return steps_number


# configure
I_nums = 1000    #积分次数
filename = 'data'

n=2048					# 单次fft的数据量，
Fs = 2.8e6				# 采样率, 1.4 1.8 1.92 2.048 2.4 2.56 2.8 3.2 MSPS
time_window = 800		# 强度计时间窗口

freq_center = 1420e6	# 中心频率

freq_spectrum_start = 1420.1e6		#频谱显示频率范围
freq_spectrum_stop = 1421.5e6		#


freq_power_start = 1420.1e6			#强度计计算范围
freq_power_stop  = 1420.5e6			#


# Calculate
k = np.arange(n) - n/2 + 0.5
freq_step = Fs/n
frq = (k*freq_step + freq_center) /1e6 # two sides frequency range

freq_spectrum_start_steps_number = steps_number(freq_spectrum_start, frq)
freq_spectrum_stop_steps_number = steps_number(freq_spectrum_stop, frq)
freq_power_start_steps_number = steps_number(freq_power_start, frq)
freq_power_stop_steps_number = steps_number(freq_power_stop, frq)


print("中心频率为： "+str(freq_center/1e6)+"MHz")
print("频率分辨率为： "+str(freq_step)+"Hz")
print("频谱显示范围为： "+str(freq_spectrum_start/1e6)+"Hz——"+str(freq_spectrum_stop/1e6)+"Hz")
print("强度计计算范围为： "+str(freq_power_start/1e6)+"Hz——"+str(freq_power_stop/1e6)+"Hz")



# configure device
sdr = RtlSdr()

sdr.sample_rate = Fs  # Hz
sdr.center_freq = freq_center    # Hz
sdr.gain = 'auto'

sdr.read_samples(512)		#避免闪退
sdr.read_samples(1024)		#避免闪退


fig, ax = plt.subplots(2, 1)
power = [0] * int(time_window)


#-----删除注释，启动文件写入功能-----
#f = open(filename, 'w')
#f.write("New"+"\n")

while True:

	tt=time.time()
	Z=np.zeros(2048)
	for num in range(0,I_nums):

		raw=sdr.read_samples(n)
		#YY = np.fft.fft(raw) # no normalization
		Y = np.fft.fftshift(np.fft.fft(raw))/n # fft computing and normalization
		Y = abs(Y)
		Z=Z+Y

	power_new = np.mean(Z[freq_power_start_steps_number:freq_power_stop_steps_number])
	power = power[1:n]
	power.append(power_new)#1420.1-1420.5MHz

	#-----删除注释，启动文件写入功能-----
	#f.write("$"+" "+str(tt)+" "+str(power_new)+"\n")
	
	#print(str(power_new))

	ax[0].cla()
	ax[1].cla()
	
	ax[0].plot(frq[freq_spectrum_start_steps_number:freq_spectrum_stop_steps_number], Z[freq_spectrum_start_steps_number:freq_spectrum_stop_steps_number], 'B') # plotting the spectrum
	#ax[0].plot(frq,Z,'B')			#全带宽显示
	ax[0].set_xlabel('Freq(MHz)')
	ax[0].set_ylabel('Power')
	#ax[0].set_ylim((0, 0.07))

	ax[1].plot(power, 'G') # plotting the spectrum
	ax[1].set_xlabel('Time')
	ax[1].set_ylabel('Power')
	#ax[1].set_ylim((0, 1))
	#ax[1].grid(True)

	plt.pause(0.01)

