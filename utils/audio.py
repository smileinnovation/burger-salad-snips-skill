import zmq
import time
import sys
from matrix_io.proto.malos.v1 import driver_pb2
from matrix_io.proto.malos.v1 import io_pb2
from multiprocessing import Process
from zmq.eventloop import ioloop
from callbacks import register_data_callback, driver_keep_alive
from mixer import Mixer

matrix_ip = '127.0.0.1'
gpio_port = 20049
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect('tcp://{0}:{1}'.format(matrix_ip, gpio_port))
mixer = Mixer()
audioToggleMute = 0
audioLevelDown = 1
audioLevelUp = 2
mikeToggleMute = 0
decreaseLevel = -2
increaseLevel = 2

def config_gpio_read():
    config = driver_pb2.DriverConfig()
    config.delay_between_updates = 0.1
    config.timeout_after_last_ping = 5
    socket.send(config.SerializeToString())


def gpio_callback(msg):
    data = io_pb2.GpioParams().FromString(msg[0])
    gpioValues = ('{0:016b}'.format(data.values))
    gpioValues = gpioValues[::-1]
    gpioValues = list(gpioValues)
    if gpioValues[audioToggleMute] == '0':
        mixer.toggleOutMute()
    if gpioValues[audioLevelDown] == '0':
        mixer.setVolume(decreaseLevel)
    if gpioValues[audioLevelUp] == '0':
        mixer.setVolume(increaseLevel)
    if gpioValues[mikeToggleMute] == '0':
        mixer.toggleMike()

if __name__ == "__main__":
    ioloop.install()
    Process(target=driver_keep_alive, args=(matrix_ip, gpio_port, 1)).start()
    Process(target=register_data_callback, args=(gpio_callback, matrix_ip, gpio_port)).start()
    config_gpio_read()
