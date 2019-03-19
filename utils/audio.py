import zmq
import time
import sys
from matrix_io.proto.malos.v1 import driver_pb2
from matrix_io.proto.malos.v1 import io_pb2
from multiprocessing import Process
from zmq.eventloop import ioloop
from callbacks import register_data_callback, driver_keep_alive
from mixer import Mixer
from led import set_led, Leds
from LedRunner import LedRunner

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

_runner = LedRunner()
reset = True
toggleMic = True
toggleOut = True

def gpio_callback(msg):
    data = io_pb2.GpioParams().FromString(msg[0])
    gpioValues = ('{0:016b}'.format(data.values))
    gpioValues = gpioValues[::-1]
    _matrix = Leds()
    global _runner
    gpioValues = list(gpioValues)
    global reset
    global toggleMic
    global toggleOut
    if gpioValues[audioToggleMute] == '0' and toggleOut == True:
        if mixer.toggleOutMute():
            _runner.start(_matrix.mute, mixer._outMuted, mixer._inMuted)
        else:
            _runner.once(_matrix.mute, mixer._outMuted, mixer._inMuted)
        toggleOut = False
    elif gpioValues[audioLevelDown] == '0' and mixer._outMuted == False:
        mixer.setVolume(decreaseLevel)
        reset = False
        _runner.start(_matrix.volume, int((18/100)*mixer._outLevel))
    elif gpioValues[audioLevelUp] == '0' and mixer._outMuted == False:
        mixer.setVolume(increaseLevel)
        reset = False
        _runner.start(_matrix.volume, int((18/100)*(mixer._outLevel)))
    elif gpioValues[mikeToggleMute] == '0' and toggleMic == True:
        if mixer.toggleMike():
            _runner.start(_matrix.mute, mixer._outMuted, mixer._inMuted)
        else:
            _runner.once(_matrix.mute, mixer._outMuted, mixer._inMuted)
        toggleMic = False
    elif reset == False:
        _runner.once(_matrix.clear)
        reset = True
    elif toggleOut == False and gpioValues[audioToggleMute] == '1':
        toggleOut = True
    elif toggleMic == False and gpioValues[mikeToggleMute] == '1':
        toggleMic = True

if __name__ == "__main__":
    ioloop.install()
    Process(target=driver_keep_alive, args=(matrix_ip, gpio_port, 1)).start()
    Process(target=register_data_callback, args=(gpio_callback, matrix_ip, gpio_port)).start()
    config_gpio_read()
