# SDR-Demodulator

Implemented Amplitude Shift Keying(ASK) demodulation using rtl-sdr(software defined radio) to captures rf data samples transmitted by a 434 Mhz module. Data is encoded as UART packets and modulated by 434 Mhz module by ASK. It shows a amplitude vs time plot for recieved data, with a normalised graph.

# Usage

`python3 rf_transmit.py`
connect a ftdl module to a 434 Mhz module and use this script to send data. Check port by `ls /dev/tty*`

`python3 sdr_recieve.py [data] [port]`    
connect a rtl-sdr module with appropriate antenna and run this script