import numpy as np
import matplotlib.pyplot as plt
from rtlsdr import RtlSdr


sdr = RtlSdr()
# configure device
sdr.sample_rate = 2.8e6  # Hz
sdr.center_freq = 434e6    # Hz
sdr.gain = 'auto'

n=2048

Fs = sdr.sample_rate; # sampling rate采样率
freq_center = sdr.center_freq
freq_step = Fs/n

k = np.arange(n)
frq = k*freq_step + freq_center # two sides frequency range
frq = frq[range(int(n/2))]/1e6 # one side frequency range


fig, ax = plt.subplots(2, 1)
power = [0] * int(n/2)

while True:
	raw=sdr.read_samples(n)

	#YY = np.fft.fft(raw) # no normalization
	Y = np.fft.fft(raw)/n # fft computing and normalization
	Y = Y[range(int(n/2))]

	power = power[1:n]
	power.append(abs(Y[292]))#0.4MHz

	ax[0].cla()
	ax[1].cla()
	
	ax[0].plot(frq,abs(Y),'B') # plotting the spectrum
	ax[0].set_xlabel('Freq(MHz)')
	ax[0].set_ylabel('Power')
	ax[0].set_ylim((0, 0.07))

	ax[1].plot(power,'G') # plotting the spectrum
	ax[1].set_xlabel('Time(s)')
	ax[1].set_ylabel('Power')
	ax[1].set_ylim((-0.003, 0.015))
	#ax[1].grid(True)

	plt.pause(0.01)
