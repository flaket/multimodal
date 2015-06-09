__author__ = 'andreas'

import serial_input
import csv
import matplotlib.pyplot as plt
import numpy as np
import random as r
from sklearn import preprocessing, svm, cross_validation
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier, BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
import Queue
from threading import Thread
import time
import math

def create_labels(y, samples_per_label):
    for n in range(42):
        y.extend([str(n)]*samples_per_label)

def std_dev(lst):
    n = len(lst)
    c = sum(lst) / n
    s = sum((x-c)**2 for x in lst)
    return math.sqrt(s / (n-1))

def confidence(o):
    return 1.96 * (o / math.sqrt(loops))

def classify():
    if len(X) == len(y):
        results = []
        svc_lin_score = []
        svc_score = []
        logisticRegression_score = []

        for i in range(loops):
            seed = r.randint(0, len(X))
            X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.25, random_state=seed)

            svc_lin = svm.LinearSVC().fit(X_train, y_train)
            svc_lin_score.append(svc_lin.score(X_test, y_test))

            svc = svm.SVC(kernel='linear').fit(X_train, y_train)
            svc_score.append(svc.score(X_test, y_test))

            logisticRegression = LogisticRegression().fit(X_train, y_train)
            logisticRegression_score.append(logisticRegression.score(X_test, y_test))


        svclin_std_dev = std_dev(svc_lin_score)
        svclin_avg = sum(svc_lin_score) / loops
        svclin_conf = confidence(svclin_std_dev)

        svc_std_dev = std_dev(svc_score)
        svc_avg = sum(svc_score) / loops
        svc_conf = confidence(svc_std_dev)

        logres_std_dev = std_dev(logisticRegression_score)
        logres_avg = sum(logisticRegression_score) / loops
        logres_conf = confidence(logres_std_dev)

        results.append(["Linear-SVC", svclin_avg, svclin_conf])
        results.append(["SVC", svc_avg, svc_conf])
        results.append(["LogisticRegression", logres_avg, logres_conf])

        results.sort(reverse=True)
        return results
    return "Mismatch in #data samples in data set X and #labels in y"

def test_trim_data():
    assert [1., 1., 1.] == trim_data([1., 1., 1.], n=3, m=1)
    assert [1., 0., 0.] == trim_data([1.], n=3, m=1)
    assert [1., 0., 0., 1., 0., 0., 1., 0., 0., 0.] == trim_data([1., 1., 1.], n=10, m=1)
    assert [0.5, 0.5, 0.5] == trim_data([1., 1., 1.], n=3, m=2)
    assert [0.1, 0.1, 0.1] == trim_data([1., 1., 1.], n=3, m=10)
    assert [.2, 0., 0., .2, 0., 0., .2, 0., 0., 0.] == trim_data([1., 1., 1.], n=10, m=5)
    assert [1., 1., 1.] == trim_data([1., 1., 1., 1., 1., 1.], n=3, m=1)
    assert [.5, .5, .5] == trim_data([.25, .75, .25, .75, .25, .75], n=3, m=1)

def serial_data_to_q(id, port, q):
    ser = serial_input.Serial(port, baud_rate, timeout=time_out)
    buf = []
    while True:
        c = ser.read()
        if c == '\n':
            result = ''.join(buf)
            q.put((id,result), block=True, timeout=1)
            buf = []
        elif c == '\r':
            pass
        else:
            buf.append(c)

def record_gestures():
    # Spin up a thread for each serial port with a common queue for them to write to.
    start_thread(serial_data_to_q, args=(1, '/dev/cu.usbmodem1a1211', serial_q))
    start_thread(serial_data_to_q, args=(2, '/dev/cu.usbmodem1a1221', serial_q))
    start_thread(serial_data_to_q, args=(3, '/dev/cu.usbmodem1a1231', serial_q))
    start_thread(serial_data_to_q, args=(4, '/dev/cu.usbmodem1a1241', serial_q))

    time.sleep(1)
    for i in range(0, samples):
        q_data = []
        one = []
        two = []
        three = []
        four = []
        print("Listening for gesture for " + str(time_out) + " seconds..")
        time.sleep(time_out)
         # Look for new data in the queue. Break and process data when queue is empty.
        while True:
            try:
                d = serial_q.get_nowait()
                # sort the data from the four sources:
                if d[0] == 1:
                    list_of_data = process_data(d[1])
                    one.extend(sort_data(list_of_data))
                elif d[0] == 2:
                    list_of_data = process_data(d[1])
                    two.extend(sort_data(list_of_data))
                elif d[0] == 3:
                    list_of_data = process_data(d[1])
                    three.extend(sort_data(list_of_data))
                elif d[0] == 4:
                    list_of_data = process_data(d[1])
                    four.extend(sort_data(list_of_data))
                else:
                    pass
            except Queue.Empty:
                break
        if len(one) < 1:
            one = [0.0] * 128
        else:
            one = trim_data(one)
        if len(two) < 1:
            two = [0.0] * 128
        else:
            two = trim_data(two)
        if len(three) < 1:
            three = [0.0] * 128
        else:
            three = trim_data(three)
        if len(four) < 1:
            four = [0.0] * 128
        else:
            four = trim_data(four)
        three.extend(four)
        two.extend(three)
        one.extend(two)
        store_to_memory(one, i)

def sort_data(list_of_data):
    # sort data from the four photo diodes:
    sensor1 = []
    sensor2 = []
    sensor3 = []
    sensor4 = []
    for j in range(0, len(list_of_data), 4):
        sensor1.append(list_of_data[j+0])
        sensor2.append(list_of_data[j+1])
        sensor3.append(list_of_data[j+2])
        sensor4.append(list_of_data[j+3])
    sensor3.extend(sensor4)
    sensor2.extend(sensor3)
    sensor1.extend(sensor2)
    sensor1 = map(float, sensor1)
    return sensor1

def process_data(raw):
    d = raw.decode()
    d = d.split(' ')
    del d[-1]
    d = list(map(int, d))
    return d

def trim_data(d, n=128, m=255):
    """
    Partitions an input array of data into a feature vector of size n:
    an n-sized array with normalized values with regard to m.
    If the input data is of a shorter length than n the returned array will be sparse.
    A larger input array will produce a denser result.
    :param d: Input array of data.
    :param n: Size of result array.
    :param m: Normalizing factor (maximum possible data value).
    :return: Array of size param n with input param data distributed over the array
             and normalized with regard to param m.
    """
    l = len(d)
    histogram = [0] * n
    s = int(l / n)
    if s == 0:
        s = int(1. / (float(l) / float(n)))
        for i, x in enumerate(d):
            histogram[i*s] = x/m
    else:
        for i in range(0, n):
            histogram[i] = sum(d[i*s:(i+1)*s])/(m*s)
    return histogram

def online_classify(d):
    prediction = svc.predict(d)
    print(prediction)

def store_to_memory(sensor1, n):
    data.append(sensor1)
    print("Stored result to memory: {0}".format(str(n + 1)))

def save_data():
    with open(output_filename, 'wb') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(data)
    print("Stored " + str(len(data)) + " data samples to file: " + output_filename)

def train_classifier():
    create_labels()
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.25)
    global svc
    svc = svm.SVC(kernel='linear').fit(X_train, y_train)

def start_thread(fn, args):
    worker = Thread(target=fn, args=args)
    worker.setDaemon(True)
    worker.start()


if __name__ == '__main__':
    #'''
    X = np.loadtxt('data/42-10.csv', delimiter=',')
    X = preprocessing.scale(X)
    y = []
    samples_per_label = 10
    loops = 100

    create_labels(y, samples_per_label)
    #print(len(X))
    #print(len(y))
    r = classify()
    print(r)
    #'''

    '''
    time_out = 3
    baud_rate = 9600
    data = []
    samples = 10
    output_filename = 'data/sw-fast-10.csv'
    serial_q = Queue.Queue()

    record_gestures()
    save_data()
    '''