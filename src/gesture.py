__author__ = 'andreas'

from serial import Serial

def gesture_recognition(q):
    time_out = 3
    baud_rate = 9600
    port = '/dev/cu.usbmodem1411'
    ser = Serial(port, baud_rate, timeout=time_out)
    buf = []
    while True:
        c = ser.read()
        if c == '\n':
            result = ''.join(buf)
            print(result)
            q.put(str(result), block=True, timeout=1)
            buf = []
        elif c == '\r':
            pass
        else:
            buf.append(c)
