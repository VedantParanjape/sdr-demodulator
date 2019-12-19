import serial
import time
ser = serial.Serial('/dev/ttyUSB0',1200,timeout=0)

while True:
    # time.sleep(0.01)  
    print(ser.write(b'\x1f\xaa\x88'))