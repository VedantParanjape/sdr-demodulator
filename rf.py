from pylab import *
from rtlsdr import *
from scipy.signal import decimate,hilbert
from scipy import sqrt
from numpy import *
from time import time
from itertools import *
import matplotlib.pyplot as plt
from libhackrf import *


def convert_data(extracted_data):
    data = []
    
    for i in extracted_data:
        sub_data = []
        print(len(i)/32)
        for j in range(0,int(len(i)/32)):
            num = int(len(i)/10)
            lower_limit = j*int(len(i)/10)
            upper_limit = (j+1)*int(len(i)/10)

            average = sum(i[lower_limit:upper_limit])/float(num)

            if average < 0.4:
                sub_data.append('0')
            elif average > 0.6:
                sub_data.append('1')
        sub_data.pop(0)
        sub_data.pop(-1)
        sub_data.reverse()
        data.append(sub_data)
    return data
sdr = RtlSdr()

# configure device
sdr.sample_rate = 2e6
sdr.center_freq = 434e6
sdr.gain = 'auto'
sdr.bandwidth = 10e4

samples = sdr.read_samples(256*1024)
fft_s = np.fft.ifft(samples)  
samples_sq = [sqrt(i.real*i.real+i.imag*i.imag) for i in samples]
samples_sq = decimate(samples_sq,50)
timestamp = []

sample_filtered = []
for i in samples_sq:
    if i<0.2:
        sample_filtered.append(int(0))
    elif i>0.8:
        sample_filtered.append(int(1))
    else:
        sample_filtered.append(int(0))
# use matplotlib to estimate and plot the PSD

# psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)

# xlabel('Frequency (MHz)')
# ylabel('Amplitude')

# psd(fft_s, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
# xlabel('Frequency (MHz)')
# ylabel('Amplitude')

# show()
i_prev = 0
extracted_data_starts = []
for i in range(0,len(sample_filtered)-1):
    if sample_filtered[i] > 0.8 and sample_filtered[i+1] < 0.2 and i > i_prev + 345:
        extracted_data_starts.append(i+1)
        i_prev = i
        
print(extracted_data_starts)

timestamp = np.linspace(0,len(samples_sq)*0.5e-6,len(samples_sq))


extracted_data = []
padding= [float(0.5) for i in range(20)]

for i in extracted_data_starts:
    extracted_data.append(sample_filtered[i:i+320])


for i in convert_data(extracted_data):
    print(i)
plt.figure()
# plt.xticks(timestamp, minor=True)
plt.plot(timestamp, samples_sq)
plt.plot(timestamp, sample_filtered)

# for i in extracted_data:
#     plt.figure()
#     plt.plot(i)
plt.show()
