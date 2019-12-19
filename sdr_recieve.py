from pylab import *
from rtlsdr import *
from scipy.signal import decimate
from scipy import sqrt
from numpy import *
from time import time
import matplotlib.pyplot as plt
import binascii

def convert_data(extracted_data):
    data = []
    
    for i in extracted_data:
        sub_data = []
        # print(len(i)/32)

        for j in range(0,int(len(i)/32)):
            num = int(len(i)/10)
            if int(len(i)/32) < 10:
                break
            lower_limit = j*num
            upper_limit = (j+1)*num

            average = sum(i[lower_limit:upper_limit])/float(num)

            if average < 0.4:
                sub_data.append('0')
            elif average > 0.6:
                sub_data.append('1')
        
        if len(sub_data) != 0 and sub_data[0] == '0' and sub_data[-1] == '1':
            sub_data.pop(0)
            sub_data.pop(-1)
            sub_data.reverse()
            data.append(sub_data)
    return data

def read_sample(number_of_samples = 256*1024):
    sdr = RtlSdr()

    # configure device
    sdr.sample_rate = 2e6
    sdr.center_freq = 434e6
    sdr.gain = 'auto'
    sdr.bandwidth = 10e4

    return sdr.read_samples(number_of_samples)


# fft_s = np.fft.ifft(samples)  

def process_samples(samples):
    sample_filtered = []
    i_prev = 0
    extracted_data_starts = []
    extracted_data = []

    samples_sq = [sqrt(i.real*i.real+i.imag*i.imag) for i in samples]
    samples_sq = decimate(samples_sq,50)

    for i in samples_sq:
        if i<0.2:
            sample_filtered.append(int(0))
        elif i>0.8:
            sample_filtered.append(int(1))
        else:
            sample_filtered.append(int(0))

    for i in range(0,len(sample_filtered)-1):
        if sample_filtered[i] > 0.8 and sample_filtered[i+1] < 0.2 and i > i_prev + 325:
            extracted_data_starts.append(i+1)
            i_prev = i

    for i in extracted_data_starts:
        extracted_data.append(sample_filtered[i:i+325])

    return samples_sq, sample_filtered, extracted_data_starts, extracted_data

def plot_waveform(samples_sq, sample_filtered):
    timestamp = []
    
    timestamp = np.linspace(0,len(samples_sq)*0.5e-6,len(samples_sq))
    plt.plot(timestamp, samples_sq)
    plt.plot(timestamp, sample_filtered)
    plt.show()

# def plot_psd(samples, sdr):
#     # use matplotlib to estimate and plot the PSD

#     psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)

#     xlabel('Frequency (MHz)')
#     ylabel('Amplitude')

#     show()
def convert_to_ascii(data):

    text = ''
    binary_array = []

    for i in data:
        temp = ""
        temp = temp.join(i)
        temp = "0b" + temp
        binary_array.append(temp)

    for j in binary_array:
        print (j)

        n = int(j,2)
        text = text + n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

    return text

def main():
    samples = read_sample(256*1024)
    samples_squared, samples_filtered, extracted_data_starts, extracted_data_points = process_samples(samples)

    extracted_data = convert_data(extracted_data_points)
    
    for i in extracted_data:
        print(i)

    print(convert_to_ascii(extracted_data))

    plot_waveform(samples_squared, samples_filtered)

if __name__ == "__main__":
    main()