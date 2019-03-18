import zmq
import time
import sys
from led import set_led, Leds
from LedRunner import LedRunner
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
mikeToggleMute = 3
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
        _matrix = Leds()
    _runner = LedRunner()
    gpioValues = list(gpioValues)
    global reset
    if gpioValues[audioToggleMute] == '0' and reset == True:
        mixer.toggleOutMute()
        reset = False
    elif gpioValues[audioLevelDown] == '0' and reset == True:
        mixer.setVolume(decreaseLevel)
        reset = False
        _runner.once(_matrix.clear)
        _runner.once(_matrix.volume, int((18/100)*(mixer._outLevel+decreaseLevel)))
        _runner.once(_matrix.clear)  
    elif gpioValues[audioLevelUp] == '0' and reset == True:
        mixer.setVolume(increaseLevel)
        reset = False
        _runner.once(_matrix.clear)  
        _runner.once(_matrix.volume, int((18/100)*(mixer._outLevel+increaseLevel)))
        _runner.once(_matrix.clear)  
    elif gpioValues[mikeToggleMute] == '0' and reset == True:
        reset = False
        mixer.toggleMike()
    elif gpioValues[audioToggleMute] == '1' and gpioValues[audioLevelDown] == '1' and gpioValues[audioLevelUp] == '1' and gpioValues[mikeToggleMute] == '1':
        reset = True

    
if __name__ == "__main__":
    ioloop.install()
    reset = False
    Process(target=driver_keep_alive, args=(matrix_ip, gpio_port, 1)).start()
    Process(target=register_data_callback, args=(gpio_callback, matrix_ip, gpio_port)).start()
    config_gpio_read()
