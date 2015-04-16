__author__ = 'andreas'

def connect_serial(ser):
    buf = []
    while True:
        byte = ser.read()
        if byte == '\n':
            buf = handle_gesture(buf)
        elif byte == '\r':
            pass
        else:
            buf.append(byte)
    ser.close()

def disconnect_serial(ser):
    ser.close()

def handle_gesture(buf):
    #global queue
    print(''.join(buf))
    if buf == 'DOWN':
        color = 255
        print('** ' + str(color))
        #queue.put(color)
    elif buf == 'RIGHT':
        color = 150
        print('** ' + str(color))
        #queue.put(color)
    elif buf == 'UP':
        color = 100
        print('** ' + str(color))
        #queue.put(color)
    elif buf == 'LEFT':
        color = 50
        print('** ' + str(color))
        #queue.put(color)
    else:
        pass
    return []