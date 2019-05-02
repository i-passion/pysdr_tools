import time
import numpy as np
import matplotlib.pyplot as plt
from rtlsdr import RtlSdr

# configure
n=2048		# fft data number
Fs = 2.8e6  # sampling rate, 1.4 1.8 1.92 2.048 2.4 2.56 2.8 3.2 MSPS
time_window = 1024
freq_center = 434e6
freq_goal = 435.3e6   #   freq_goal - freq_center < Fs/2

freq_step = Fs/n
steps_number = round((freq_goal - freq_center) / freq_step)

sdr = RtlSdr()
# configure device
sdr.sample_rate = Fs  # Hz
sdr.center_freq = freq_center    # Hz
sdr.gain = 'auto'

k = np.arange(n)
frq = k*freq_step + freq_center # two sides frequency range
frq = frq[range(int(n/2))]/1e6 # one side frequency range


fig, ax = plt.subplots(2, 1)
power = [0] * int(time_window)

f = open('data', 'w')

while True:

	tt=time.time()
	raw=sdr.read_samples(n)

	#YY = np.fft.fft(raw) # no normalization
	Y = np.fft.fft(raw)/n # fft computing and normalization
	Y = Y[range(int(n/2))]

	power = power[1:n]
	power.append(abs(Y[steps_number]))
	f.write(str(tt)+" "+str(abs(Y[steps_number]))+"\n")


	ax[0].cla()
	ax[1].cla()
	
	ax[0].plot(frq,abs(Y),'B') # plotting the spectrum
	ax[0].set_xlabel('Freq(MHz)')
	ax[0].set_ylabel('Power')
	ax[0].set_ylim((0, 0.07))

	ax[1].plot(power,'G') # plotting the spectrum
	ax[1].set_xlabel('Time(full_speed_refresh)')
	ax[1].set_ylabel('Power')
	ax[1].set_ylim((0, 0.01))
	#ax[1].grid(True)

	plt.pause(0.01)
