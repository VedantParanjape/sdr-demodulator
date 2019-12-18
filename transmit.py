import serial
import time
ser = serial.Serial('/dev/ttyUSB0',1200,timeout=0)

while True:
    time.sleep(0.05)
    print(ser.write(b'\xff'))