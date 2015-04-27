__author__ = 'andreas'

from serial import Serial

def gesture_recognition(q):
    ser = Serial('/dev/cu.usbmodem1431', 9600)
    buf = []
    while True:
        c = ser.read()
        if c == '\n':
            result = ''.join(buf)
            print(result)
            q.put(('gesture', result), block=True, timeout=1)
            buf = []
        elif c == '\r':
            pass
        else:
            buf.append(c)

def dimming_lights(q):
    ser = Serial('/dev/cu.usbmodem1431', 9600)
    buf = []
    while True:
        c = ser.read()
        if c == '\n':
            result = ''.join(buf)
            #print(result)
            q.put(('dim', result), block=True, timeout=1)
            buf = []
        elif c == '\r':
            pass
        else:
            buf.append(c)

def lighting_levels(q):
    ser = Serial('/dev/cu.usbmodem1431', 9600)
    buf = []
    while True:
        c = ser.read()
        if c == '\n':
            result = ''.join(buf)
            print(result)
            q.put(('lighting', result), block=True, timeout=1)
            buf = []
        elif c == '\r':
            pass
        else:
            buf.append(c)
