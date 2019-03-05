import os
import zmq
import time
import sys
from matrix_io.proto.malos.v1 import driver_pb2
from matrix_io.proto.malos.v1 import io_pb2
from multiprocessing import Process
from zmq.eventloop import ioloop
from utils import driver_keep_alive, register_data_callback, register_error_callback
from mixer import Mixer

matrix_ip = '127.0.0.1'
gpio_port = 20049
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect('tcp://{0}:{1}'.format(matrix_ip, gpio_port))

def gpio_callback(msg):
    data = io_pb2.GpioParams().FromString(msg[0])
    gpioValues = ('{0:016b}'.format(data.values))
    gpioValues = gpioValues[::-1]
    gpioValues = list(gpioValues)
    #Set volume here
    if gpioValues[0] == '0':
        print("Mute")
    print('GPIO PINS-->[0-15]\n{0}'.format(gpioValues))

if __name__ == "__main__":
    ioloop.install()
    Process(target=register_data_callback, args=(gpio_callback, matrix_ip, gpio_port)).start()
