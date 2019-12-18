import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy#use numpy for buffers
import matplotlib.pyplot as plt
from scipy.signal import decimate,hilbert
from scipy import sqrt

#create device instance
#args can be user defined or from the enumeration result
args = dict(driver="rtlsdr")
sdr = SoapySDR.Device(args)

#apply settings
sdr.setSampleRate(SOAPY_SDR_RX, 0, 1e6)
sdr.setFrequency(SOAPY_SDR_RX, 0, 434e6)
# sdr.setGain('auto')
sdr.setBandwidth(SOAPY_SDR_RX, 0, 1e6)

#setup a stream (complex floats)
rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
sdr.activateStream(rxStream) #start streaming

#create a re-usable buffer for rx samples
buff = numpy.array([0]*1024*256, numpy.complex64)

#receive some samples
sr = sdr.readStream(rxStream, [buff], len(buff))
print(buff[0], buff[100], buff[200] ,buff[2000])
samples_sq = [sqrt(i.real*i.real+i.imag*i.imag) for i in buff]
samples_sq = decimate(samples_sq,50)

sample_filtered = []
for i in samples_sq:
    if i<0.2:
        sample_filtered.append(int(0))
    elif i>0.4:
        sample_filtered.append(float(0.6))
    else:
        sample_filtered.append(int(0))

extracted_data_starts = []
for i in range(0,len(sample_filtered)):
    if sample_filtered[i] > 0.4 and sample_filtered[i+1] < 0.2:
        extracted_data_starts.append(i)
        
print(extracted_data_starts)

timestamp = numpy.linspace(0,len(samples_sq)*10e-6,len(samples_sq))
plt.figure()
plt.xticks(timestamp)
plt.plot(timestamp, samples_sq)
plt.plot(timestamp, sample_filtered)
plt.show()

#shutdown the stream
sdr.deactivateStream(rxStream) #stop streaming
sdr.closeStream(rxStream)